from utils import *
import sys

MINUTE = 60

class Access_Log(dict):
    def __init__(self,address,  neighbor_access_time):
        super().__init__(address=address, neighbor_access_time=neighbor_access_time)


class access_calculator():

    def __init__(self, base_port, num_nodes, address, duration, address_dest='./logs/access.log', log_path = './logs/'):

        self.base_port = base_port
        self.num_nodes = num_nodes
        self.log_path = log_path
        self.address = address
        self.file_name = os.path.join(self.log_path, f'{self.address[1]}.log')
        self.addresses = [('', self.base_port + i) for i in range(self.num_nodes)]
        self.address_dest = address_dest
        self.duration = duration

        self.read_input()
        self.init_log_file()
    
    def read_input(self):
        with open(self.file_name, 'r') as file:
            self.data = json.load(file)

    def init_log_file(self):
        self.dest_file = self.address_dest
        with open(self.dest_file, 'a') as _:
            pass

    def log(self,log):
        with open(self.dest_file, 'a') as file:
            json.dump(log, file, indent=2)


    def all_time_neighbors(self):
        self.sumtimes = [0 for i in range(self.num_nodes)]
        self.last_time = [-1 for i in range(self.num_nodes)]
        begin_time = self.data[1]['time']
        log_time = -1

        for log in self.data:
            if log == ['', self.address[1]]:
                continue

            log_time = log['time']
            for x in log['neighbors']:
                index = x['address'][1] - self.base_port
                if x['type'] == 'bi':# or x['type'] == 'uni' or x['type'] == 'tempuni':
                    if self.last_time[index] == -1:
                        self.last_time[index] = log_time
                    else:
                        self.sumtimes[index] += (log_time - self.last_time[index])
                        self.last_time[index] = log_time
                else:
                    self.last_time[index] = -1
        
        time_ratios = [x / (self.duration * MINUTE) for x in self.sumtimes]
        neighbor_access_time = {}
        for i in range(self.num_nodes):
            neighbor_access_time[str(self.base_port + i)] = time_ratios[i]

        self.log(Access_Log(self.address, neighbor_access_time))


ac = access_calculator(int(sys.argv[1]), int(sys.argv[2]),('',int(sys.argv[3])), float(sys.argv[4]), sys.argv[5])
ac.all_time_neighbors()


