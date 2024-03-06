import pandas as pd 
import os
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import format_df 

savetodir = 'data_output'
combined_carbon_file = "../../shared_data/combined_carbon.csv"
carbon_df = pd.read_csv(combined_carbon_file)

yearlist = [2022, 2021, 2020]

for year in yearlist:
    year_df = pd.DataFrame(columns=["mean", "cv"])

    raw_year_df = format_df.get_year_df(carbon_df, year, drop_datetime=False)

    raw_year_df.set_index('datetime', inplace=True)
    raw_year_df.index =  pd.to_datetime(raw_year_df.index)

    grouped_year_df = raw_year_df.groupby(raw_year_df.index.date) # group by date

    region_daily_std = grouped_year_df.std()
    region_daily_mean = grouped_year_df.mean()

    region_year_mean = raw_year_df.mean()
    region_year_cv = (region_daily_std/region_daily_mean).mean()

    year_df['mean'] = region_year_mean
    year_df['cv'] = region_year_cv

    year_df.index.name = 'zone_code'

    file_name = f"{savetodir}/mean_and_cv_{year}.csv"
    year_df.to_csv(file_name)

