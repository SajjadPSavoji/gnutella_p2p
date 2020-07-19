log_path = './logs/*.log'
top_path = './graphs/'
res_path = './res/'

import imageio
import glob
import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import shutil
from tqdm import tqdm

from matplotlib.lines import Line2D

legend_elements = [Line2D([0], [0], color='gray', lw=1, label='temp'),
                    Line2D([0], [0], color='black', lw=1, label='undirected'),
                    Line2D([0], [0], color='blue', lw=1, label='bi'),
                    Line2D([0], [0], color='green', lw=1, label='uni'),
                   ]



def vis_graph_via_log(log, my_port, save_path = top_path):    
    fig, ax = plt.subplots()
    ax.legend(handles=legend_elements, loc= 'lower right', fontsize=6)
    node_colors = ['blue' if node==my_port else 'gray' for node in G.nodes]
    # draw  nodes
    nx.draw_networkx_nodes(G, pos, node_color = node_colors, node_size = 500, edgecolors='black', alpha=0.5)
    nx.draw_networkx_labels(G,pos,font_size=8)

    # draw edges
    bi_edges = []
    uni_edges = []
    temp_edges = []
    ud_edges  = []

    for neighbor in log['neighbors']:
        neighbor_port = neighbor['address'][1]
        neighbor_type = neighbor['type']
        # uni
        if neighbor_type == 'uni':
            uni_edges.append((neighbor_port, my_port))
        elif neighbor_type == 'bi':
            bi_edges.append((neighbor_port, my_port))
            bi_edges.append((my_port, neighbor_port))
        elif neighbor_type == 'temp':
            temp_edges.append((my_port, neighbor_port))
        elif neighbor_type == 'tempuni':
            temp_edges.append((my_port, neighbor_port))
            uni_edges.append((neighbor_port, my_port))

        neighbor_neighbors = neighbor['neighbors_list']
        for nn in neighbor_neighbors:
            nn_port = nn[0][1]
            nn_type = nn[1]
            if nn_type == 'uni' or nn_type == 'tempuni':
                if (nn_port, neighbor_port) in bi_edges or (nn_port, neighbor_port) in uni_edges:
                    continue
                ud_edges.append((nn_port, neighbor_port))

            elif nn_type == 'bi':
                if not((nn_port, neighbor_port) in bi_edges or (nn_port, neighbor_port) in uni_edges or (nn_port, neighbor_port) in ud_edges):
                    ud_edges.append((nn_port, neighbor_port))
                if not((neighbor_port, nn_port) in bi_edges or (neighbor_port, nn_port) in uni_edges or (nn_port, neighbor_port) in ud_edges):
                    ud_edges.append((neighbor_port, nn_port))

    # G.add_edges_from(bi_edges)
    # G.add_edges_from(uni_edges)
    # G.add_edges_from(temp_edges)
    # G.add_edges_from(ud_edges)

    nx.draw_networkx_edges(G, pos, edgelist=temp_edges, arrows=True, edge_color='gray', style='dotted', alpha=0.5, connectionstyle= 'arc3,rad=0.1')
    nx.draw_networkx_edges(G, pos, edgelist=bi_edges, arrows=True, edge_color='blue', connectionstyle= 'arc3,rad=0.2')
    nx.draw_networkx_edges(G, pos, edgelist=uni_edges, arrows=True, edge_color='green', connectionstyle= 'arc3,rad=0.2')
    nx.draw_networkx_edges(G, pos, edgelist=ud_edges, arrows=True, edge_color='black', connectionstyle= 'arc3,rad=0.2')

    plt.title('time: ' + str(log['time']))
    plt.savefig(save_path + str(my_port) + '/' + str(log['time']) + '.png')
    plt.close()

def create_gif(port_num):
    anim_file = f'./gifs/{port_num}.gif'
    print(anim_file)
    file_names = None
    with imageio.get_writer(anim_file, mode='I') as writer:
        filenames = glob.glob(f'./graphs/{port_num}/*.png')
        filenames = sorted(filenames)
        last = -1
        for i,filename in enumerate(filenames):
            frame = 2*(i**0.5)
            if round(frame) > round(last):
                last = frame
            else:
                continue
            image = imageio.imread(filename)
            writer.append_data(image)
        image = imageio.imread(filename)
        writer.append_data(image)


try: shutil.rmtree(top_path)
except: pass

try: shutil.rmtree(res_path)
except: pass

try: shutil.rmtree('./gifs/')
except: pass


try:
    os.mkdir(top_path)
except:
    pass

try:
    os.mkdir(res_path)
except:
    pass

# ceate GIFS
# creat gif directory
try:
    os.mkdir('./gifs/')
except:
    pass

# extract log files
file_names = sorted(glob.glob(log_path))

# extrac node ports form log files
names = []
for file_name in file_names:
    with open(file_name, 'r') as f:
        log = json.load(f)
        names.append(log[0][1])

print(f'detected ports: {names}')

# creat sub dir for each node
for name in names:
    try:
        os.mkdir(top_path + f'{name}')
        os.mkdir(res_path + f'{name}')
    except:
        pass

G = nx.DiGraph()
G.add_nodes_from(names)
pos = nx.spring_layout(G)

for file_name in file_names:
    with open(file_name, 'r') as f:
        logs = json.load(f)
        my_port = logs[0][1]
        print(f'proceeding port: {my_port}')
        for log in tqdm(logs[1:]):
            vis_graph_via_log(log, my_port)
        vis_graph_via_log(logs[-1], my_port, res_path)
        create_gif(my_port)