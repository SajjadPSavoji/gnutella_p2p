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
            time.sleep(self.expire_time)

            for i in self.neighbors:
                if i['type'] == 'bi':
                    self.send_HELLO(i['address'])



    def rcv(self):
        while(True):
            if not self.active:
                continue

            (message, address) = self.socket.recvfrom(self.buffsize)
            print(message.decode())
            # @TODO
            # construct Hello class
            # acwuire N LoCK
            # acwuice neighors Lock
            # check if num neighbors < N
            # updsate neighbors


    def maintain_neighbors(self):
        while(True):
            time.sleep(self.expire_time)
            # @TODO
            self.NeighborsLock.acquire()
            for neighbor in self.neighbors:
                if time.time() - neighbor['last_rcv_from'] > self.expire_time:
                    neighbor['type'] = None
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
            # @TODO
            # acqire Neighbots
            # update temp
            # release
            #send HELLO packat to address
            self.send_HELLO(new_address)

    def get_my_neighbors(self):
        my_neighbors = []
        for neighbor in self.neighbors:
            if neighbor['type'] == "bi" or neighbor['type'] == "uni":
                my_neighbors.append([neighbor['address'], neighbor['type']])
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
        # creat 2 thread
        # find neighbor
        start_new_thread(self.find_neighbors, ())
        print('after run ')
        # sending every 2 seconds
        start_new_thread(self.periodic_send, ())
        # # recv from others
        # start_new_thread(self.rcv, ())
        # # neighbor maintanacne
        # start_new_thread(self.maintain_neighbors, ())


if __name__ == "__main__":
    pass