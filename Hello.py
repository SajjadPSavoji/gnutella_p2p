from utils import *

class Hello(dict):
    def __init__(self, sender_id, sender_address, type, sender_neighbors, rcv_neighbor):
        super().__init__(self, id=sender_id, type=type
        , neighbors = sender_neighbors, rcv = rcv_neighbor)
        # self.__dict__ = {}
        # self.__dict__['id'] = sender_id
        # self.__dict__['address'] = sender_address
        # self.__dict__['type'] = type
        # self.__dict__['neighbors'] = sender_neighbors
        # self.__dict__['rcv'] = rcv_neighbor

    def __repr__(self):
        return json.dumps(self).encode()

if __name__ == "__main__":
    pass