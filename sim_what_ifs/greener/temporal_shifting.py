import pandas as pd 
import numpy as np
import os 
import sys 
import concurrent.futures
currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)


from check_dir import check_dir
import regions 

data_dir = 'data_output/added_renewables'
save_to_dir = 'data_output/temporal_shifting'
check_dir(save_to_dir)


slack_list = [365*24] 
job_length_list  = [1,6,12,24,48,96,168] # can change this

def task( df, zone_code ,job, slack, slackdir): 

    columns = df.columns 

    combined_interrupt_df = pd.DataFrame(columns = columns)
    combined_slack0_df = pd.DataFrame(columns = columns)

    for c in columns:
        selected_df = df[c]

        l = len(selected_df) 
        if slack != 24*365:
            inf = False
            ending = l-job
        else: 
            inf = True
            ending  = l

        abs_slack = slack

        non_interrupt = []
        interrupt = []
        slack0 = []
        for i in range(ending): 


            # print(rolling_df)
            if inf:

                sorted_df = selected_df.iloc[i:abs_slack].sort_values().values
                rolling_df = selected_df.iloc[i:abs_slack].rolling(job).sum().dropna().reset_index(drop=True)
            else:
                lim = i+abs_slack+job
                sorted_df = selected_df.iloc[i:lim].sort_values().values
                rolling_df = selected_df.iloc[i:lim].rolling(job).sum().dropna().reset_index(drop=True)
    
            if len(sorted_df) < job: 
                break

            lowest_interrupt = sorted_df[:job].sum().round(decimals=2)
            lowest_non_interrupt = rolling_df.min().round(decimals=2)
            slack_0_val = rolling_df.loc[0]

            if lowest_interrupt > lowest_non_interrupt: 
     
                if slack_0_val != np.nan:
                    print("error", zone_code, job, slack, lowest_non_interrupt, lowest_interrupt)

            interrupt_savings = lowest_interrupt
            interrupt.append(interrupt_savings)
            slack0.append(slack_0_val)


        combined_interrupt_df[c] = interrupt
        combined_slack0_df[c] = slack0

    filename_combined = f"{slackdir}/{zone_code}_combined.csv"
    filename_slack0 = f"{slackdir}/{zone_code}_slack0.csv"

    combined_interrupt_df.to_csv(filename_combined,index=False)
    combined_slack0_df.to_csv(filename_slack0,index=False)
    # print(filename)

files = os.listdir(data_dir)


if __name__ == "__main__":
    with concurrent.futures.ProcessPoolExecutor(max_workers=50) as executor:
        
        for job in job_length_list: 
            jobdir = f"{save_to_dir}/job_{job}"
            check_dir(jobdir)
            for slack in slack_list:
                slackdir = f"{jobdir}/slack_{slack}"
                check_dir(slackdir)

                for file in files:
                    zone_code = file[:-4]
                    absfile = os.path.join(data_dir, file )
                    df = pd.read_csv(absfile).astype(float).ffill().bfill()




            # task(df,  zone_code, job,slack, slackdir)
                # for zonecode in zone_code_list: 
                    print(zone_code, job, slack)
                    executor.submit(task, df,  zone_code, job,slack, slackdir)
