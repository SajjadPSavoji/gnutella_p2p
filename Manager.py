from utils import *
from Node import *

class Manager():
    def __init__(self, num_nodes, num_neighbour, max_time, base_port):
        self.num_nodes = num_nodes
        self.num_neighbour = num_neighbour
        self.list_nodes = []
        self.list_actives = [[True] for i in range(num_nodes)]
        self.max_time = max_time
        self.ip = ''
        self.node_port = base_port
        self.addresses = [(self.ip, self.node_port+i) for i in range(self.num_nodes)]


    def portal(self, addr, num_neighbour, activity, id):
        try:
            self.list_nodes.append(Node(addr, num_neighbour, activity, id))
        except :
            pass

    def create_node(self):
        for i in range(self.num_nodes):
            start_new_thread(self.portal, (self.addresses, 
                    self.num_neighbour, self.list_actives[i],i))

    
    def set_activations(self):
        past = time.time()
        start = past
        last = -1
        this = -1
        
        while True:
        #     if time.time() - past >= self.max_time:
        #         past = time.time()
        #         x = random.randint(0, self.num_neighbour - 1)
        #         self.list_actives[x] = False
        #         self.list_actives[last] = True

        #         last = this
        #         this = x

            if time.time() - start > 60 * 5:
                exit()

    
    def run(self):
        self.create_node()
        self.set_activations()


