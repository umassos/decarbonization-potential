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
    slack_list = [24,24*7, 24*20,24*30, 24*365] # absolute slacks
else:
    modetag = f"proportional_slack_{year}"
    slack_list = [i for i in range(1,10+1)] # proportional slack, can change this

job_length_list  = [1,6,12,24,48,96,168] # can change this


save_to_dir = f"{main_output_dir}/{modetag}"
check_dir(save_to_dir)


def task(zone_code, job, slack, slackdir): 
    rolling_df = carbon_df[zone_code].rolling(job).sum().dropna().reset_index(drop=True)
    sorted_df = carbon_df[zone_code].sort_values()

    l = len(sorted_df) 

    non_interrupt = []
    interrupt = []
    slack_0 = []
    

    if slack != 24*365:
        inf = False
        ending = l-job
        if absolute:
            abs_slack = slack # absolute slack
        else: 
            abs_slack = int(slack*job) # proportional slack
    else: 
        inf = True
        abs_slack = slack
        ending  = len(sorted_df)


    for i in range(ending): 

        if inf:

            sorted_df = carbon_df[zone_code].iloc[i:abs_slack].sort_values().values
            rolling_df = carbon_df[zone_code].iloc[i:abs_slack].rolling(job).sum().dropna().reset_index(drop=True)
        else:
            lim = i+abs_slack+job
            sorted_df = carbon_df[zone_code].iloc[i:lim].sort_values().values
            rolling_df = carbon_df[zone_code].iloc[i:lim].rolling(job).sum().dropna().reset_index(drop=True)
   
        if len(sorted_df) < job: 
            break

        lowest_interrupt = sorted_df[:job].sum().round(decimals=2)
        lowest_non_interrupt = rolling_df.min().round(decimals=2)
        slack_0_val = rolling_df.loc[0]


        if lowest_interrupt > lowest_non_interrupt: 
     
            if slack_0_val != np.nan:
                print("error", zone_code, job, slack, lowest_non_interrupt, lowest_interrupt)

        non_interrupt.append(lowest_non_interrupt)
        interrupt.append(lowest_interrupt)
        slack_0.append(slack_0_val)

    df = pd.DataFrame()

    df["slack_0"] = slack_0
    df["non_interrupt"] = non_interrupt
    df["interrupt"] = interrupt

    filename = f"{slackdir}/{zone_code}.csv"
    df.to_csv(filename,index=False)


# zone_code_list = ['SE-SE1']
if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        for job in job_length_list: 
            jobdir = f"{save_to_dir}/job_{job}"
            check_dir(jobdir)
            for slack in slack_list:
                slackdir = f"{jobdir}/slack_{slack}"
                check_dir(slackdir)
                for zonecode in zone_code_list: 
                    print("Running...", zonecode, job,slack,)
                    executor.submit(task, zonecode, job,slack, slackdir)


