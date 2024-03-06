## Prep Raw Data
All the processed data is saved to [shared_data/combined_carbon.csv](../shared_data/combined_carbon.csv)
<br>

### Process Carbon Intensity Data
[combined_carbon.py](combined_carbon.py): 
* Required file: Raw Carbon intensity signal from Electricity Maps
* Clean up the raw data and extract the carbon intensity columns of all the regions and put all the carbon signals in one file for a year.
* Our experiments use carbon intensity data from 123 regions worldwide. The 123 regions are list in [global_modules/static_files/name_stats.csv](../global_modules/static_files/name_stats.csv)
<br>

[mean_order.py](mean_order.py): 
* Required file: Combined carbon file from [combined_carbon.py](combined_carbon.py)
* Order the region from lowest to highest carbon intensity for each year (2020-2022).
<br>

[mean_stats.py](mean_stats.py): 
* Required file: Combined carbon file from [combined_carbon.py](combined_carbon.py)
* Get mean from year 2020-2022

***

### Process Google Latency Matrix
[prep_latency_matrix.py](prep_latency_matrix.py): 

* Required file: Raw google latency matrix from https://lookerstudio.google.com/reporting/fc733b10-9744-4a72-a502-92290f608571/page/p_854mo2jmcd

* Process raw latency data and map the GCP datacenters to the Electricity Maps region using ```gcp_dc_zonecode_mapper.json```