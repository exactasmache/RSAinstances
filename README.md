# RSA instances
This is a repository to store several topologies and a script to generate the instances for the NP-complete problem called Routing and Spectrum Allocation problem.

## [RSA problem](https://link.springer.com/article/10.1007/s11750-018-0483-6)
The __Routing and Spectrum Assignment problem__ (RSA) consists in establishing the lightpaths for a set of end-to-end traffic demands that are expressed in terms of the number of required slots. Since lightpaths are determined by a route and a selected channel, RSA involves finding a route and assigning frequency slots to each demand. To comply with the ITU recommendation, the following constraints must to be respected in this setting:

- __slot continuity:__ the slots assigned to a certain demand must remain the same on all the links of the corresponding route;
- __slot contiguity:__ the slots allocated to each demand must be contiguous;
- __non-overlapping slot:__ a slot can be assigned to various demands if the routes assigned to these demands do not share any link.

### Formally 
Given a directed graph __G=(V,E)__ representing the optical fiber network, a set of demands __D = {(s_1, t_1, v_1), ..., (s_k, t_k, v_k)}__ --such that each demand __i__ in __{1, ..., k}__ has a source __s_i__ in __V__, a target __t_i__ in __V__, and a volume __v_i__ (positive integer) -- and a fixed number __S__ (positive integer) of available slots, RSA consists in establishing a lightpath associated to each demand, in such a way that lightpaths do not overlap. In other words, each demand __i__ in __{1, ..., k}__ must be assigned a path __P_i__ beloging to __E__ in __G__ between __s_i__ and __t_i__ and an interval __I_i__ consisting of __v_i__ consecutive slots in __[1,S]__ in such a way that if the intersection of __P_i__ with __P_j__ is not empty then the intersetion of __I_i__ with __I_j__ must, for any two demands __i__ not equal to __j__ (i.e., if the paths assigned to __i__ and __j__ share an arc, then the assigned slot intervals must be disjoint).

## Parameters

From the literature we obtained the most used data for the RSA problem:

  - The slot bandwith most of the cases is 12.5 GHz. However it could be smaller (sometimes 5 GHz) or larger, but not much larger, due to the fact that for the RWA problem with WDM, the minimum bandwidth of the slot is 50 GHz and the main objective of RSA is to improve granularity.

  - The bandwidth of the optical fiber used on average is 4800 GHz, although the theoretical maximum bandwidth of the optical fiber is around 231 THz.

We use that information to define the default available number of slots per link the maximal amount of slots used by each demand and the amount of demands.
    
To define the number of demands of each instance, we estimate an upper limit using the density of the graph, the number of slots per link and the average of slots per demand trying to make the majority of instances feasible, but not all. The amount of demands will be a number between that and its half.

```
max_number_of_demands = (n - 1) * d * S / (max_slots_per_demand / 2)
```

## Files
The main scrip called **instances_generator.py** reads the topologies stored in the __topologies/__ directory and generates a serie of instances files for the RSA for each topology based on the data of the literature. It depends on the modulation level the optical fiber used, the graph density among other paramters.

## Data Format
The format of the data is commented in the header of each file. The separator used is the tabulation, and the line starting with # is a comment.
### Topology
The topology file is preceded by the number of nodes and the number of edges followed by the list of these one by line.
```
# Comment
|N|     |M|
<node i>    <node j>
<node k>    <node l>
...
```
Most of the instances belong to capacitated networks and we were able to obtain that data. In those cases, the weight of each edge is added when it is defined.
```
<node i>    <node j>    <weight ij>
```

### Generated Instance
As well as the problem is stated over directed graphs and due to the way in which the networks are made we asume all the links have both senses.

The instance file also begins with a header that briefly explains the format. The version of this software and the used seed are shown there. The number of slots available for each edge and the number of demands requested are shown below followed by the list of demands.
```
# Comment
S     |D|
<src d1>    <dst d1>      <n of slots required by d1>
<src d2>    <dst d2>      <n of slots required by d1>
...
```

## Usage
### Requirements
The requirements are stored in `requirements.txt`. They can be installed via

```
pip install -r requirements.txt
```

## Run
To generate the instances just run the script:

```
python instances_generator.py
```

By default the instances are going to be placed on a new folder called instances into the directory of the script into subfolders according to the maximum percent of slots used by demands and the topology. Each one of those files with its asociated topology are the input for the RSA problem.

Run the following to see how to configure the parameters:

```
python instances_generator.py -h

optional arguments:
  -h, --help            show this help message and exit
  -mdir MDIR            The main directory or path. If no tdir or idir parameters are used, mdir must contain the 'topologies' and/or 'instances' folder. The default
                        value is the location of this script
  -tdir TDIR            The topologies directory or path.
  -idir IDIR            The directory or path for the created instances.
  -s SEED, --seed SEED  The random seed. Default is 1988.
  -S SLOTS [SLOTS ...], --slots SLOTS [SLOTS ...]
                        List of amounts of available slots.
  -p PERCENTS [PERCENTS ...], --percents PERCENTS [PERCENTS ...]
                        List of maximum percentage of total available slots that a demand can use. Must be in (0, 1].
```

### Example
The following line will generate instances for S in [10, 25] and p in [10%, 20%, 30%, 50%]. They will be saved in `./instances/`.

```
python instances_generator.py -S 10 25 -p .1 .3 .5 .2
```

This one will generate instances with S in [10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000] and p in [10%, 20%, 30%, ..., 90%] in the directory `/home/instances`.

```
python instances_generator.py -idir /home/instances
```