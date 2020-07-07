from utils import *
class Neighbor():
    def __init__(self, address, last_sent_to_time, last_recv_from_time):
        '''
        address = (ip, port)
        '''
        self.__dict__ = {}
        self.__dict__['address'] = address
        self.__dict__["last_sent_to_time"] = last_sent_to_time
        self.__dict__['last_recv_from_time'] = last_recv_from_time

    def __repr__(self):
        return json.dumps(self.__dict__).encode()



    