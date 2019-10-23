#!/usr/bin/env python

'''
    This script reads the topologies stored in the topologies directory
    and generates a serie of instances files for the RSA for each topology 
    based on the data of the bibliography. It depends on the modulation level
    the optical fiber used, the graph density among other paramters.

    From the bibliography we got the next more commonly used data for the RSA:

    + The slot bandwith is between 5 and 12.5 GHz, but it could be greater. 
    50 GHz is the used on the WDM problem.

    + The slot bitrate is about 2.5 Gbps
    
    + The average optical fiber used bandwidth is 4800 GHz despite the maximal
    optical fiber bandwith is around 231 THz.
'''

import os
import random

__author__ = "Marcelo Bianchetti"
__credits__ = ["Marcelo Bianchetti"]
__version__ = "1.0.0"
__maintainer__ = "Marcelo Bianchetti"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Production"

line_enter = '{}\n'
sep = '\t'


def calculateGraphDensity(n, m):
    ''' Returns the density of the undirected graph '''
    return 2.*m/(n*(n-1))


def calculateMaxNumberOfDemands(n, m, S, max_sd):
    ''' Given a graph and the amount of slots per link
        it returns an estimative of the max amount of 
        demands per instance. 

        n: number of nodes
        m: number of undirected edges
        S: chosen number of slots per arc
        max_sd: chosen max value for slots by demand

        A tighter bound could be the min grade of the 
        nodes but we want infeasible instances too.
    '''
    d = calculateGraphDensity(n, m)
    max_n_of_demands = int((n-1.) * d * S/(max_sd/2.))
    return max_n_of_demands


def readTopologyData(tops_dir, top_fname):
    ''' Returns the amount of nodes, edges and density of the graph '''
    with open(os.path.join(tops_dir, top_fname)) as f:
        for l in f:
            if l.startswith('#'):
                continue
            l = l.split()
            return int(l[0]), int(l[1])


if __name__ == "__main__":
    main_dir = os.path.dirname(os.path.abspath(__file__))
    topologies_dir = os.path.join(main_dir, 'topologies')
    instances_dir = os.path.join(main_dir, 'instances')
    instance_fname = 'instance_{}_{}_{}_{}.txt'

    avaliable_S = [10, 15, 20, 30, 40, 60, 80,
                   100, 150, 200, 300, 400, 600, 800, 1000]

    # From a low loaded network to a really high loaded one.
    max_slots_by_demand = [4, 10, 15, 20, 25, 30, 50, 80]

    if not os.path.exists(instances_dir):
        os.makedirs(instances_dir)
    
    random.seed(1988)
    for top_fname in os.listdir(topologies_dir):
        top_name = os.path.splitext(top_fname)[0]
        n, m = readTopologyData(topologies_dir, top_fname)
        instance_dir = os.path.join(instances_dir, top_name)

        if not os.path.exists(instance_dir):
            os.makedirs(instance_dir)

        for S in avaliable_S:
            for max_sd in max_slots_by_demand:

                max_nD = calculateMaxNumberOfDemands(n, m, S, max_sd)
                nD = random.randint(int(max_nD/2), max_nD)
                
                demand_f = os.path.join(
                    instance_dir, instance_fname.format(top_name, S, max_sd, nD))

                with open(demand_f, 'w') as out:
                    out.write('# Created by {}\n'.format(__author__))
                    out.write('# Format:\n')
                    out.write('#   First line: S  |D|\n')
                    out.write('#   Other lines: <src\tdst\t#slots>\n')
                    
                    l = '{}{}{}'.format(S, sep, nD)
                    out.write(line_enter.format(l))
                    
                    for _ in range(nD):
                        src, dst = random.sample(range(n), 2)
                        s = random.randint(1, max_sd)
                        l = '{src}{sep}{dst}{sep}{s}'.format(S=S, sep=sep, src=src, dst=dst, s=s)
                        out.write(line_enter.format(l))
