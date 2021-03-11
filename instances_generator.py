#!/usr/bin/env python

'''
    This script reads the topologies stored in the topologies directory
    and generates a serie of instances files for the RSA for each topology
    based on the data of the bibliography. It depends on the modulation level
    the optical fiber used, the graph density among other paramters.

    From the literature we obtained the most used data for the RSA problem:

    + The slot bandwith most of the cases is 12.5 GHz. However it could be
    smaller (sometimes 5 GHz) or larger, but not much larger, due to the fact
    that for the RWA problem with WDM, the minimum bandwidth of the slot is
    50 GHz and the main objective of RSA is to improve granularity.

    + The bandwidth of the optical fiber used on average is 4800 GHz,
    although the theoretical maximum bandwidth of the optical fiber is
    around 231 THz.
'''

import os
import random
import argparse
import numpy as np
import math

__author__ = "Marcelo Bianchetti"
__credits__ = ["Marcelo Bianchetti"]
__version__ = "1.2.0"
__maintainer__ = "Marcelo Bianchetti"
__email__ = "mbianchetti at dc.uba.ar"
__status__ = "Production"

line_enter = '{}\n'
sep = '\t'


def error(err):
    print("ERROR: {}".format(err))
    exit(1)


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
    ''' Returns the amount of nodes and edges of the graph '''
    with open(os.path.join(tops_dir, top_fname)) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.split()
            return int(line[0]), int(line[1])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-mdir",
                        type=str,
                        help="The main directory or path. If no tdir or idir "
                             "parameters are used, mdir must contain the "
                             "'topologies' and/or 'instances' folder. The "
                             "default value is the location of this script")
    parser.add_argument("-tdir",
                        type=str,
                        help="The topologies directory or path.")
    parser.add_argument("-idir",
                        type=str,
                        help="The directory or path for the created "
                        "instances.")
    parser.add_argument("-s", "--seed", type=int, default=1988,
                        help="The random seed. Default is 1988.")
    parser.add_argument("-S", "--slots", nargs='+', type=int,
                        help="List of amounts of available slots.")
    parser.add_argument("-p", "--percents", nargs='+', type=float,
                        help="List of maximum percentage of total available "
                             "slots that a demand can use. Must be in (0, 1].")
    args = parser.parse_args()

    main_dir = (os.path.dirname(os.path.abspath(__file__))
                if args.mdir is None else args.mdir)

    topologies_dir = (os.path.join(main_dir, 'topologies')
                      if args.tdir is None
                      else os.path.abspath(args.tdir))

    instances_dir = (os.path.join(main_dir, 'instances')
                     if args.idir is None
                     else os.path.abspath(args.idir))

    for d in [main_dir, topologies_dir]:
        if not os.path.exists(d):
            error("Directory '{}' not found.".format(d))

    instance_fname = 'instance_{}_{}_{}_{}.txt'

    random.seed(args.seed)

    # Available slots per fiber

    avaliable_S = ([10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 400,
                    600, 800, 1000] if args.slots is None else
                   [s for s in set(args.slots) if s > 0])

    # Default: From a lightly loaded network to a heavily loaded one.
    max_percentages_of_slots_by_demand = (np.arange(.1, .9, .1)
                                          if args.percents is None else
                                          [p for p in set(args.percents)
                                           if p > 0 and p <= 1])

    # Creation of instances directory if it does not exist
    if not os.path.exists(instances_dir):
        os.makedirs(instances_dir)

    for percentage in max_percentages_of_slots_by_demand:

        # The resulting instances are created in directories
        # acoording to their percentage and topologies
        percentage_dir = os.path.join(instances_dir,
                                      "{}".format(round(percentage, 2) * 100))

        # Creation of instance directory if it does not exist
        if not os.path.exists(percentage_dir):
            os.makedirs(percentage_dir)

        for top_fname in os.listdir(topologies_dir):
            top_name = os.path.splitext(top_fname)[0]
            n, m = readTopologyData(topologies_dir, top_fname)

            # The resulting instances are created in directories
            # acoording to their topologies
            top_dir = os.path.join(percentage_dir, top_name)

            # Creation of instance directory if it does not exist
            if not os.path.exists(top_dir):
                os.makedirs(top_dir)

            # Iterates over each available S
            for S in avaliable_S:
                max_sd = math.ceil(percentage * S)

                max_nD = calculateMaxNumberOfDemands(n, m, S, max_sd)
                nD = random.randint(int(max_nD/2), max_nD)

                demand_f = os.path.join(
                    top_dir, instance_fname.format(
                        top_name, S, max_sd, nD))

                with open(demand_f, 'w') as out:
                    out.write('# Created by {}\n'.format(__author__))
                    out.write('# Version: {}\n'.format(__version__))
                    out.write('# Seed: {}\n'.format(args.seed))
                    out.write('# Format:\n')
                    out.write('#   First line: S  |D|\n')
                    out.write('#   Other lines: <src\tdst\t#slots>\n')

                    line = '{}{}{}'.format(S, sep, nD)
                    out.write(line_enter.format(line))

                    for _ in range(nD):
                        src, dst = random.sample(range(n), 2)
                        s = random.randint(1, max_sd)
                        line = '{src}{sep}{dst}{sep}{s}'.format(
                            S=S, sep=sep, src=src, dst=dst, s=s)
                        out.write(line_enter.format(line))


# git commit -m "Version that allows to pass the directory names, the seed, the max slot available per arc and the percentage of the slots that a demand can use as arguments. Reordering the output directories. "