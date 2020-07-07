from utils import *

class Hello():
    def __init__(self, sender_id, sender_address, type, sender_neighbors, rcv_neighbor):
        self.__dict__ = {}
        self.__dict__['id'] = sender_id
        self.__dict__['address'] = sender_address
        self.__dict__['type'] = type
        self.__dict__['neighbors'] = sender_neighbors
        self.__dict__['rcv'] = rcv_neighbor

    def __repr__(self):
        return json.dumps(self.__dict__).encode()

if __name__ == "__main__":
    pass