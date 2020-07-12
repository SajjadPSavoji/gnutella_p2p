from utils import *
from Neighbor import Neighbor
from Hello import Hello

class Node():
    def __init__(self, addresses, N, active, id, expire_time=8, comm_time=2):
        '''
        address (ip, port)
        addresses are the initial addresses that client should hit: list of addresses
        N is the number of neighbors
        expire time is the time within wich on communication should have happened
        comm_time is the period of sending messeges
        active is the permission to work
        '''
        self.address = addresses[id]
        self.addresses = addresses
        self.N = N
        self.expire_time = expire_time
        self.comm_time = comm_time
        self.active = active
        self.neighbors = []
        self.num_neighbors = 0
        self.id = id
        self.NLock = threading.Lock()
        self.NeighborsLock = threading.Lock()
        self.SearchLock = threading.Lock()
        self.SearchFlag = False

        self.make_udp_sock()
        self.init_neighbors()
        self.run()


    def init_neighbors(self):
        for address in self.addresses:
            if not self.is_address_mine(address):
                self.neighbors.append(Neighbor(address, -1, -1))


    def periodic_send(self):
        while(True):
            time.sleep(self.comm_time)

            self.NeighborsLock.acquire()

            for i in self.neighbors:
                if i['type'] == 'bi' or i['type'] == 'temp':
                    i['last_sent_to'] = time.time()
                    self.send_HELLO(i['address'])

            self.NeighborsLock.release()



    def rcv(self):
        while(True):
            if not self.active:
                continue
            (message, address) = self.socket.recvfrom(self.buffsize)
            hello = json.loads(message.decode())
            address = hello['sender_address']
            

            rand = random.random()
            if rand < 0.05:
                continue

            self.NLock.acquire()
            # acwuire N LoCK
            self.NeighborsLock.acquire()
            # acwuice neighors Lock
            if self.num_neighbors >= self.N:
                self.NLock.release()
                self.NeighborsLock.release()
                continue
            # check if num neighbors < N
            neighbor = self.get_neighbor_by_address(address)
            t = neighbor['type']
            if t == 'bi':
                self.rcv_bi_handler(neighbor, hello)
            elif t == 'uni':
                self.rcv_uni_handler(neighbor, hello)
            elif t == 'temp':
                self.rcv_temp_handler(neighbor, hello)
            else:
                self.rcv_none_handler(neighbor, hello)

            self.NLock.release()
            self.NeighborsLock.release()

    def rcv_bi_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        
    def rcv_uni_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        for address, _ in hello['neighbors']:
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                return

    def rcv_temp_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        for address, _ in hello['neighbors']:
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                self.SearchLock.acquire()
                self.SearchFlag = False
                self.SearchLock.release()
                return
        neighbor['type'] = 'uni'

        
    def rcv_none_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        for address, _ in hello['neighbors']:
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                return
        neighbor['type'] = 'uni'
        

    def update_rcv_from(self, neighbor, hello):
        neighbor['last_rcv_from'] = time.time()
        neighbor['neighbors'] = hello['neighbors']
    


    def maintain_neighbors(self):
        while(True):
            time.sleep(self.expire_time)
            # @TODO
            self.NeighborsLock.acquire()
            self.NLock.acquire()
            for neighbor in self.neighbors:
                if time.time() - neighbor['last_rcv_from'] > self.expire_time:
                    if neighbor['type'] == 'bi':
                        self.num_neighbors -= 1
                    neighbor['type'] = None
            self.NLock.release()
            self.NeighborsLock.release()

            self.SearchLock.acquire()
            self.SearchFlag = False
            self.SearchLock.release()

    def find_neighbors(self):
        while(True):
            # @TODO
            self.NLock.acquire()
            if not(self.active and self.num_neighbors < self.N):
                self.NLock.release()
                continue
            self.NLock.release()

            self.SearchLock.acquire()
            if self.SearchFlag:
                self.SearchLock.release()
                continue
            self.SearchFlag = True
            self.SearchLock.release()

            new_address = self.get_random_neighbor()
            # acqire Neighbots
            self.NeighborsLock.acquire()
            # update temp
            Neighbor = self.get_neighbor_by_address(new_address)
            Neighbor['type'] = 'temp'
            # release
            self.NeighborsLock.release()


    def get_my_neighbors(self):
        my_neighbors = []
        for neighbor in self.neighbors:
            if neighbor['type'] == "bi" or neighbor['type'] == "uni":
                my_neighbors.append((neighbor['address'], neighbor['type']))
        return my_neighbors

        
    def get_neighbor_by_address(self, address):
        for neighbor in self.neighbors:
            if neighbor['address'] == address:
                return neighbor

    def send_HELLO(self, address):
        neighbor = self.get_neighbor_by_address(address)
        hello = Hello(self.address, None, self.get_my_neighbors(), neighbor)
        self.socket.sendto(repr(hello).encode(), address)


    def make_udp_sock(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.buffsize = 1024


    def get_random_neighbor(self):
        mask = copy.deepcopy(self.addresses)
        random.shuffle(mask)
        for address in mask:
            if self.is_address_bi(address) or self.is_address_mine(address):
                continue
            return address


    def is_address_bi(self, address):
        for neighbor in self.neighbors:
            if neighbor['address'] == address and neighbor['type'] == 'bi':
                return True
        return False

    def is_address_mine(self, address):
        if address == self.addresses:
            return True
        return False
    
    def run(self):
        # find neighbor
        start_new_thread(self.find_neighbors, ())
        # sending every 2 seconds
        start_new_thread(self.periodic_send, ())
        # # recv from others
        start_new_thread(self.rcv, ())
        # # neighbor maintanacne
        # start_new_thread(self.maintain_neighbors, ())


if __name__ == "__main__":
    pass