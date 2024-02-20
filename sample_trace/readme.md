## Trace Analysis
### Sample Carbon Trace
Required file: Sample carbon intensity signal 

[sample_carbon_trace](sample_trace/sample_carbon_trace.py): Plots sample carbon trace
### Energy Mix
Required file: Raw carbon intensity signal from Electricity Maps. The zone codes for the sample regions are and we plot the energy mix of the year 2022 
```
"CA-ON", 
"US-CAL-CISO", 
"AU-VIC", 
"IN-MH"
```
This analysis involves two steps:
1. Calculate: run the  ```calculate_energy_mix.py``` script to process the data. The calculated values from the experiment is stored in the ```data_output``` directory.
2. Plot: run the  ```plot_energy_mix.py``` script to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.
