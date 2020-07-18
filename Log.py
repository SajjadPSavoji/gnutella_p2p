from utils import *

class Log(dict):
    '''
    procedures: [DUMP, RCV, SEND, UPDATE, SEARCH, PcktLoss]
    '''
    def __init__(self, procedure, address, hosts_neighbors, time):
        super().__init__(time=time, procedure=procedure, address=address, neighbors=hosts_neighbors)

if __name__ == "__main__":
    pass