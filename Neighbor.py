from utils import *
class Neighbor(dict):
    def __init__(self, address, last_sent_to_time, last_recv_from_time, truthful=False):
        '''
        address = (ip, port)
        '''
        super().__init__(self, address=address, last_sent_to_time=last_sent_to_time
        , last_recv_from_time = last_recv_from_time, truthful = truthful, neighbors=None)
        # self.__dict__ = {}
        # self.__dict__['address'] = address
        # self.__dict__["last_sent_to_time"] = last_sent_to_time
        # self.__dict__['last_recv_from_time'] = last_recv_from_time
        # self.__dict__['truthful'] = truthful
        # self.__dict__['neighbors'] = None



    