## Carbon Savings Upper Bound Analysis

### Virtual Environment

To install the requirements ```pip install -r requirements.txt```

****

### Raw Data Sources 
* **Carbon Intensity**: https://www.electricitymaps.com/data-portal 

* **Google Latency**: https://lookerstudio.google.com/reporting/fc733b10-9744-4a72-a502-92290f608571/page/p_854mo2jmcd

* **Google Trace**: https://blog.research.google/2010/01/google-cluster-data.html
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
[temporal](temporal): deferrability, interruptibility, combined deferrability and interruptibility, weighted job leghts, vary slack <br>
[temporal_spatial_combined](temporal_spatial_combined): combined savings for temporal and spatial*

More details about the experiments are described in their respective diretories.
****

### Non-Experiment Directories 
[prep_rawdata](prep_rawdata): Prepare raw data for analyses and experiments <br>
[shared_data](shared_data): A directory that has files that are shared across multiple experiments <br>
[global_modules](global_modules): Contains helper functions, flag images, and fonts

