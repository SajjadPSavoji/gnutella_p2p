from utils import *
from Node import *

Minute = 60
Duration = 0.3


class Manager():
    def __init__(self, num_nodes, num_neighbour, max_time, base_port,
                             log_path = './logs/', address_dest='history'):
        self.num_nodes = num_nodes
        self.num_neighbour = num_neighbour
        self.list_nodes = []
        self.max_time = max_time
        self.ip = ''
        self.node_port = base_port
        self.addresses = [(self.ip, self.node_port + i) for i in range(self.num_nodes)]
        self.list_threads = []
        self.log_path = log_path
        self.address_dest = address_dest
        self.filename = 'history_calculator.py'
        self.access_file = 'access_calculator.py'

        self.init_log_dir()
        self.init_log_file()

    def init_log_file(self):
        self.dest_file = os.path.join(self.log_path, f'{self.address_dest}.log')
        with open(self.dest_file, 'w') as _:
            pass

        self.file_current_neighbors = os.path.join(self.log_path, f'current_neighbors.log')
        with open(self.file_current_neighbors, 'w') as _:
            pass

        self.file_access = os.path.join(self.log_path, f'access.log')
        with open(self.file_access, 'w') as _:
            pass

    def init_log_dir(self):
        try:
            os.mkdir(self.log_path)
        except:
            pass

    def portal(self, addr, num_neighbour, id):
        try:
            node = Node(addr, num_neighbour, id, self.log_path)
            self.list_nodes.append(node)
            node.run()
        except :
            pass

    def create_node(self):
        for i in range(self.num_nodes):
            new_thread = Thread(target=self.portal,
                         args=(self.addresses, self.num_neighbour, i,))
            new_thread.start()
            print("Node " + str(i + 1) + " is created.")
            self.list_threads.append(new_thread)
        
        print(" ")

    
    def set_activations(self):
        past = time.time()
        start = past
        last = -1
        this = -1
        x = -1
        
        while True:
            if time.time() - past >= self.max_time:
                
                x = -1
                while x == this or x == last or x == -1:
                    x = random.randint(0, self.num_nodes - 1)
                
                self.list_nodes[x].active = False
                
                if last != -1:
                    self.list_nodes[last].active = True

                past = time.time()
                last = this
                this = x
                
                print("_______")
                for i in self.list_nodes:
                    print(i.address,"is active -->" ,i.active)
                print("_______")


            if time.time() - start > Duration * Minute:
                break

        for node in self.list_nodes:
            node.active = True
            node.stop = True
                    
        for i in self.list_threads:
            i.join()
        print('All threads are joined.')

        for i in range(self.num_nodes):
            num = self.node_port + i
            os.system(f'python3 {self.filename} {self.node_port} {self.num_nodes} {num} {self.dest_file}')
            os.system(f'python3 {self.access_file} {self.node_port} {self.num_nodes} {num} {Duration} {self.file_access}')
        print('History and Access logs file created.')


    
    def run(self):
        self.create_node()
        self.set_activations()


