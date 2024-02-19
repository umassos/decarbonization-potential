import pandas as pd 
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
job_length_list  = [1,6,12,24,48,96,168]

main_data_dir = f'../data_output/{mode}_2022_processed/abs'
main_save_to_dir = 'data_output'

new_mode_dir = f"{main_save_to_dir}/{mode}"
check_dir(new_mode_dir)

zone_code_list = regions.get_year_order()
groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]

for slack in slack_list:


    savings_df = pd.DataFrame(columns=groupings, index=job_length_list)

    for job in job_length_list:
        
        abs_interrupt_file = f"{main_data_dir}/job_{job}/slack_{slack}/interrupt.csv" # savings -- the difference already accounted
        abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"
        interrupt_df = pd.read_csv(abs_interrupt_file)
        slack0_df = pd.read_csv(abs_slack0_file)    

        global_slack0_emissions = slack0_df.sum(axis=1)   
        global_baseline = slack0_df.mean().mean()


        for grouping in groupings: 
            members = regions.get_grouping_members(grouping)

            member_slack0_emissions = slack0_df[members].sum(axis=1)
            member_interrupt_saved_emissions = interrupt_df[members].sum(axis=1)

            member_interrupt_savings =  interrupt_df[members].mean()
            member_interrupt_savings /=  global_baseline
            member_interrupt_savings *= 100
           


            mean_interrupt_savings = member_interrupt_savings.mean()
        
            savings_df.loc[job, grouping] = mean_interrupt_savings


    save_file_name = os.path.join(new_mode_dir, f"slack_{slack}.csv")

    savings_df.index.name = 'job'
    savings_df.to_csv(save_file_name)