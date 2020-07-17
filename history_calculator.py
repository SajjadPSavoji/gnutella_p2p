from utils import *

class History_Log(dict):
    def __init__(self,address,  neighbor_addresses, rcv_pack, send_pack):
        super().__init__(address=address, neighbor_addresses=neighbor_addresses, 
                            rcv_pack=rcv_pack, send_pack=send_pack)


class history_calculator():

    def __init__(self, base_port, num_nodes, address, log_path = './logs/', address_dest='history'):

        self.base_port = base_port
        self.num_nodes = num_nodes
        self.log_path = log_path
        self.address = address
        self.file_name = os.path.join(self.log_path, f'{self.address[1]}.log')
        self.addresses = [('', self.base_port + i) for i in range(self.num_nodes)]
        self.address_dest = address_dest

        self.read_input()
        self.init_log_file()
    
    def read_input(self):
        with open(self.file_name, 'r') as file:
            self.data = json.load(file)

    def init_log_file(self):
        self.dest_file = os.path.join(self.log_path, f'{self.address_dest}.log')
        with open(self.dest_file, 'w') as _:
            pass

    def log(self,log):
        with open(self.dest_file, 'a') as file:
            json.dump(log, file, indent=2)


    def all_time_neighbors(self):
        num_sent_packets = [0 for i in range(self.num_nodes)]
        num_rcv_packets = [0 for i in range(self.num_nodes)]
        for log in self.data:

            if log['procedure'] == "SEND":
                num_sent_packets[log['address'][1] - self.base_port] += 1
            elif log['procedure'] == "RCV":
                num_rcv_packets[log['address'][1] - self.base_port] += 1

        self.log(History_Log(self.address, self.addresses, num_rcv_packets, num_sent_packets))
        
        

hc = history_calculator(8000, 3,('',8000))
print(hc.file_name)
hc.all_time_neighbors()


