import pandas as pd 
import os 
import sys

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir,"..",  "global_modules")
sys.path.append(global_module)


import format_df

file_path = '../shared_data/combined_carbon.csv'
year_mean_stat_file = '../shared_data/mean_stats.csv'

carbon_df = pd.read_csv(file_path)

yearlist = [2020, 2021, 2022]
stats_df = pd.DataFrame()

for year in yearlist: 

    year_df = format_df.get_year_df(carbon_df, year)
    mean_df = year_df.mean()
    stats_df[year] = mean_df

stats_df.index.name = "zonecode"
stats_df.to_csv(year_mean_stat_file)
