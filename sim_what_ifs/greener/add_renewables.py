import pandas as pd 
from copy import deepcopy
import numpy as np
import math
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import format_df
from check_dir import check_dir

raw_data_dir = 'data_output/raw_mix'
emission_factor_file = 'data_output/emission_factors.csv'
save_to_dir = 'data_output/added_renewables'
check_dir(save_to_dir)

non_renewables = [
                "coal",
                "oil", 
                "gas",
                "biomass",
                "unknown",
                "nuclear",
              ]

renewables = [
            "solar", 
            "wind", 
            "hydro"
            ]

to_add_cols = [
            "solar", 
            "wind"
            ]


combined_source = non_renewables + renewables
combined_cols = [f"power_production_{s}_avg" for s in combined_source]
non_renewables_cols = [f"power_production_{s}_avg" for s in non_renewables]
to_add_cols = [f"power_production_{s}_avg" for s in to_add_cols]


ratio_list = [(i/100) for i in range(0, 100+1, 20)]


factor_df = pd.read_csv(emission_factor_file, index_col='zone_code')

files = os.listdir(raw_data_dir)

for file in files: 

    zone_code = file[:-4]
    absfile = os.path.join(raw_data_dir, file)

    zone_df = pd.read_csv(absfile)
    df = format_df.get_year_df(zone_df, selected_year=2022)

    new_df = pd.DataFrame()

    factor = factor_df.loc[zone_code]
    factor = pd.Series(factor)

    for ratio in ratio_list: 


        temp_df = pd.DataFrame()
        temp_df[combined_cols] = df[combined_cols].copy(deep=True)  #* 1000

        total_production = temp_df.sum(axis=1)

        new_renewables = total_production * ratio

        for index, row in temp_df.iterrows():

            original_sources = temp_df.loc[index, to_add_cols]
            original_non_renewable_sources = temp_df.loc[index, non_renewables_cols]

            # if it does not exist in the first place, don't add 
            # this is to account for no solar period and NaN sources
            original_sources = original_sources[original_sources > 0 ]
            original_non_renewable_sources  = original_non_renewable_sources[original_non_renewable_sources  > 0]

            to_add_sources = list(original_sources.index)
            source_count = len(to_add_sources)

            to_add_total = new_renewables.iloc[index]
          

            to_remove_sources = list(original_non_renewable_sources.index)

            to_remove_total = deepcopy(to_add_total)

            if source_count > 0:
                for source_index, s in enumerate(to_remove_sources): 

                    curr_val = deepcopy(temp_df.loc[index,s])
                    if curr_val >= to_remove_total:
                        temp_df.loc[index,s] -= to_remove_total
                        to_remove_total -= to_remove_total
                    else: 

                        temp_df.loc[index,s] -=  curr_val
                        to_remove_total -=  curr_val
                        
            
                    if to_remove_total == 0:

                        break

                to_add_total -= to_remove_total
                to_add_per_source = to_add_total / source_count
                temp_df.loc[index, to_add_sources] += to_add_per_source

        if total_production.sum() != temp_df.sum().sum(): 
            print(zone_code, total_production.sum(), temp_df.sum().sum())


        temp_df *= 1000
        temp_df.columns = temp_df.columns.str.replace("power_production_", "")
        temp_df.columns = temp_df.columns.str.replace("_avg", "")

        total_emissions =  (pd.Series(factor) * temp_df).sum(axis=1, numeric_only=True)

        total_production = temp_df.sum(axis=1, numeric_only=True)
        new_trace = total_emissions.divide( total_production)
    
        new_df[int(ratio*100)] = new_trace

    new_df = new_df.round(decimals=2)
    new_file = os.path.join(save_to_dir, f"{zone_code}.csv")
    new_df.to_csv(new_file, index=False)
    print(new_file)