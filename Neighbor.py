from utils import *
class Neighbor(dict):
    def __init__(self, address, last_sent_to_time, last_recv_from_time):
        '''
        address = (ip, port)
        '''
        super().__init__(self, address=address, last_sent_to=last_sent_to_time
        , last_recv_from = last_recv_from_time, type = None, neighbors_list=[])



    