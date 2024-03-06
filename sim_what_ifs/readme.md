## What-If Scenarios 
Each sub-directories are individual simulations. To run each simulation go to the sub-directory by 
```
cd <sub diretory name>
```

### Mixed Workloads
Required files: Combined carbon file
<br>
This simulation involves the following steps: 

1. Calculate the carbon reductions from mixed workloads: [calculate_mixed_workload.py](mixed_workloads/calculate_mixed_workload.py)
2. Process the calculation: [process_mixed_workload.py](mixed_workloads/process_mixed_workload.py)
2. Plot the results: [plot_mixed_workload.py](mixed_workloads/plot_mixed_workload.py)

### Prediction Error
Required files: Combined carbon file
<br>
This simulation involves the following steps: 

1. Add the error to the trace: [add_error.py](prediction_error/add_error.py)
2. Create a combined file for each error value: [combined_spatial_trace.py](prediction_error/combined_spatial_trace.py)
3. Run temporal shifting: [temporal_shifting.py](prediction_error/temporal_shifting.py)
4. Process temporal shifting results: [calculate_temporal.py](prediction_error/calculate_temporal.py)
5. Process spatial shifting results: [calculate_spatial.py](prediction_error/calculate_spatial.py)
6. Plot the results: [combined_spatial_trace.py](prediction_error/combined_spatial_trace.py)


### Increasing Renewable Penetration
Required files: Raw carbon intensity data file from Electricity Maps. **Please contact Electricity Maps for this or check out this [link](https://www.electricitymaps.com/research)**
<br>
This simulation involves the following steps: 

1. Create the emission factors for each region: [create_emission_factors.py](greener/create_emission_factors.py)
2. Add the renewables to the trace and recalculate the carbon intensity: [add_renewables.py](greener/add_renewables.py)
3. Create a combined file for each add renewable value: [combined_spatial_trace.py](greener/combined_spatial_trace.py)
4. Run temporal shifting: [temporal_shifting.py](greener/temporal_shifting.py)
5. Process temporal shifting results: [calculate_job_agnostic.py](greener/calculate_job_agnostic.py) and [calculate_job_aware.py](greener/calculate_job_aware.py)
6. Plot the results for temporal and spatial: [plot_temporal.py](greener/plot_temporal.py) and [plot_spatial.py](greener/plot_spatial.py)

### Spatial and Temporal Combined

This simulation involves the following steps: 
1. Calculate: run the [calculate_combined_savings.py](temporal_spatial_combined/calculate_combined_savings.py) script to process combined temporal and spatial effects. The calculated values from the experiment is stored in the ```data_output``` directory.
2. Plot: run the [plot_combined_savings.py.py](temporal_spatial_combined/plot_combined_savings.py) script to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.