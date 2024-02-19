## Trace Analysis
1. Calculate
2. Plot
***
### Mean and CV 
Required file: Carbon intensity signal from Electricity Maps

[calculate_mean_and_cv](mean_and_cv/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data``` directory. <br>
[plot_mean_and_cv](mean_and_cv/plot_mean_and_cv.py): Plots yearly mean and daily CV.

****
### Change Over Time
Required file: Carbon intensity signal from Electricity Maps

[calculate_mean_and_cv](mean_and_cv/calculate_mean_and_cv.py): Calculates daily CV and yearly mean from year 2020-2022 and store the calculation ```data``` directory. <br>
[plot_mean_and_cv](mean_and_cv/plot_change_overtime.py): Plots the change and carbon intensity and daily CV from 2020-2022.

***
### Periodicty Score
Required file: Periodicity score 

The periodicity score of the trace can be calculated using https://azure.microsoft.com/en-us/products/data-explorer. The score is derived from azure's ```series_peroids_detect()```

[periodicity_score](periodicity/periodicity_score.py): Plots the periodicity scores with country flags.
