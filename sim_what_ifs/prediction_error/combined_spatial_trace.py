import pandas as pd 
import os 
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions

main_data_dir = 'data_output/added_error'
main_save_to_dir = 'data_output/spatial_combined_df'
check_dir(main_save_to_dir)

members = regions.get_year_order()

std_list = [i for i in range(0, 100+1, 20)]

for std in std_list:

    std_df = pd.DataFrame()

    for member in members: 

        absfile = os.path.join(main_data_dir, f'{member}.csv')

        df = pd.read_csv(absfile)
        df.columns = df.columns.astype(int)

        std_df[member] = df[std]

    file_name = os.path.join(main_save_to_dir, f'error_{std}.csv')
    std_df.to_csv(file_name, index=False)