import pandas as pd 
import os
import sys

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "..", "global_modules")
sys.path.append(global_module)

import format_df
import regions

year = 2022
zone_code_list = regions.get_year_order()

combined_carbon_file = os.path.join( '..', 'shared_data/combined_carbon.csv')
carbon_df = pd.read_csv(combined_carbon_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=year)[zone_code_list]

temporal_data_dir = f'../temporal/data_output/absolute_slack_{year}_processed/abs'
save_to_dir = 'data_output'

job = 1 # can change this
slack_list = [24*365, 24] # can change this

for slack in slack_list:

    temporal_saving_file = f"{temporal_data_dir}/job_{job}/slack_{slack}/combined.csv"
    temporal_slack0_file = f"{temporal_data_dir}/job_{job}/slack_{slack}/slack0.csv"
    temporal_saving_df = pd.read_csv(temporal_saving_file)
    temporal_slack0_df = pd.read_csv(temporal_slack0_file)

    global_baseline = temporal_slack0_df.mean().mean()

   


    data_df = pd.DataFrame(index=["Spatial", "Temporal", "Net"], columns=zone_code_list)
    for dest in zone_code_list: 
        temporal_savings = temporal_saving_df[dest]# additional temporal savings from the destination region
    
        spatial_savings = carbon_df.subtract(carbon_df[dest],axis=0)
        spatial_savings = spatial_savings.iloc[:len(temporal_savings)]

        combined_savings = spatial_savings.add(temporal_savings, axis=0)

        mean_spatial_savings = (spatial_savings/global_baseline)*100
        mean_temporal_savings = (temporal_savings/global_baseline)*100
        mean_combined_savings = (combined_savings/global_baseline)*100

        mean_spatial_savings = mean_spatial_savings.mean().mean()
        mean_temporal_savings = mean_temporal_savings.mean().mean()
        mean_combined_savings = mean_combined_savings.mean().mean()


        data_df[dest] = [mean_spatial_savings, mean_temporal_savings, mean_combined_savings]

    savename = f"{save_to_dir}/slack_{slack}.csv"

    data_df.index.name = 'data'
    data_df.to_csv(savename)


        