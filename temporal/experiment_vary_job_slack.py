import pandas as pd
import numpy as np
import os 
import sys 
import concurrent.futures

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "..", "global_modules")
sys.path.append(global_module)

import format_df
from check_dir import check_dir

combined_carbon_file = os.path.join( '..', 'shared_data/combined_carbon.csv')
main_output_dir = 'data_output'
year = 2022
carbon_df = pd.read_csv(combined_carbon_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=year) # only for the selected year

zone_code_list = list(carbon_df.columns)


absolute = True # if then proportional slack

if absolute:
    modetag = f"absolute_slack_{year}"
    # slacklist = [24,24*7, 24*20,24*30,24*365] # absolute slack
    slacklist = [24*365] # absolute slack
else:
    modetag = f"proportional_slack_{year}"
    slacklist = [i for i in range(1,10+1)] # proportional slack

joblengthlist  = [1,6,12,24,48,96,168]

save_to_dir = f"{main_output_dir}/{modetag}"
check_dir(save_to_dir)


def task(zone_code, job, slack, slackdir): 
    rolling_df = carbon_df[zone_code].rolling(job).sum().dropna().reset_index(drop=True)
    sorted_df = carbon_df[zone_code].sort_values()
    
    l = len(rolling_df) 
    
    non_interrupt = []
    interrupt = []
    slack_0 = []
    
    if absolute:
        abs_slack = slack # absolute slack
    else: 
        abs_slack = int(slack*job) # proportional slack

    if abs_slack < l:
        ending = l-abs_slack
    else: 
        ending = l # for the one-year slack case
    for i in range(ending): 
        deadline = abs_slack + job
        
        rangelist = [j for j in range(i, i+deadline)]
        rangelist_rolling = [k for k in range(i, i+abs_slack)] 
        interrupt_slots = sorted_df[sorted_df.index.isin(rangelist)]
        rolling_slots = rolling_df[rolling_df.index.isin(rangelist_rolling)] 
        lowest_interrupt = interrupt_slots[:job].reset_index(drop=True).sum().round(decimals=2)

        lowest_non_interrupt = rolling_slots.min().round(decimals=2)
        slack_0_val = rolling_df.loc[i]

        if lowest_interrupt > lowest_non_interrupt: 
     
            if slack_0_val != np.nan:
                print("error", zone_code, job, slack, lowest_non_interrupt, lowest_interrupt)
                   
        sorted_df  = sorted_df.drop(index=[i])
        rolling_df = rolling_df.drop(index=[i]) 

        non_interrupt.append(lowest_non_interrupt)
        interrupt.append(lowest_interrupt)
        slack_0.append(slack_0_val)

        df = pd.DataFrame()
    df["slack_0"] = slack_0
    df["non_interrupt"] = non_interrupt
    df["interrupt"] = interrupt

    filename = f"{slackdir}/{zone_code}.csv"
    df.to_csv(filename,index=False)
    print(filename)

if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        for job in joblengthlist: 
            jobdir = f"{save_to_dir}/job_{job}"
            check_dir(jobdir)
            for slack in slacklist:
                slackdir = f"{jobdir}/slack_{slack}"
                check_dir(slackdir)
                for zonecode in zone_code_list: 
                    executor.submit(task, zonecode, job,slack, slackdir)
