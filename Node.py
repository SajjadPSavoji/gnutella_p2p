from utils import *

class Node():
    def __init__(self, addresses, N, expire_time, comm_time, active, id):
        '''
        addresses are the initial addresses that client should hit
        N is the number of neighbors
        expire time is the time within wich on communication should have happened
        comm_time is the period of sending messeges
        active is the permission to work
        '''
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