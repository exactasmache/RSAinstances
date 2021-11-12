# RSA instances
This is a repository to store several topologies and a script to generate the instances for the NP-complete problem called Routing and Spectrum Allocation problem.

## [RSA problem](https://link.springer.com/article/10.1007/s11750-018-0483-6)
The __Routing and Spectrum Assignment problem__ (RSA) consists in establishing the lightpaths for a set of end-to-end traffic demands that are expressed in terms of the number of required slots. Since lightpaths are determined by a route and a selected channel, RSA involves finding a route and assigning frequency slots to each demand. To comply with the ITU recommendation, the following constraints must to be respected in this setting:

- __slot continuity:__ the slots assigned to a certain demand must remain the same on all the links of the corresponding route;
- __slot contiguity:__ the slots allocated to each demand must be contiguous;
- __non-overlapping slot:__ a slot can be assigned to various demands if the routes assigned to these demands do not share any link.

### Formally 
Given a directed graph _G = (V, E)_ representing the optical fiber network, a set of demands _D = {(s<sub>1</sub>, t<sub>1</sub>, v<sub>1</sub>), ..., (s<sub>k</sub>, t<sub>k</sub>, v<sub>k</sub>)}_ --such that each demand _i_ in _{1, ..., k}_ has a source _s<sub>i</sub>_ in _V_, a target _t<sub>i</sub>_ in _V_, and a volume _v<sub>i</sub>_ (positive integer) -- and a fixed number _s*_ (positive integer) of available slots, RSA consists in establishing a lightpath associated to each demand, in such a way that lightpaths do not overlap. In other words, each demand _i_ in _{1, ..., k}_ must be assigned a path _P<sub>i</sub>_ beloging to _E_ in _G_ between _s<sub>i</sub>_ and _t<sub>i</sub>_ and an interval _I<sub>i</sub>_ consisting of _v<sub>i</sub>_ consecutive slots in _[1, s*]_ in such a way that if the intersection of _P<sub>i</sub>_ with _P<sub>j</sub>_ is not empty then the intersetion of _I<sub>i</sub>_ with _I<sub>j</sub>_ must, for any two demands _i_ not equal to _j_ (i.e., if the paths assigned to _i_ and _j_ share an arc, then the assigned slot intervals must be disjoint).

Twelve integer linear programming models to solve this version of RSA can be found in [[1]](https://link.springer.com/article/10.1007/s11750-018-0483-6), and a branch-and-cut algorithm using several families of valid equalities, inequalities and optimality cuts can be found in [[2]](https://arxiv.org/abs/2106.15454).

## Parameters

Since RSA is a problem that appears on the optical fiber networks, we selected 20 topologies used in the literature to solve several communication problems, most of them being real optical fiber networks. Their parameters are summarized in the following table:

| Topology          | Nodes | Arcs | _&Delta;_ | min_<sub>v &isin; V</sub>&Delta;(v)_ | max_<sub>v&isin; V</sub> &Delta;(v)_ |
| :---------------- | :--: | :---: | :----: | :-: | :---: |
| 6n-9m-n6s9        |  6 |  18 | 0.60 | 4 | 8   |
| 10n-42m-SmallNet  | 10 |  42 | 0.47 | 4 | 12  |
| 10n-44m-SmallNet  | 10 |  44 | 0.49 | 6 | 12  |
| 11n-52m-COST239   | 11 |  52 | 0.47 | 8 | 12  |
| 14n-42m-NSF       | 14 |  42 | 0.23 | 4 | 8   |
| 14n-46m-DT        | 14 |  46 | 0.25 | 4 | 12  |
| 15n-46m-NSF       | 15 |  46 | 0.22 | 4 | 8   |
| 16n-46m-EURO      | 16 |  46 | 0.19 | 4 | 8   |
| 19n-76m-EON19     | 19 |  76 | 0.22 | 4 | 12  |
| 20n-62m-ARPANet   | 20 |  62 | 0.16 | 6 | 8   |
| 20n-78m-EON20     | 20 |  78 | 0.21 | 4 | 14  |
| 21n-70m-Spain     | 21 |  70 | 0.17 | 4 | 8   |
| 21n-72m-Italian   | 21 |  72 | 0.17 | 4 | 12  |
| 21n-78m-UKNet     | 21 |  78 | 0.19 | 4 | 14  |
| 22n-70m-BT        | 22 |  70 | 0.15 | 6 | 8   |
| 24n-86m-UBN24     | 24 |  86 | 0.16 | 4 | 10  |
| 28n-68m-EON       | 28 |  68 | 0.09 | 4 | 8   |
| 28n-82m-EURO28    | 28 |  82 | 0.11 | 4 | 10  |
| 30n-112m-Spain    | 30 | 112 | 0.13 | 6 | 10  |
| 43n-176m-Euro     | 43 | 176 | 0.10 | 4 | 12  |

A particularity of this type of network is that most of them are representable by strongly connected planar graphs. This fact makes sense if we think that such a structure is more fault tolerant.

In order to get an instance for RSA, besides the topology, we must define the maximum amount of available slots per arc and the set of demands, given as the number of slots that each demand needs, as well as their sources and destinations. From the literature we obtained some real data used when the RSA problem is studied:

  - The slot bandwith, in most of the cases, is 12.5 GHz according to the ITU recommendation. However it could be smaller (sometimes 6.5 GHz) or larger (25 Ghz), but not much larger, due to the fact that for RWA with WDM, the minimum bandwidth of the wavelenght is 50 GHz, and the main objective of RSA is to improve granularity.
  - The bandwidth of the optical fiber used on average is 4800 GHz, (although the theoretical maximum bandwidth of the optical fiber is around 231 THz).
  - We can have up to 3200 slots in a 5THz spectrum using 6.25 GHz slots.
  - The arc capacity _s*_ is normaly fixed in range [170, 320].
  - The amount of demands |_D_| is normaly in the range [10,100] except for some outliers that use 552, or even a thousand. But these large values are used for heuristic experimentations.
  - The volume needed by each demand _d &isin; D_ usually belongs to the range [1,20], but it depends on the value of s*.
\end{itemize}

## Generating the instances
The generator uses two different definitions to the term _density_, namely,

  - __Arcs-density__: amount of links of the topology over a complete graph.
  - __Demands-Density__: Relation between the maximum volume required by the demands and the arc capacity, i.e., _s*_.

To calculate the arcs-density for each topology, we interpret it as a directed graph _G = (V, E)_, which is the natural way, even though there are several works that assume symmetrical demands using the same spectrum, thus simplifying the number of edges in half by using undirected graphs.

The arcs-density of a graph _G_, called as _&Delta;(G)_, then is calculated as

<img src="https://latex.codecogs.com/svg.latex?\Delta(G)=\frac{|E|}{|V|(|V|-1)}." title="\Delta(G)=\frac{|E|}{|V|(|V|-1)}." />

Let _i_ be an instance for RSA and let _D<sub>i</sub>_, _s*<sub>i</sub>_ and _v<sub>i</sub> : D &#8594; &Nopf;_ be the demands set, the arcs capacity and the function that receives a demand and returns its volume, respectively. We define

<img src="https://latex.codecogs.com/svg.latex?maxSD_i=\max_{d\in%20D_i}v_i(d)," title="maxSD_i = \max_{d\in D_i} v_i(d)," />

as the maximum volume required by all the demands for a given instance _i_. In order to generate each instance, the script, in addition to _s*_ and the topology _G=(V,E)_, receives a real parameter _p &isin; (0,1]_ used to calculate

<img src="https://latex.codecogs.com/svg.latex?maxSD=p\times%20s^*," title="maxSD = p\times \bar s,"/>

in such a way that each demand uses a random number in 

<img src="https://latex.codecogs.com/svg.latex?[\frac{1}{2}maxSD,~maxSD]," title="\frac{1}{2}maxSD,~maxSD"/> 

and an optional factor _F_ to limit the number of demands, namely,

<img src="https://latex.codecogs.com/svg.latex?|D|=\frac{2\times%20F\times(|V|-1)\times\Delta(G)\times%20s^*}{maxSD}," title="|D| = \frac{2\times F \times (|V| - 1) \times \Delta(G) \times \bar s}{maxSD},"/>

with _&Delta;(G)_ the __arc-density__ of the graph _G_ and _F = 1_ by default.

The source and destination of each demand is randomly selected taking two nodes of the graph. We allow multiple demands for the same pair source destination depending on a parameter passed by the user.

## The Script
In this section we present the characteristics of the software developed as well as the way to execute it, its scripts, directories, parameters and its input and output files. 

### Files
The main scrip called **instances_generator.py** reads the topologies stored in the __topologies/__ directory and generates a serie of instances files for the RSA for each topology based on the data of the literature. It depends on the modulation level the optical fiber used, the graph density among other paramters.

### Data Format
The format of the data is commented in the header of each file. The separator used is the tabulation, and the line starting with # is a comment.
#### Topology
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

#### Generated Instance
As well as the problem is stated over directed graphs and due to the way in which the networks are made we asume all the links have both senses.

The instance file also begins with a header that briefly explains the format. The version of this software and the used seed are shown there. The number of slots available for each edge and the number of demands requested are shown below followed by the list of demands.
```
# Comment
s*     |D|
<src d1>    <dst d1>      <n of slots required by d1>
<src d2>    <dst d2>      <n of slots required by d1>
...
```

### Usage
#### Requirements
The requirements are stored in `requirements.txt`. They can be installed via

```
pip install -r requirements.txt
```

#### Run
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
  -mdir MDIR            The main directory or path. If no tdir or idir parameters are used, mdir must contain the 'topologies' and/or 'instances' folder. The
                        default value is the location of this script
  -tdir TDIR            The topologies directory or path.
  -idir IDIR            The directory or path for the created instances.
  -s SEED, --seed SEED  The random seed. Default is 1988.
  -S SLOTS [SLOTS ...], --slots SLOTS [SLOTS ...]
                        List of amounts of available slots.
  -p PERCENTS [PERCENTS ...], --percents PERCENTS [PERCENTS ...]
                        List of maximum percentage of total available slots that a demand can use. Must be in (0, 1].
  -d DENSITY, --density DENSITY
                        Density factor. The maximum amount of demands is multiplied by this factor. Default is 1.0
  -m, --multiple        If set, multiple demands between a source and a destination are allowed.
```

#### Example
The following line will generate instances for S in [10, 25] and p in [10%, 20%, 30%, 50%]. They will be saved in `./instances/`.

```
python instances_generator.py -S 10 25 -p .1 .3 .5 .2
```

This one will generate instances with S in [10, 15, 20, 30, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000] and p in [10%, 20%, 30%, ..., 90%] in the directory `/home/instances`, allowing multiple demands between each pair (src, dst).

```
python instances_generator.py -idir /home/instances -m
```

## References
[[1]](https://link.springer.com/article/10.1007/s11750-018-0483-6) Bertero, F., M. Bianchetti, and J. Marenco, _Integer programming models for the routing and spectrum allocation problem_, TOP __26__ (2018), 465–488.

[[2]](https://arxiv.org/abs/2106.15454) Bianchetti M. and J. Marenco, _Valid inequalities and a branch-and-cut algorithm for the Routing and Spectrum Allocation problem_, Electronic Notes in Theoretical Computer Science (_in press_)
