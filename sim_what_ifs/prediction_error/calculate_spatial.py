import pandas as pd 
import numpy as np
import os 
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions


main_data_dir = 'data_output/spatial_combined_df'
main_save_to_dir = 'data_output/spatial_savings'
check_dir(main_save_to_dir)

multipliers = [i for i in range(0,100+1, 10)]


base_file = os.path.join(main_data_dir, 'error_0.csv')
based_df = pd.read_csv(base_file)

based_inf_trace = based_df.min(axis=1)
based_inf_locs = based_df.idxmin(axis=1).values

data_df = pd.DataFrame()
for multiplier in multipliers:
    absfile = os.path.join(main_data_dir, f'error_{multiplier}.csv')
    df = pd.read_csv(absfile)

    error_inf_trace = df.min(axis=1)
    error_inf_locs = df.idxmin(axis=1)

    accounted_carbon_trace = []

    for row, des in enumerate(error_inf_locs): 

        accounted_carbon = based_df.loc[row, des]
        accounted_carbon_trace.append(accounted_carbon)

    added_carbon =  (accounted_carbon_trace - based_inf_trace)/based_inf_trace
    added_carbon *= 100 

    mean_diff = added_carbon.mean()

    data_df[multiplier] = [mean_diff]

data_df = data_df.T
data_df.index.name = 'error'
data_df.columns = ['inf']

file_name = os.path.join(main_save_to_dir, 'mean_inf_spatial.csv')
data_df.to_csv(file_name)