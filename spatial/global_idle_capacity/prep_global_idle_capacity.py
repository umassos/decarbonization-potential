import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import format_df
import regions

combined_carbon_file = os.path.join( '../..', 'shared_data/combined_carbon.csv')

year = 2022

zone_code_list =  regions.get_year_order(year)
carbon_df = pd.read_csv(combined_carbon_file)
carbon_df = format_df.get_year_df(carbon_df) # only for the selected year
carbon_df = carbon_df[zone_code_list] 

all_region_mean = carbon_df.mean()


idle_cap_list = [i for i in range(0, 100, 10)]
idle_cap_list.append(99)

region_count = len(zone_code_list)
base_work_per_dc = len(zone_code_list)

allocation_df = pd.DataFrame(index=zone_code_list)

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
    emissions = (allocation * all_region_mean)/np.sum(allocation)

    allocation_df[idle_cap_percent] = emissions

allocation_df.index.name = 'zonecode'
allocation_df.to_csv("emissions.csv")