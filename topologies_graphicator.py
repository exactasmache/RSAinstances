#!/usr/bin/env python

'''
    This script reads the topologies stored in the topologies directory
    and generates the images that represent them.
'''

import os
import networkx as nx
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

__author__ = "Marcelo Bianchetti"
__credits__ = ["Marcelo Bianchetti"]
__version__ = "1.0.0"
__maintainer__ = "Marcelo Bianchetti"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Production"


def readTopology(tops_dir, top_fname):
    G = nx.DiGraph()
    ''' Returns the graph '''
    with open(os.path.join(tops_dir, top_fname)) as f:
        for l in f:
            if l.startswith('#'):
                continue
            ls = l.split()
            n, m = int(ls[0]), int(ls[1])
            G.add_nodes_from([i for i in range(n)])
            for i in range(m):
                l = f.readline().split()
                e1, e2 = int(l[0]), int(l[1])
                G.add_edge(e1, e2)
                G.add_edge(e2, e1)
    return G


def draw(G, iname, layout='net', **args):
    if layout == 'net':
        nx.draw_networkx(G, **args)
    if layout == 'circ':
        nx.draw_circular(G, **args)
    if layout == 'kam':
        nx.draw_kamada_kawai(G, **args)
    if layout == 'spec':
        nx.draw_spectral(G, **args)
    if layout == 'rnd':
        nx.draw_random(G, **args)

    plt.savefig(iname, dpi=400)
    plt.close()
    return


if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.abspath(__file__))
    topologies_dir = os.path.join(main_dir, 'topologies')
    images_dir = os.path.join(main_dir, 'images')
    image_fname = 'image_{}_{}.png'

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for top_fname in os.listdir(topologies_dir):
        top_name = os.path.splitext(top_fname)[0]
        G = readTopology(topologies_dir, top_fname)
        image_dir = os.path.join(images_dir, image_fname)

        layouts = ['net', 'circ', 'kam', 'spec', 'rnd']
        for layout in layouts:
            iname = image_dir.format(top_name, layout)

            draw(G, iname, layout, with_labels=True, node_color='#abcfff',
                 arrowsize=5, node_size=250)
