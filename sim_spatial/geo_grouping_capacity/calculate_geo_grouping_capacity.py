import pandas as pd
import numpy as np
import sys
import os 


currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import format_df

combined_carbon_file = os.path.join( '../..', 'shared_data/combined_carbon.csv')

year = 2022 
carbon_df = pd.read_csv(combined_carbon_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=year) # only for the selected year

all_region_mean = carbon_df.mean()
all_region_mean  = all_region_mean.sort_values() # sort region from lowest to highest mean

zone_code_list = all_region_mean.index
carbon_df = carbon_df[zone_code_list] 

allocation_df = pd.DataFrame(index=zone_code_list)

idle_cap_list = [0,50, 99] #99% ~infinite capacity, since all jobs can move there
region_count = len(zone_code_list)
base_work_per_dc = len(zone_code_list)
for idle_cap_percent in idle_cap_list: 
  
    allocation = np.zeros(region_count)

    idle_cap_decimal = idle_cap_percent/100
    work_per_dc = int(base_work_per_dc * (1-idle_cap_decimal))
    idle_cap_dc = int(base_work_per_dc * (idle_cap_decimal))

    total_work = work_per_dc * region_count

    allocation = np.zeros(region_count)
    counter = 0
    while total_work > 0: 
        if total_work >= base_work_per_dc: 
            allocation[counter] = base_work_per_dc
            total_work -= base_work_per_dc
        else: 
            allocation[counter] = total_work
            total_work -= total_work
        counter += 1
  
    # average emission per unit job in the
    emissions = (allocation * all_region_mean)/allocation

    allocation_df[idle_cap_percent] = emissions

allocation_df.index.name = 'zonecode'
allocation_df.to_csv("data_output/emissions.csv")


