from Manager import *

NODES = 6
N = 3
TIME = 10
BASEPORT = 8000

network_manager = Manager(NODES, N, TIME, BASEPORT)
network_manager.run()

