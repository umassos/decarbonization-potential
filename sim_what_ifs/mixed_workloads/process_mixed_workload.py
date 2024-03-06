import pandas as pd 
import numpy as np
import statsmodels.stats.api as sms
import os 
import sys 

np.random.seed(88)

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)
import format_df
from check_dir import check_dir
combined_file = "../../shared_data/combined_carbon.csv"


raw_data_dir = 'data_output/mix_loads'
save_to_dir = 'data_output/processed_mix_loads'
check_dir(save_to_dir)

carbon_df = pd.read_csv(combined_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=2022)

zone_code_list = carbon_df.columns
mix_list = [i for i in range(0, 100+1, 10)] # batch job


combined_df = pd.DataFrame(index=['avg', 'high', 'low'],columns=mix_list).rename_axis('stats')
for mix in mix_list: 

    file_path = os.path.join(raw_data_dir, f'mix_{mix}.csv')

    data_df = pd.read_csv(file_path)

    savings = carbon_df - data_df

    region_savings = savings.mean()
    conf_interval = list(sms.DescrStatsW(region_savings.values).tconfint_mean(alpha=0.05))

    mean_savings = region_savings.mean()

    combined_df.loc["avg", mix] = mean_savings
    combined_df.loc["low", mix] =  mean_savings - conf_interval[0]
    combined_df.loc["high", mix] = conf_interval[1] - mean_savings

save_to_name = os.path.join(save_to_dir, 'processed_savings.csv')
combined_df.to_csv(save_to_name)
