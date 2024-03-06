import pandas as pd 
import numpy as np
import math
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)
import format_df
from check_dir import check_dir

np.random.seed(99)

combined_file = "../../shared_data/combined_carbon.csv"

save_to_dir = 'data_output/added_error'
check_dir(save_to_dir)


carbon_df = pd.read_csv(combined_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=2022)



zone_code_list = carbon_df.columns
error_list = [i/100 for i in range(0, 100+1, 20)]

l = len(carbon_df)
for zone_code in zone_code_list: 

    df = carbon_df[zone_code]

    min_df = df.min()

    new_df = pd.DataFrame()
    for error in error_list:

        choice = np.random.choice([-1, 1],size=l) # erorr can be +/-
        noise = np.random.uniform(low=0, high=error/2, size=l) # create noise with the error 
        noise = noise * choice
    
        df *= (1+noise)
        new_df[int(error*100)] = df

    new_df = new_df.round(decimals=2)
    new_file = os.path.join(save_to_dir, f"{zone_code}.csv")
    new_df.to_csv(new_file, index=False)
    print(new_file)