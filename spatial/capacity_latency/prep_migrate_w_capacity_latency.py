import pandas as pd
import numpy as np
from copy import deepcopy
import sys
import os 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import format_df

shared_file_dir = os.path.join( '../..', 'shared_data')
combined_carbon_file = os.path.join( shared_file_dir, 'combined_carbon.csv')
latency_matrix_file = os.path.join( shared_file_dir, 'gcp_latency_matrix.csv')


latency_df = pd.read_csv(latency_matrix_file, index_col="origin").rename_axis(None)
carbon_df = pd.read_csv(combined_carbon_file)

year = 2022 
carbon_df = format_df.get_year_df(carbon_df, selected_year=year) # only for the selected year
all_region_mean = carbon_df.mean()


all_region  = list(all_region_mean.sort_values().index) # sort region from lowest to highest mean

all_origin = list(latency_df.columns)

zone_code_list_unsorted =  list(set(all_region).intersection(all_origin)) # all origin regions that we have the carbon trace 
zone_code_list = [z for z in all_region  if z in zone_code_list_unsorted]

# filter the latency matrix
latency_df = latency_df[zone_code_list]
latency_df = latency_df[latency_df.index.isin(zone_code_list)]

latency_limit_list = [i for i in range(50, 301, 50)]
latency_limit_list.insert(0,5)

idle_cap_list = [0,50, 99] #99% ~infinite capacity, since all jobs can move there
region_count = len(zone_code_list)
max_util = 100

allocation_df = pd.DataFrame(columns=idle_cap_list, index=latency_limit_list)

for idle_cap_percent in idle_cap_list: 
    for latency_lim in latency_limit_list: 

        idle_cap_decimal = idle_cap_percent/100

        # for each origin region
        base_work_per_dc = round(max_util * (1-idle_cap_decimal))  
        total_work = base_work_per_dc*region_count

        allocation = [base_work_per_dc]*region_count
  
        for origin_index, origin in enumerate(zone_code_list): 
            work_per_dc = deepcopy(base_work_per_dc)  
            origin_latency_list = latency_df[origin]
            origin_mean = all_region_mean.loc[origin]

            allowed_regions = origin_latency_list[origin_latency_list <= latency_lim] # allowed destination
            # dest_mean = all_region_mean.loc[allowed_regions.index].min()

            sorted_allowed_regions_mean = list(all_region_mean.loc[allowed_regions.index].sort_values().index)

            '''migrating job from one region to the other region'''
            for dest_index, dest in enumerate(sorted_allowed_regions_mean): 
                alloc_index = zone_code_list.index(dest)

                if allocation[alloc_index] <= max_util:
                    avail_alloc = max_util-allocation[alloc_index]

                    if work_per_dc >= avail_alloc: 
                        allocation[alloc_index] += avail_alloc
                        allocation[origin_index] -= avail_alloc
                        work_per_dc -= avail_alloc
                    else: 
                        allocation[alloc_index] += work_per_dc
                        allocation[origin_index] -= work_per_dc
                        work_per_dc -= work_per_dc
                
                if work_per_dc <= 0: 
                    break
        # the remaining work will stay at the last region
        if work_per_dc > 0:
            allocation[origin_index] = work_per_dc

        emissions = (allocation * all_region_mean.loc[zone_code_list])/total_work 
        # print(emissions)

        allocation_df.loc[latency_lim, idle_cap_percent] = emissions.sum()

print(allocation_df)
allocation_df.index.name = 'latency'
allocation_df.to_csv("emissions.csv")
