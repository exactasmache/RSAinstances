# RSA instances
A repository to store several topologies and scripts to generate the instances for the RSA problem.

The main scrip called **instances_generator.py** reads the topologies stored in the topologies/ directory and generates a serie of instances files for the RSA for each topology based on the data of the bibliography. It depends on the modulation level the optical fiber used, the graph density among other paramters.

From the literature we got the next more commonly used data for the RSA problem:

    + The slot bandwith is between 5 and 12.5 GHz, but it could be greater. 50 GHz is the used on the WDM problem.

    + The slot bitrate is about 2.5 Gbps
    
    + The average optical fiber bandwidth is 4800 GHz despite the maximal optical fiber bandwith is around 231 THz.

We use that information to define the available number of slots per link, the maximal amount of slots used by each demand. This is stored in the variables:

    avaliable_S, max_slots_by_demand
    
In order to define the amount of demands of each instance we estimate an upper bound using the graph density, the number of slots per link and the average of slots by demand.

## Usage
  
To generate the instances just run the script:

    python instances_generator.py

The instances are going to be placed on a new folder called instances into the main directory. The format of the data is commented into the file. Each one of those files with its asociated topology are the input for the RSA problem.