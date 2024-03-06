import pandas as pd 
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

import regions

mode = "absolute_slack"
main_data_dir = f'../data_output/{mode}_2022_processed/abs'
main_save_to_dir = 'data_output'

slack_list = [24,24*7, 24*20,24*30,24*365]
job_length_list = [1,6,12,24,48,96,168]

groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]
combined_mean_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")

for slack in slack_list:
    for g in groupings: 

        members = regions.get_grouping_members(g)

        temp_job_df = pd.DataFrame()
        for job in job_length_list: 
            abs_combined_file = f"{main_data_dir}/job_{job}/slack_{slack}/combined.csv" # reductions -- the difference already accounted
            abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"
            
            combined_df = pd.read_csv(abs_combined_file)    
            slack0_df = pd.read_csv(abs_slack0_file) 

            group_savings = combined_df[members].mean().mean() / job
            mean_savings = (group_savings).mean()

            temp_job_df[job] = [mean_savings]

        combined_mean_df.loc[slack,g] = temp_job_df.mean().mean()

meanname = f"{main_save_to_dir}/emissions.csv"
combined_mean_df.to_csv(meanname)