import pandas as pd 
import statsmodels.stats.api as sms
import scipy.stats as st
import numpy as np
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions

weight_mode = 'equal' # equal, azure, gcp
mode = "absolute_slack"

main_data_dir = f'../data_output/{mode}_2022_processed/abs'
main_save_to_dir = 'data_output_v2'


slack_list = [24*365, 24]
job_length_list  = [1,6,12,24,48,96,168]
groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]
groupings = [ "Oceania"]

l = len(job_length_list)

weight_dict = {

    'equal': [1/l] * l, 
    'gcp':  [2/100, 4/100, 4/100, 10/100, 5/100, 5/100, 70/100], 
    'azure': [0.4/100, 0.9/100, 0.9/100, 1.4/100, 1.3/100, 2/100, 93.1/100]
}

weight_mode_list = ['equal', 'azure', 'gcp']
for weight_mode in weight_mode_list:    
    
    new_mode_dir = f"{main_save_to_dir}/{weight_mode}"
    check_dir(new_mode_dir)
    weight_list = weight_dict[weight_mode]
    combined_mean_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")
    combined_conf_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")
    combined_std_err_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")


    for row, slack in enumerate(slack_list): 
        for g in groupings: 

            if weight_mode == 'equal': 
                members = regions.get_grouping_members(g)

            else: 
                members = regions.get_provider_members(g, weight_mode)

            temp_grouping_weighted_df = pd.DataFrame()

            for w, job in enumerate(job_length_list): 

                abs_combined_file = f"{main_data_dir}/job_{job}/slack_{slack}/combined.csv" # reductions -- the difference already accounted
                abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"
                
                
                combined_df = pd.read_csv(abs_combined_file)    
                slack0_df = pd.read_csv(abs_slack0_file)    

                global_slack0_emissions = slack0_df.sum(axis=1)   

                weighted_savings = (combined_df.mean()/job) * weight_list[w]
                temp_grouping_weighted_df[job] = weighted_savings


            group_weighted_savings = temp_grouping_weighted_df.sum(axis=1) / sum(weight_list)
    
            
            group_saved_emissions = group_weighted_savings[group_weighted_savings.index.isin(members)]
            
            group_values = group_saved_emissions.values
            group_mean = group_saved_emissions.mean()
        
            a = group_saved_emissions.values
            conf_interval = list(st.t.interval(0.95, len(a)-1, loc=np.mean(a), scale=st.sem(a)))
            high_end = conf_interval[1] - group_mean
            low_end = group_mean - conf_interval[0]

            if len(members) <= 2:

                split = (group_saved_emissions.max()-group_saved_emissions.min())/2

                high_end = split
                low_end = split
            
            combined_mean_df.loc[slack,g] = group_mean
            combined_conf_df.loc[slack,g] = tuple([high_end, low_end])

    mean_name = f"{new_mode_dir}/mean.csv"
    conf_name = f"{new_mode_dir}/conf.csv"

    combined_mean_df.to_csv(mean_name)
    combined_conf_df.to_csv(conf_name)
