import pandas as pd 
import numpy as np
import json

raw_file = '../shared_data/raw_gcp_latency.csv'
mapper_file = '../shared_data/gcp_dc_zonecode_mapper.json'
new_file = '../shared_data/gcp_latency_matrix.csv'

with open(mapper_file, 'r' ) as mapper_f: 
    mapper_dict = json.load(mapper_f)

raw_df = pd.read_csv(raw_file).sort_values('sending_region')

regions = raw_df['sending_region'].unique()

matrix = pd.DataFrame(columns=regions, index=regions)
for i in range(len(raw_df)): 
    row = raw_df.iloc[i]

    origin = row['sending_region']
    dest = row['receiving_region']
    latency = row['milliseconds']

    matrix.loc[origin, dest] = latency


df = pd.DataFrame(5, index=matrix.index, columns=matrix.index) # to its own region
np.fill_diagonal(matrix.values, df)

matrix = matrix.fillna(999999999) # if the origin-destination pair does not exist, latency to infinite
matrix.index.name = 'origin'
matrix.rename(columns=mapper_dict, index=mapper_dict, inplace=True)
matrix.to_csv(new_file)
