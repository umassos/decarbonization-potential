## Temporal

Each sub-directories are individual simulations. To run each simulation go to the sub-directory by 
```
cd <sub diretory name>
```

Each simulation involves two steps:


1. Experiment: [experiment_vary_job_slack.py](experiment_vary_job_slack.py). Change ```slack_list``` and ```job_length_list``` for different job lengths and slacks. Required Combined carbon file from [process_raw_data](../process_raw_data). 

2. Process experiment results: [process_vary_job_slack_data.py](process_vary_job_slack_data.py). 

The outputs from 1 and 2 are in [data_output](data_output) directory. 


3. Calculate and plot different dimensions in the subdirectories (i.e.run the script inside each directory).

***
### Sub-directories
All the experiments Required file: from 2.

to run the script type ```python3 <file_name>.py```

Each experiment involves two steps:
1. Calculate: run the script starts with ```calculate``` to process the data from 2. The calculated values from the experiment is stored in the ```data_output``` directory.
2. Plot: run the script starts with ```plot``` to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.


### Weighted Job Length
* Require an additional data: the weights for each job length based on the workload trace 
* **Google Trace**: https://github.com/google/cluster-data, the weights for Google trace in our experiment was based on Google cluster trace 3 --  from [Borg: the next generation](https://dl.acm.org/doi/10.1145/3342195.3387517) and [Take it to the limit: peak prediction-driven resource overcommitment in datacenters](https://dl.acm.org/doi/10.1145/3447786.3456259).
* **Azure Trace**: https://github.com/Azure/AzurePublicDataset
* Depending on the work load trace, you are unlikely to get the exact same results as the paper.