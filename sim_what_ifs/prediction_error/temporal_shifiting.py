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

data_dir = 'data_output/added_error'
save_to_dir = 'data_output/temporal_shifting'
check_dir(save_to_dir)


slack_list = [ 365*24] 
job_length_list  = [1,6,12,24,48,96,168] # can change this

def task( df, zone_code ,job, slack, slackdir): 

    columns = df.columns
    combined_non_interrupt_df = pd.DataFrame(columns = columns)
    combined_interrupt_df = pd.DataFrame(columns = columns)

    real_trace = df.iloc[:, 0]

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

        # non_interrupt = []
        # interrupt = []

        savings_diff_interrupt_list = []
        savings_diff_non_interrupt_list = []
        for i in range(ending): 

            if inf:
                lim = abs_slack
            else:
                lim = i+abs_slack+job
            error_sorted_df = selected_df.iloc[i:lim].sort_values().values
            error_rolling_df = selected_df.iloc[i:lim].rolling(job).sum().dropna().reset_index(drop=True)
            
            real_sorted_df = real_trace.iloc[i:lim].sort_values().values
            real_rolling_df = real_trace.iloc[i:lim].rolling(job).sum().dropna().reset_index(drop=True)
            
            if len(error_sorted_df) < job: 
                break

            # accounting
            error_lowest_non_interrupt = error_rolling_df.min(numeric_only=True)
            error_non_interrupt_index = error_rolling_df[error_rolling_df == error_lowest_non_interrupt].index.values[0]
            accounted_non_interrupt = real_rolling_df.iloc[error_non_interrupt_index]
            
            interrupt_index = selected_df.iloc[i:lim].sort_values()[:job].index
            accounted_interrupt = real_trace.iloc[interrupt_index].sum().round(decimals=2)
            

            # actual scheduling 
            actual_lowest_interrupt = real_sorted_df[:job].sum().round(decimals=2)
            actual_lowest_non_interrupt = real_rolling_df.min().round(decimals=2)

            savings_diff_interrupt = (accounted_interrupt - actual_lowest_interrupt)/ actual_lowest_interrupt
            savings_diff_non_interrupt = (accounted_non_interrupt - actual_lowest_non_interrupt)/ actual_lowest_non_interrupt

            if savings_diff_interrupt < 0: 
                savings_diff_interrupt = 0 


            if savings_diff_non_interrupt < 0: 
                savings_diff_non_interrupt = 0 

            savings_diff_interrupt_list.append(savings_diff_interrupt)
            savings_diff_non_interrupt_list.append(savings_diff_non_interrupt)

        combined_interrupt_df[c] = savings_diff_interrupt_list
        combined_non_interrupt_df[c] = savings_diff_non_interrupt_list


    combined_interrupt_df *= 100
    combined_non_interrupt_df *= 100


    filename_interrupt = f"{slackdir}/{zone_code}_interrupt.csv"
    filename_non_interrupt = f"{slackdir}/{zone_code}_non_interrupt.csv"
    combined_interrupt_df.to_csv(filename_interrupt,index=False)
    combined_non_interrupt_df.to_csv(filename_non_interrupt,index=False)

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
                    df = pd.read_csv(absfile).astype(float)

                    print("Running...", zone_code, job,slack,)
                    executor.submit(task, df,  zone_code, job,slack, slackdir)
