import pandas as pd 
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import format_df

rawdatadir = "../../shared_data/electricty_maps_raw_data"

selected_regions = [
"CA-ON", 
"US-CAL-CISO", 
"AU-VIC", 
"IN-MH"
]

real_names = [
    "Ontario",
    "California",
    "Victoria",
    "Mumbai"
]


non_renewables = ["gas",
                  "biomass",
                  "oil", 
                  "coal",
                  "unknown",
              "nuclear"]
renewables = ["solar", 
              "wind", 
              "hydro"]

combined_source = non_renewables + renewables
combined_cols = [f"power_production_{s}_avg" for s in combined_source]

combined_df = pd.DataFrame()

for region in selected_regions: 
    absfile = f"{rawdatadir}/{region}.csv"

    zone_df = pd.read_csv(absfile)
    df = format_df.get_year_df(zone_df, selected_year=2022)

    total_production = df[combined_cols].sum(axis=1)#.sum()

    renewables_ratio = df[combined_cols].T.divide(total_production).T

    renewables_ratio = renewables_ratio.mean()

    combined_df[region] = renewables_ratio

combined_df.columns = real_names
combined_df.index = combined_df.index.str.replace("power_production_", "")
combined_df.index = combined_df.index.str.replace("_avg", "")
combined_df = combined_df.T

combined_df["fossil fuels"] = combined_df[["unknown", "biomass", "oil", "coal", "unknown", "gas"]].sum(axis=1) 
combined_df = combined_df[["hydro", "solar","wind", "nuclear", "fossil fuels"]]
combined_df.index.name = 'name'
combined_df.to_csv("data_output/energy_mix.csv")