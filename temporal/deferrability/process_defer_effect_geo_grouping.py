import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions

year = 2022

mode = "absolute_slack"
slack_list = [24*365, 24]


job_length_list = [1,6,12,24,48,96,168]

main_data_dir = f'../data_output/{mode}_2022_processed/abs'
main_save_to_dir = 'data_output'

new_mode_dir = f"{main_save_to_dir}/{mode}"
check_dir(new_mode_dir)

zone_code_list = regions.get_year_order()
groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]

for slack in slack_list:


    savings_df = pd.DataFrame(columns=groupings, index=job_length_list)

    for job in job_length_list:
        
        abs_non_interrupt_file = f"{main_data_dir}/job_{job}/slack_{slack}/non_interrupt.csv" # savings -- the difference already accounted
        abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"
        non_interrupt_df = pd.read_csv(abs_non_interrupt_file)
        slack0_df = pd.read_csv(abs_slack0_file)    

        global_slack0_emissions = slack0_df.sum(axis=1)   
        global_baseline = slack0_df.mean().mean()


        for grouping in groupings: 
            members = regions.get_grouping_members(grouping)

            member_slack0_emissions = slack0_df[members].sum(axis=1)
            member_defer_saved_emissions = non_interrupt_df[members].sum(axis=1)

            member_defer_savings =  non_interrupt_df[members].mean()
            member_defer_savings /=  global_baseline
            member_defer_savings *= 100
           


            mean_defer_savings = member_defer_savings.mean()
        
            savings_df.loc[job, grouping] = mean_defer_savings


    save_file_name = os.path.join(new_mode_dir, f"slack_{slack}.csv")

    savings_df.index.name = 'job'
    savings_df.to_csv(save_file_name)