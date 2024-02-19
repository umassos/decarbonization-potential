## Carbon Savings Upper Bound Analysis
The aim of this repository is to provide source code for to reproduce the results of the following work: 
***On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud***.
***

### Configurations 
We run this experiment with 
* Ubuntu 20.04.6
* Python 3.8.10

#### Python Modules 
* pandas
* numpy 
* scikit-learn
* matplotlib 
* seaborn

We generated [requirement.txt](requirement.txt) for the required python modules. <br>
We suggest to create a Python virtual environment and install modules inside of this virtual environment.

To install the requirements run ```pip install -r requirements.txt```

****

### Raw Data Sources 
* **Carbon Intensity**: https://www.electricitymaps.com/data-portal 

* **Google Latency**: https://lookerstudio.google.com/reporting/fc733b10-9744-4a72-a502-92290f608571/page/p_854mo2jmcd

* **Google Trace**: https://github.com/google/cluster-data 
* **Azure Trace**: https://github.com/Azure/AzurePublicDataset

****

### Raw Data Processing and Storing
[shared_data](shared_data) : All the **raw** and **processed** data are stored in this directory. The data is shared across multiple experiments. 

[prep_rawdata](prep_rawdata): To process raw **carbon intensity** and **latency** data.
***

### Experiment Directories 
[sample_trace](sample_trace): sample carbon intensity trace to show variation across time and regions and the regions' respective energy mix. <br>
[trace_analysis](trace_analysis): mean and cv, change over time, periodicity score <br>
[spatial](spatial): grouping breakdown, global idle capacity, capacity and latency, one and infinite migration <br>
[temporal](temporal): deferrability, interruptibility, combined deferrability and interruptibility, weighted job legths, vary slack <br>
[temporal_spatial_combined](temporal_spatial_combined): combined savings for temporal and spatial*

More details about the experiments are described in their respective diretories.

Note that for any experiment/plotting script the code should be **run inside** that directory.

To run any experiment, to go its directory and run
```python3 <file_name>```

****

### Non-Experiment Directories 
[prep_rawdata](prep_rawdata): Prepare raw data for analyses and experiments <br>
[shared_data](shared_data): A directory that has files that are shared across multiple experiments <br>
[global_modules](global_modules): Contains helper functions, flag images, and fonts

