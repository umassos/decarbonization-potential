import pandas as pd 
import statsmodels.stats.api as sms
import scipy.stats as st

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

combined_df_mean = pd.DataFrame(index=["one", "inf","one_high","one_low","inf_high","inf_low"]).rename_axis('migration')


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

    
    # one_migration_savings = mem_savings_one.div(member_df)* 100
    # inf_migration_savings = mem_savings_inf.div(member_df)* 100

    one_migration_region_mean = mem_savings_one.mean()

    one_migration_savings_mean = one_migration_region_mean.mean()
    # one_migration_savings_std_err = one_migration_region_mean.sem() # standard error
    # one_migration_savings_std_dev = one_migration_region_mean.std() # standard deviation
    
    inf_migration_region_mean = mem_savings_inf.mean()
    inf_migration_savings_mean = inf_migration_region_mean.mean()
    
    # inf_migration_savings_std_err = inf_migration_region_mean.sem() # standard error
    # one_migration_conf_interval = list(sms.DescrStatsW(one_migration_region_mean.values).tconfint_mean(alpha=0.05))
    # inf_migration_conf_interval = list(sms.DescrStatsW(inf_migration_region_mean.values).tconfint_mean(alpha=0.05))
    one_migration_conf_interval = list(st.t.interval(0.95, len(members)-1, loc=one_migration_savings_mean ))
    inf_migration_conf_interval = list(st.t.interval(0.95, len(members)-1, loc=inf_migration_savings_mean ))
    # inf_migration_savings_std_dev = inf_migration_region_mean.std() # standard deviation
    

    combined_df_mean.loc["one", grouping] = one_migration_savings_mean
    combined_df_mean.loc["inf", grouping] = inf_migration_savings_mean

    combined_df_mean.loc["one_low", grouping] = one_migration_savings_mean - one_migration_conf_interval[0]
    combined_df_mean.loc["one_high", grouping] = one_migration_conf_interval[1] - one_migration_savings_mean
    
    combined_df_mean.loc["inf_low", grouping] =  inf_migration_savings_mean - inf_migration_conf_interval[0]
    combined_df_mean.loc["inf_high", grouping] = inf_migration_conf_interval[1] - inf_migration_savings_mean



combined_df_mean.to_csv(f'{save_to_dir}/savings_mean.csv')
# combined_df_std_dev.to_csv(f'{save_to_dir}/savings_std_dev.csv')
# combined_df_std_err.to_csv(f'{save_to_dir}/savings_std_err.csv')