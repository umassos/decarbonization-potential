import pandas as pd 
import os

rawdatadir = "../shared_data/electricty_maps_raw_data"
combined_file_path = '../shared_data/combined_carbon.csv'

files = os.listdir(rawdatadir)

combined_df = pd.DataFrame()
for index, file in enumerate(files): 
    
    zonecode = file[:-4]
    absfile = f"{rawdatadir}/{file}"

    df = pd.read_csv(absfile)
    
    if index == 0: 
        combined_df["datetime"] = df["datetime"]
    
    combined_df[zonecode] = df["carbon_intensity_avg"]
combined_df.to_csv(combined_file_path, index=False)