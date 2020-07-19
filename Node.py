from utils import *
from Neighbor import Neighbor
from Hello import Hello
from Log import Log
from Log import Log_final

class Node():
    def __init__(self, addresses, N, id, log_path, expire_time=8, comm_time=2):
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
        self.active = True
        self.neighbors = []
        self.num_neighbors = 0
        self.id = id

        self.NLock = threading.Lock()
        self.NeighborsLock = threading.Lock()
        self.SearchLock = threading.Lock()
        self.LogLock = threading.Lock()

        self.SearchFlag = False
        self.log_path = log_path
        self.stop = False
        self.log_bank = [self.address]
        self.make_udp_sock()
        self.init_neighbors()
        self.init_log_file()

    def log(self,log):
        self.log_bank.append(log)

    def log_neighbors(self):
        try :
            new_neighbors = [x for x in self.neighbors if x['type'] == 'bi']
            return {"address" : new_neighbors[0]['address'], 
                            "last_sent_to" : new_neighbors[0]['last_sent_to'], 
                            "last_recv_from" : new_neighbors[0]["last_recv_from"], 
                                "type" : new_neighbors[0]["type"]}
        except:
            return {}

    def final_log(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.log_bank, file, indent=2)

        with open(self.file_current_neighbors, 'a') as file:
            json.dump(Log_final(self.address, self.log_neighbors()), file, indent=2)
        

    def init_log_file(self):
        self.file_name = os.path.join(self.log_path, f'{self.address[1]}.log')
        with open(self.file_name, 'w') as _:
            pass

        self.file_current_neighbors = os.path.join(self.log_path, f'current_neighbors.log')
        with open(self.file_current_neighbors, 'a') as _:
            pass
            
    def init_neighbors(self):
        for address in self.addresses:
            if not self.is_address_mine(address):
                self.neighbors.append(Neighbor(address, time.time(), time.time()))


    def periodic_send(self):
        while(True):
            if self.stop:
                exit()

            time.sleep(self.comm_time)
            if not self.active:
                time.sleep(1)
                continue
            
            self.NeighborsLock.acquire()

            # print(self.address, "sending ....")
            for i in self.neighbors:
                if i['type'] == 'bi' or i['type'] == 'temp' or i['type'] == 'tempuni':
                    i['last_sent_to'] = time.time()
                    self.LogLock.acquire()
                    self.log(Log('SEND', i['address'], self.neighbors, time.time()))
                    self.LogLock.release()
                    self.send_HELLO(i['address'])

            self.NeighborsLock.release()




    def rcv(self):
        while(True):
            if self.stop:
                exit()
            try:
                (message, address) = self.socket.recvfrom(self.buffsize)
            except: continue
            hello = json.loads(message.decode())
            address = (hello['sender_address'][0], hello['sender_address'][1])
            

            self.NLock.acquire()
            self.NeighborsLock.acquire()

            # if not active
            if not self.active:
                time.sleep(1)
                self.NeighborsLock.release()
                self.NLock.release()
                continue

            # if pckt loss
            rand = random.random()
            if rand < 0.05:
                self.LogLock.acquire()
                log = Log('PcktLoss', address, self.neighbors, time.time())
                self.log(log)
                self.LogLock.release()
                self.NeighborsLock.release()
                self.NLock.release()
                continue
            self.LogLock.acquire()
            log = Log('RCV', address, self.neighbors, time.time())
            self.log(log)
            self.LogLock.release()
            
            
            neighbor = self.get_neighbor_by_address(address)
            t = neighbor['type']
            if t == 'bi':
                self.rcv_bi_handler(neighbor, hello)
            elif t == 'uni':
                self.rcv_uni_handler(neighbor, hello)
            elif t == 'temp':
                self.rcv_temp_handler(neighbor, hello)
            elif t == 'tempuni':
                self.rcv_tempuni_handler(neighbor, hello)
            else:
                self.rcv_none_handler(neighbor, hello)

            self.LogLock.acquire()
            log = Log('UPDATE', address, self.neighbors, time.time())
            self.log(log)
            self.LogLock.release()

            # print("UPDATE", self.address)
            # for i in self.neighbors:
            #     print(i['address'], i['type'])
            # print(" ")

            self.NeighborsLock.release()
            self.NLock.release()



    def need_neighbors(self):
        '''
        before calling this function hold NLOCK and NeighborLock 
        '''
        if self.num_neighbors >= self.N:
            return False
        return True

    def rcv_bi_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        
    def rcv_uni_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        if not self.need_neighbors():
            return

        for address, _ in hello['neighbors']:
            address = (address[0], address[1])
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                self.num_neighbors += 1
                self.SearchLock.acquire()
                self.SearchFlag = False
                self.SearchLock.release()
                return

    def rcv_tempuni_handler(self, neighbor, hello):
        self.rcv_uni_handler(neighbor, hello)

    def rcv_temp_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        if not self.need_neighbors():
            return

        for address, _ in hello['neighbors']:
            address = (address[0], address[1])
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                self.num_neighbors += 1
                self.SearchLock.acquire()
                self.SearchFlag = False
                self.SearchLock.release()
                return
        neighbor['type'] = 'tempuni'


        
    def rcv_none_handler(self, neighbor, hello):
        self.update_rcv_from(neighbor, hello)
        if not self.need_neighbors():
            return

        for address, _ in hello['neighbors']:
            address = (address[0], address[1])
            if self.is_address_mine(address):
                neighbor['type'] = 'bi'
                self.num_neighbors += 1
                self.SearchLock.acquire()
                self.SearchFlag = False
                self.SearchLock.release()
                return
        neighbor['type'] = 'uni'
        

    def update_rcv_from(self, neighbor, hello):
        neighbor['last_recv_from'] = time.time()
        neighbor['neighbors_list'] = hello['neighbors']
    


    def maintain_neighbors(self):
        while(True):
            if self.stop:
                exit()
            time.sleep(1)

            self.NLock.acquire()
            self.NeighborsLock.acquire()

            for neighbor in self.neighbors:
                if neighbor['type'] == 'tempuni':
                    neighbor['type'] = 'uni'

            for neighbor in self.neighbors:
                if time.time() - neighbor['last_recv_from'] > self.expire_time:
                    if neighbor['type'] == 'bi':
                        self.num_neighbors -= 1
                        print(self.address, "missed -->", neighbor['address'])
                    neighbor['type'] = None

                    self.LogLock.acquire()
                    log = Log('DUMP', neighbor['address'], self.neighbors, time.time())
                    self.log(log)
                    self.LogLock.release()

            self.NeighborsLock.release()
            self.NLock.release()

            self.SearchLock.acquire()
            self.SearchFlag = False
            self.SearchLock.release()


    def find_neighbors(self):
        while(True):
            if self.stop:
                exit()

            self.NLock.acquire()
            if not(self.active and self.num_neighbors < self.N):
                self.NLock.release()
                time.sleep(1)
                continue
            self.NLock.release()

            self.SearchLock.acquire()
            if self.SearchFlag:
                self.SearchLock.release()
                time.sleep(1)
                continue
            self.SearchFlag = True
            self.SearchLock.release()

            new_address = self.get_random_neighbor()
            # acqire Neighbots
            self.NeighborsLock.acquire()
            # update temp
            neighbor = self.get_neighbor_by_address(new_address)
            

            neighbor['type'] = 'temp'
            self.LogLock.acquire()
            log = Log('SEARCH', neighbor['address'], self.neighbors, time.time())
            self.log(log)
            self.LogLock.release()
            self.NeighborsLock.release()




    def get_my_neighbors(self):
        my_neighbors = []
        for neighbor in self.neighbors:
            if neighbor['type'] == "bi" or neighbor['type'] == "uni" or neighbor['type'] == "tempuni":
                my_neighbors.append((neighbor['address'], neighbor['type']))
        return my_neighbors

        
    def get_neighbor_by_address(self, address):
        for neighbor in self.neighbors:
            if neighbor['address'] == address:
                return neighbor

    def send_HELLO(self, address):
        neighbor = self.get_neighbor_by_address(address)
        hello = Hello(self.address, None, self.get_my_neighbors(), neighbor)
        try:
            self.socket.sendto(repr(hello).encode(), address)
        except:
            pass


    def make_udp_sock(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(self.address)
        self.buffsize = 1024
        self.socket.settimeout(1)


    def get_random_neighbor(self):
        mask = copy.deepcopy(self.addresses)
        random.shuffle(mask)
        for address in mask:
            neighbor = self.get_neighbor_by_address(address)
            if self.is_address_bi(address) or self.is_address_mine(address):
                continue
            return address


    def is_address_bi(self, address):
        for neighbor in self.neighbors:
            if neighbor['address'] == address and neighbor['type'] == 'bi':
                return True
        return False

    def is_address_mine(self, address):
        if address == self.address:
            return True
        return False

    
    def run(self):
        # find neighbor
        a = Thread(target=self.find_neighbors, args=())
        a.start()

        # sending every 2 seconds
        b = Thread(target=self.periodic_send, args=())
        b.start()

        # recv from others
        c = Thread(target=self.rcv, args=())
        c.start()

        # neighbor maintanacne
        d = Thread(target=self.maintain_neighbors, args=())
        d.start()

        a.join()
        b.join()
        c.join()
        d.join()
        self.final_log()

