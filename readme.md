## Carbon Savings Upper Bound Analysis
The aim of this repository is to provide the source code that reproduce the results of the following work: 

> Sukprasert, Thanathorn and Souza, Abel and Bashir, Noman and Irwin, David and Shenoy, Prashant, "On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting in the Cloud", in the 19th European Conference on Computer Systems (EuroSys)

We conduct a detailed trace-driven analysis to understand the benefits and limitations of spatiotemporal workload scheduling for cloud workloads with different characteristics, e.g., job duration, deadlines, SLOs, memory footprint, etc., based on hourly variations in energy's carbon-intensity over three years across 123 distinct regions, which encompass most major cloud sites. For more information, please refer to the paper.

***

### Configurations 
We run this experiment with 
* Ubuntu 20.04.6
* Python 3.8+

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
The following datasets are required to generate our results:

* **Carbon Intensity**: https://www.electricitymaps.com/data-portal: Our experiments use carbon intensity data from 123 regions worldwide. The 123 regions are list in [global_modules/static_files/name_stats.csv](../global_modules/static_files/name_stats.csv)

* **Google Latency**: https://lookerstudio.google.com/reporting/fc733b10-9744-4a72-a502-92290f608571/page/p_854mo2jmcd

* **Google Trace**: https://github.com/google/cluster-data (version 3)
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

The calculated result for each experiment will be stored in their own ```data_output``` directory and the plots of each calculated result will be stored in their own ```plot_output``` directory.

For example to *calculate* mean and CV: <br>
1. From the main directory, go to the *trace_analysis* directory by ```cd trace_analysis```
2. In the *trace_analysis* directory go to *mean_and_cv* directory by ```cd mean_and_cv```
3. In the *mean_and_cv* directory run ```python3 calculate_mean_and_cv.py``` to calculate mean and CV of the carbon intensity signal. 

****

### Non-Experiment Directories 
[prep_rawdata](prep_rawdata): Prepare raw data for analyses and experiments <br>
[shared_data](shared_data): A directory that has files that are shared across multiple experiments <br>
[global_modules](global_modules): Contains helper functions, flag images, and fonts

