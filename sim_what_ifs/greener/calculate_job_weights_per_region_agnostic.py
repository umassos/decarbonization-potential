import pandas as pd 
import os 
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions

main_data_dir = 'data_output/temporal_shifting_v'
main_save_to_dir = 'data_output/processed_weighted_slack0'
check_dir(main_save_to_dir)

slack_list = [24*365]
job_length_list  = [1,6,12,24,48,96,168] 

l = len(job_length_list)

weight_dict = {

    'equal': [1/l] * l, 
    'gcp':  [2/100, 4/100, 4/100, 10/100, 5/100, 5/100, 70/100], 
    'azure': [0.4/100, 0.9/100, 0.9/100, 1.4/100, 1.3/100, 2/100, 93.1/100]
}


weight_mode_list = ['equal']

for weight_mode in weight_mode_list:    
    weight_list = weight_dict[weight_mode]

    members = regions.get_grouping_members('Global')
    main_slack_df = pd.DataFrame()
    for row, slack in enumerate(slack_list): 
        
        temp_slack_df = pd.DataFrame()
        for member in members:
            
            temp_job_df = pd.DataFrame()
            for w, job in enumerate(job_length_list): 
        

                abs_combined_file = f"{main_data_dir}/job_{job}/slack_{slack}/{member}_slack0.csv" # savings -- the difference already accounted
               

                combined_df = pd.read_csv(abs_combined_file)   

                region_mean = combined_df.mean()
                weighted_savings = (region_mean/job) * weight_list[w]
                temp_job_df[job] = weighted_savings

            temp_job_df = temp_job_df.sum(axis=1) # add the weights, /1 is redundant

            temp_slack_df[member] = temp_job_df

        file_path = os.path.join(main_save_to_dir, f'slack_{slack}.csv')

        temp_slack_df.index.name = 'multiplier'
        temp_slack_df.index = temp_slack_df.index.astype(int) 
        temp_slack_df.to_csv(file_path)
    