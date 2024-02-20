import pandas as pd 
import os
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import format_df 

savetodir = 'data_output'
rawdatadir = "../../shared_data/electricty_maps_raw_data"

files = os.listdir(rawdatadir)

yearlist = [2022, 2021, 2020]

for year in yearlist:
    year_df = pd.DataFrame(index=["mean", "cv"])


    for file in files: 

        region_name = file[:-4]
        absfile = os.path.join(rawdatadir, file)
        raw_df = pd.read_csv(absfile)

        raw_year_df = format_df.get_year_df(raw_df, year, drop_datetime=False)[['datetime', 'carbon_intensity_avg']]
        grouped_year_df = raw_year_df.groupby(raw_year_df['datetime'].dt.date) # group by date

        region_daily_std = grouped_year_df['carbon_intensity_avg'].std()
        region_daily_mean = grouped_year_df['carbon_intensity_avg'].mean()
        
        region_year_mean = raw_year_df['carbon_intensity_avg'].mean()
        region_year_cv = (region_daily_std/region_daily_mean).mean()
        
        year_df[region_name] = [region_year_mean, region_year_cv]

    year_df = year_df.T
    year_df.index.name = 'zone_code'

    file_name = f"{savetodir}/mean_and_cv_{year}.csv"
    year_df.to_csv(file_name)

