## Carbon Savings Upper Bound Analysis
The aim of this repository is to provide the code to reproduce the results of the following work: 

> Sukprasert, Thanathorn and Souza, Abel and Bashir, Noman and Irwin, David and Shenoy, Prashant, "On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud", in the 19th European Conference on Computer Systems (EuroSys)

In this work, we conduct a detailed trace-driven analysis to understand the benefits and limitations of spatiotemporal workload scheduling for cloud workloads with different characteristics, e.g., job duration, deadlines, SLOs, memory footprint, etc., based on hourly variations in energy's carbon-intensity over three years across 123 distinct regions, which encompass most major cloud sites. For more information, please refer to the paper.

***

### Requirements 

* Ubuntu 20.04+
* Python 3.8+

We have run this experiment with in the above setting. However, this codebase should work on any Unix based system with Python 3.8+ installed.

In addirion, we have generated a [requirements.txt](requirements.txt) for the required Python modules. <br>
We suggest you to create and load a Python [virtual environment](https://docs.python.org/3/library/venv.html) and install modules inside of this virtual environment.

#### Python Modules 
* pandas
* numpy 
* scikit-learn
* matplotlib 
* seaborn


## Getting Started

### 1. Creating Virtual Environment

In the direction that you want to run:

Create a virtual environment: 

```
python3 -m venv .venv
```

where the .venv is the name of the virtual environment 

To activate the virtual environment 
```
source .venv/bin/activate
```


To install the requirements 
```
pip3 install -r requirements.txt
```

To deactivate the virtual environment 
```
deactivate
```

### 2. Raw Data Sources

* **Carbon Intensity**: 
    * Downloading carbon intensity data: https://www.electricitymaps.com/data-portal
        1. To download the data for each region, select the region then select 'Get data'
        2. At the 'Year' filter, select the year 
        3. At the 'Interval' select ```hourly```
        4. To download the file for each zone in the region click the download button. 
        5. Enter the information and click 'Submit', the click 'Download data'
        6. Place the downloaded data in the [downloaded_carbon_data](downloaded_carbon_data) directory 
        7. Process the downloaded data in [process_raw_carbon_data](process_raw_carbon_data) directory 

    * Alternatively, the carbon intensity data from year 2020-2022 are provided in the [provided_data/combined_carbon.csv](provided_data/combined_carbon.csv) directory 

    * If the downloaded data is used, the processed data from the [process_raw_carbon_data/process_data.py](process_raw_carbon_data/process_data.py) directory will be saved to the [shared_data](shared_data) directory. 

    * Otherwise, copy the [provided_data/combined_carbon.csv](provided_data/combined_carbon.csv) to the [shared_data](shared_data) directory. 


* **Google Latency**: https://lookerstudio.google.com/reporting/fc733b10-9744-4a72-a502-92290f608571/page/p_854mo2jmcd (from the AT&T Center for Virtualization at Southern Methodist University)

* **Google Trace**: https://github.com/google/cluster-data (version 3)
* **Azure Trace**: https://github.com/Azure/AzurePublicDataset (V2)


### 3. Running Experiments

The directories that starts with ```sim_``` are the directories with different groups of simulations. 

The table below shows the directory names that start with ```sim```, their sub-directories that contain the simulations as well as the respective figures. 

| Main Simulation Diretory Name | Sub-directories | Figure(s) |
| :------------------------ | :-------------------------- | --------------: |
| sample_trace        |  carbon_trace, energy_mix  | 1(a)-(b) |
| trace_analysis       |  mean_and_cv, change_over_time, periodicity    | 3(a)-(b), 4 |
| spatial           | geo_grouping_capacity, global_idle_capacity, capacity_and_latency, one_and_infinite_migration   | 5(a)-(c), 6(a)-(b)|
| temporal    |  deferrability, interruptibility, deferrability and interruptibility combined, job_length_distribution, vary_slack    | 7(a)-(b), 8(a)-(b), 9(a)-(b), 10(a)-(b) |
| what_ifs |  mixed_workload, greener, temporal_spatial_combined  | 11(a)-(d), 12|




Each simulation is run **inside** its own sub-directory. 

To access the main simulation directory:

```
cd  sim_<directory name>
```

To access the simulation directory

```
cd <simulation sub-directotry name>
```

In the simulation directory, to run any script: 
```
python3 <file_name>
``` 

The calculated result for each simulation will be stored in their own ```data_output``` directory and the plots of each calculated result will be stored in their own ```plot_output``` directory.

For example to *calculate* mean and CV: <br>
1. From the main directory, go to the *trace_analysis* directory by 
```
cd sim_trace_analysis
```
2. In the *trace_analysis* directory go to *mean_and_cv* directory by 
```
cd mean_and_cv
```
3. In the *mean_and_cv* directory, to calculate mean and CV of the carbon intensity signal, run 
```
python3 calculate_mean_and_cv.py
``` 
### Other Sources 
* The [shared_data](shared_data) directory contains data that are sharedacross multiple experiments. 

* The flag images are from: https://github.com/gosquared/flags/blob/master/flags/flags-iso/flat/16/US.png



### License
* The Python codebase available in here follows the Apache v2 License unless otherwise stated.
* The *Google Latency* dataset has been created by the from the AT&T Center for Virtualization at the Southern Methodist University and follows the Apache v2 License.
* The *Electricity Maps Carbon Intensity* is made available under the Open Database License: http://opendatacommons.org/licenses/odbl/1.0/. Any rights in individual contents of the database are licensed under the Database Contents License: http://opendatacommons.org/licenses/dbcl/1.0/

