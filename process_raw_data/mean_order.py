import pandas as pd 
import json

file_path = '../shared_data/mean_stats.csv'
order_file_path =  '../shared_data/mean_order.json'
mean_df = pd.read_csv(file_path,index_col='zonecode').rename_axis(None)
mean_df.columns = mean_df.columns.astype(int)

yearlist = [2020, 2021, 2022]
order_dict = dict()
for year in yearlist: 

    year_df = mean_df[year]
    year_order = year_df.sort_values()
    region_order = list(year_order.index)
    order_dict[year] =  region_order


with open(order_file_path, "w") as f: 
    json.dump(order_dict, f, indent=4)