## Trace Analysis

The **Mean and CV** and **Change Over Time** simulations involve two steps:
1. Calculate: run the script starts with ```calculate``` to process the data. The calculated values from the experiment is stored in the ```data_output``` directory.

2. Plot: run the script starts with ```plot``` to plot the data in ```data_output```. The plot output will be in the ```plot_output``` directory.

***

### Mean and CV 
Required file: Combined carbon file: [../shared_data/combined_carbon.csv](../shared_data/combined_carbon.csv)

[calculate_mean_and_cv](mean_and_cv/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data_output``` directory. <br>
[plot_mean_and_cv](mean_and_cv/plot_mean_and_cv.py): Plots yearly mean and daily CV.

****
### Change Over Time
Required file: Combined carbon file: [../shared_data/combined_carbon.csv](../shared_data/combined_carbon.csv)

[calculate_mean_and_cv](change_over_time/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data``` directory. <br>
[plot_change_over_time](change_over_time/plot_change_over_time.py): Plots the change and carbon intensity and daily CV from 2020-2022.

***
### Periodicity Score
Required file: Periodicity score 

The periodicity score of the trace can be calculated using https://azure.microsoft.com/en-us/products/data-explorer. The score is derived from azure's ```series_peroids_detect()```. To obtain the periodicity score, put the whole-year carbon trace of a region to the ```series_peroids_detect()``` function.

[plot_periodicity_score](periodicity/plot_periodicity_score.py): Plots the periodicity scores with country flags.