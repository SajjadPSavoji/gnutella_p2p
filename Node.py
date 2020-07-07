from utils import *

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
    
    def maintain_neighbors(self):
        pass

    def find_neighbors(self):
        pass

    def get_random_neighbor(self):
        mask = copy.deepcopy(self.addresses)
        random.shuffle(mask)
        for address in mask:
            if self.is_address_in_neighbors(address) or self.is_address_mine(address):
                continue
            return address


    def is_address_in_neighbors(self, address):
        for neighbor in self.neighbors:
            if neighbor.__dict__['address'] == address:
                return True
        return False

    def is_address_mine(self, address):
        if address == self.addresses:
            return True
        return False


    
