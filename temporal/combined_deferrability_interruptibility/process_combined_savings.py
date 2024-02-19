import pandas as pd 
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir

mode = "absolute_slack"
slack_list = [24*365, 24]
job_length_list  = [1,6,12,24,48,96,168]


main_data_dir = f'../data_output/{mode}_2022_processed/abs'
main_save_to_dir = 'data_output'

new_mode_dir = f"{main_save_to_dir}/{mode}"
check_dir(new_mode_dir)

for slack in slack_list:

    combined_df = pd.DataFrame(columns=job_length_list,index=['defer', "interrupt"] )

    for job in job_length_list:
        abs_non_interrupt_file = f"{main_data_dir}/job_{job}/slack_{slack}/non_interrupt.csv" # savings -- the difference already accounted
        abs_interrupt_file = f"{main_data_dir}/job_{job}/slack_{slack}/interrupt.csv" # savings -- the difference already accounted
        abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"

        interrupt_df = pd.read_csv(abs_interrupt_file) # savings already calculated
        non_interrupt_df = pd.read_csv(abs_non_interrupt_file) # savings already calculated
        slack0_df = pd.read_csv(abs_slack0_file)  

        global_slack0_emissions = slack0_df.sum(axis=1)    
        global_non_interrupt_saved_emissions = non_interrupt_df.sum(axis=1)    
        global_interrupt_saved_emissions = interrupt_df.sum(axis=1)  

        non_interrupt_savings = global_non_interrupt_saved_emissions / global_slack0_emissions
        non_interrupt_savings *= 100 
        non_interrupt_savings_mean = non_interrupt_savings.mean() 

        interrupt_savings = global_interrupt_saved_emissions / global_slack0_emissions
        interrupt_savings *= 100 

        interrupt_savings_mean = interrupt_savings.mean() 
        if job == 1: 
            interrupt_savings_mean = 0 # floating point errors



        combined_df[job] = [non_interrupt_savings_mean, interrupt_savings_mean]
    combined_df.index.name = 'stats'

    save_file_name = os.path.join(new_mode_dir, f"slack_{slack}.csv")

    combined_df.to_csv(save_file_name)