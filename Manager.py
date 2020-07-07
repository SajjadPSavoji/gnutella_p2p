from utils import *

class Manager():
    def __init__(self, num_nodes, num_neighbour, max_time):
        num_nodes = num_nodes
        num_neighbour = num_neighbour
        list_nodes = []
        list_actives = [[True] for i in range(num_nodes)]
        max_time = max_time


    def portal(self, ..........):
        list_nodes.append(Node('''dsafsdasdasdsadsa'''))

    def create_node(self):
        for i in range(num_nodes):
            start_new_thread(self.portal, (..........))

    
    def self.set_activations(self):
        past = time.time()
        last = -1
        this = -1
        
        while True:
            if time.time() - past >= max_time:
                past = time.time()
                x = random.ranint(0, 5)
                list_actives[x] = False
                list_actives[last] = True

                last = this
                this = x

    
    def Run(self):
        self.create_node()
        self.set_activations()


