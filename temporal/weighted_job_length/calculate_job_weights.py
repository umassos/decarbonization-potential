import pandas as pd 
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
main_save_to_dir = 'data_output'

new_mode_dir = f"{main_save_to_dir}/{weight_mode}"
check_dir(new_mode_dir)

slack_list = [24*365, 24]
job_length_list  = [1,6,12,24,48,96,168]
groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]

l = len(job_length_list)

weight_dict = {

    'equal': [1/l] * l, 
    'gcp':  [2/100, 4/100, 4/100, 10/100, 5/100, 5/100, 70/100], 
    'azure': [0.4/100, 0.9/100, 0.9/100, 1.4/100, 1.3/100, 2/100, 93.1/100]
}

weight_list = weight_dict[weight_mode]

combined_mean_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")
combined_std_dev_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")
combined_std_err_df = pd.DataFrame(index=slack_list,columns=groupings).rename_axis("slack")
for row, slack in enumerate(slack_list): 
    for g in groupings: 

        if weight_mode == 'equal': 
            members = regions.get_grouping_members(g)

        else: 
            members = regions.get_provider_members(g, weight_mode)

        temp_grouping_weighted_df = pd.DataFrame()
        temp_global_baseline_df = pd.DataFrame()
        for w, job in enumerate(job_length_list): 

            abs_combined_file = f"{main_data_dir}/job_{job}/slack_{slack}/combined.csv" # savings -- the difference already accounted
            abs_slack0_file = f"{main_data_dir}/job_{job}/slack_{slack}/slack0.csv"
            
            
            combined_df = pd.read_csv(abs_combined_file)    
            slack0_df = pd.read_csv(abs_slack0_file)    

            global_slack0_emissions = slack0_df.sum(axis=1)   

            weighted_savings = combined_df.mean() * weight_list[w]
            global_baseline_weighted_savings = slack0_df.mean() * weight_list[w]
            
            temp_grouping_weighted_df[job] = weighted_savings
            temp_global_baseline_df[job] = global_baseline_weighted_savings

        group_weighted_savings = temp_grouping_weighted_df.sum(axis=1)
        global_weighted_savings = temp_global_baseline_df.sum(axis=1)

        global_mean = global_weighted_savings.mean()
        
        group_saved_emissions = group_weighted_savings[group_weighted_savings.index.isin(members)]
    
        group_saved_emissions /= global_mean
        group_saved_emissions *= 100
        
        group_mean = group_saved_emissions.mean()
        group_std_err = group_saved_emissions.sem()
        group_std_dev = group_saved_emissions.std()

        combined_mean_df.loc[slack,g] = group_mean
        combined_std_err_df.loc[slack,g] = group_std_err
        combined_std_dev_df.loc[slack,g] = group_std_dev

mean_name = f"{new_mode_dir}/mean.csv"
std_dev_name = f"{new_mode_dir}/std_dev.csv"
std_err_name = f"{new_mode_dir}/std_err.csv"

combined_mean_df.to_csv(mean_name)
combined_std_dev_df.to_csv(std_dev_name)
combined_std_err_df.to_csv(std_err_name)