from utils import *
from Node import *

Minute = 60
Duration = 0.1


class Manager():
    def __init__(self, num_nodes, num_neighbour, max_time, base_port, log_path = './logs/'):
        self.num_nodes = num_nodes
        self.num_neighbour = num_neighbour
        self.list_nodes = []
        self.max_time = max_time
        self.ip = ''
        self.node_port = base_port
        self.addresses = [(self.ip, self.node_port + i) for i in range(self.num_nodes)]
        self.list_threads = []
        self.log_path = log_path
        self.init_log_dir()

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

        print('All threads are joined and the program is finished.')

    
    def run(self):
        self.create_node()
        self.set_activations()


