## Trace Analysis

Each analysis involves two main steps:
1. Calculate
2. Plot
***

### Mean and CV 
Required file: Combined carbon file: [../shared_data/combined_carbon.csv](../shared_data/combined_carbon.csv)

[calculate_mean_and_cv](mean_and_cv/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data_output``` directory. <br>
[plot_mean_and_cv](mean_and_cv/plot_mean_and_cv.py): Plots yearly mean and daily CV.

****
### Change Over Time
Required file: Combined carbon file: [../shared_data/combined_carbon.csv](../shared_data/combined_carbon.csv)

[calculate_mean_and_cv](mean_and_cv/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data``` directory. <br>
[plot_mean_and_cv](mean_and_cv/plot_change_overtime.py): Plots the change and carbon intensity and daily CV from 2020-2022.

***
### Periodicty Score
Required file: Periodicity score 

The periodicity score of the trace can be calculated using https://azure.microsoft.com/en-us/products/data-explorer. The score is derived from azure's ```series_peroids_detect()```. To obtain the periodicity score, put the whole-year carbon trace of a region to the ```series_peroids_detect()``` function.

[plot_periodicity_score](periodicity/plot_periodicity_score.py): Plots the periodicity scores with country flags.