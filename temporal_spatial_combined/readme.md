## Temporal and Spatial
1. Calculate 
2. Plot

* Required data output from [process_vary_job_slack_data.py](process_vary_job_slack_data.py) and combined carbon file from [prep_rawdata](../prep_rawdata). 

The experiment involves two steps:
1. Calculate: run the ```calculate_combined_savings.py``` script to process combined temporal and spatial effects. The calculated values from the experiment is stored in the ```data_output``` directory.
2. Plot: run the ```plot_combined_savings.py``` script to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.