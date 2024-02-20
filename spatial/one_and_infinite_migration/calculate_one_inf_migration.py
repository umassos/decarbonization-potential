import pandas as pd 
import sys
import os 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import format_df
import regions


combined_carbon_file = os.path.join( '../..', 'shared_data/combined_carbon.csv')
save_to_dir = "data_output"

year = 2022
groupings = ["Asia", "Americas", "Global", "Europe", "Oceania"]

carbon_df = pd.read_csv(combined_carbon_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=year)

all_region_mean = carbon_df.mean()

combined_df_mean = pd.DataFrame(index=["one", "inf"]).rename_axis('migration')
combined_df_std_dev = pd.DataFrame(index=["one", "inf"]).rename_axis('migration')
combined_df_std_err = pd.DataFrame(index=["one", "inf"]).rename_axis('migration')

for grouping in groupings: 

    members = regions.get_grouping_members(grouping)
    member_df = carbon_df[members]
    member_mean = member_df.mean()

    lowest_member_name =  member_mean.idxmin() # destination for one-migration
    mem_inf_trace = member_df.min(axis=1) # infinite migration trace

    one_dest_trace = member_df[lowest_member_name]
    mem_savings_one = member_df.subtract(one_dest_trace, axis=0)
    mem_savings_inf = member_df.subtract(mem_inf_trace, axis=0)


    no_migration_emission = member_df.sum()
    lowest_region_emission = member_df[lowest_member_name].sum()

    
    one_migration_savings = mem_savings_one.div(member_df)* 100
    inf_migration_savings = mem_savings_inf.div(member_df)* 100

    one_migration_region_mean = one_migration_savings.mean()
    one_migration_savings_mean = one_migration_region_mean.mean()
    one_migration_savings_std_err = one_migration_region_mean.sem() # standard error
    one_migration_savings_std_dev = one_migration_region_mean.std() # standard deviation
    
    inf_migration_region_mean = one_migration_savings.mean()
    inf_migration_savings_mean = inf_migration_region_mean.mean()
    inf_migration_savings_std_err = inf_migration_region_mean.sem() # standard error
    inf_migration_savings_std_dev = inf_migration_region_mean.std() # standard deviation
    

    combined_df_mean.loc["one", grouping] = one_migration_savings_mean
    combined_df_mean.loc["inf", grouping] = inf_migration_savings_mean

    
    combined_df_std_dev.loc["one", grouping] = one_migration_savings_std_dev
    combined_df_std_dev.loc["inf", grouping] = inf_migration_savings_std_dev

    
    combined_df_std_err.loc["one", grouping] = one_migration_savings_std_err
    combined_df_std_err.loc["inf", grouping] = inf_migration_savings_std_err
    

combined_df_mean.to_csv(f'{save_to_dir}/savings_mean.csv')
combined_df_std_dev.to_csv(f'{save_to_dir}/savings_std_dev.csv')
combined_df_std_err.to_csv(f'{save_to_dir}/savings_std_err.csv')