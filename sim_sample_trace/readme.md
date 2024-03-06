## Sample Trace Analysis
### Sample Carbon Trace
Required file: Sample carbon intensity signal 

[sample_carbon_trace](sample_trace/sample_carbon_trace.py): Plots sample carbon trace

### Energy Mix
Required file: Raw carbon intensity signal from Electricity Maps. We plot the energy mix of the year 2022. The zone codes for the sample regions are:

```
"CA-ON", 
"US-CAL-CISO", 
"AU-VIC", 
"IN-MH"
```

The energy mix for all 123 regions are provided in the ```data_output``` directory. 

This analysis involves selecting the regions to plot using the ```plot_energy_mix.py``` script from the data in ```data_output```. The plot output will be in the ```plot_output``` directory.

**Please contact Electricity Maps to collect raw carbon intensity with energy mix.**
