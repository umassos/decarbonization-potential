import pandas as pd 
import numpy as np
import math
import os 
import sys 

# np.random.seed(88)

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)
import format_df
from check_dir import check_dir
combined_file = "../../shared_data/combined_carbon.csv"

save_to_dir = 'data_output/mix_loads'
check_dir(save_to_dir)

carbon_df = pd.read_csv(combined_file)
carbon_df = format_df.get_year_df(carbon_df, selected_year=2022)
inf_trace = carbon_df.min(axis=1)

zone_code_list = carbon_df.columns
mix_list = [i/10 for i in range(0, 10+1, 1)] # non-migratable job

l = len(carbon_df)

for mix in mix_list: 
    size = math.ceil(l*(mix)) # migratable workload

    index = np.random.choice(carbon_df.index, size, replace=False)
    new_df = carbon_df.copy(deep=True)

    if size > 0:
        # change the number of slots for the migratable workload
        new_df.loc[new_df.index.isin(index), zone_code_list] = inf_trace.loc[inf_trace.index.isin(index)]

    file_name = os.path.join(save_to_dir, f'mix_{int(mix*100)}.csv') # non-migratavb

    new_df.to_csv(file_name, index=False)
    print(file_name)