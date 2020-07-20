from Manager import *

NODES = 6
N = 3
TIME = 10
BASEPORT = 8000
Top_file = 'Topology.py'

network_manager = Manager(NODES, N, TIME, BASEPORT)
network_manager.run()

os.system(f'python3 {Top_file}')

