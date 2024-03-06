## Spatial

Each sub-directories are individual simulations. To run each simulation go to the sub-directory by 
```
cd <sub diretory name>
```

Each simulation involves two steps:
1. Calculate: run the script starts with ```calculate``` to process the data. The calculated values from the experiment is stored in the ```data_output``` directory.
2. Plot: run the script starts with ```plot``` to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.

Required files can be procssed using the scripts in [prep_rawdata](../prep_rawdata) and are stored in [shared_rawdata](../shared_rawdata)

### Capacity and Latency
* Required files: Combined carbon file and processed GCP latency matrix 
* Change ```idle_cap_list``` variable in for [calculate_capacity_latency.py](capacity_latency/calculate_capacity_latency.py) for different idle capacities.


### Global Idle Capacity
* Required files: Combined carbon file
* Change ```idle_cap_list``` variable in for [calculate_capacity.py](global_idle_capacity/calculate_capacity.py) for different idle capacity.

### Grouping Breakdown with Capacity

* Required files: Combined carbon file
* Change ```idle_cap_list``` variable in for [calculate_capacity.py](geo_grouping_capacity/calculate_capacity.py) for different idle capacity.

Note that Global Idle Capacity and Grouping Breakdown with Capacity have the same experiment, but the experiment file is provided in both subdirectories.

### One and Infinite Migration
* Required files: Combined carbon file