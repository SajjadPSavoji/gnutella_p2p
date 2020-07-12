from utils import *

class Hello(dict): 
    def __init__(self, sender_address, type, sender_neighbors, neighbor):
        super().__init__(self, sender_address=sender_address, type=type, neighbors = sender_neighbors,
        last_sent_to = neighbor['last_sent_to'] , last_rcv_from = neighbor['last_recv_from'])

    def __repr__(self):
        return json.dumps(self)

    def __str__(self):
        return json.dumps(self)


if __name__ == "__main__":
    pass    