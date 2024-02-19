## Temporal
1. Experiment: [experiment_vary_job_slack.py](experiment_vary_job_slack.py). Change ```slack_list``` and ```job_length_list``` for different job lengths and slacks. Required Combined carbon file from [prep_rawdata](../prep_rawdata). 

2. Process experiment results: [process_vary_job_slack_data.py](process_vary_job_slack_data.py). 

The outputs from 1 and 2 are in ```data_output```

3. Calculate and plot different dimensions in the subdirectories.
***
### Sub-directories
All Required file: from 2.
1. Calculate 
2. Plot


### Weighted Job Length
* Require an additional data: the weights for each job length based on the workload trace 
* **Google Trace**: https://blog.research.google/2010/01/google-cluster-data.html
* **Azure Trace**: https://github.com/Azure/AzurePublicDataset
