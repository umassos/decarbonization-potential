import pandas as pd
import datetime
import os 

raw_data_dir = '../downloaded_carbon_data' # make sure that the downloaded files are in this directory
save_to_dir = '../shared_data'
raw_files = os.listdir(raw_data_dir)

year_dict = dict()

for r_file in raw_files: 
    zone_code, year, granular = r_file[:-4].split('_')
    if year not in year_dict:
        year_dict[year] = []
    year_dict[year].append(zone_code)

year_list = list(year_dict.keys())
year_list.sort()

zone_code_list = year_dict[year_list[0]]
l = len(zone_code_list)
file_check = all(len(year_dict[y]) == l for y in year_dict)

if not file_check: 
    print("Not all zone codes have the same number of years!")
    exit()


start_year = year_list[0]
end_year = year_list[-1]
start_date = datetime.datetime.strptime(f'{start_year}-01-01', "%Y-%m-%d")
end_date = datetime.datetime.strptime(f'{int(end_year)+1}-01-01', "%Y-%m-%d")
datelist = pd.date_range(start_date, end_date, freq="H", inclusive='left')#.strftime("%H:%M:%S")


combined_df = pd.DataFrame()
combined_df['datetime'] = datelist

for zone_code in zone_code_list:

    zone_temp_df = pd.DataFrame()
    for year in year_list: 

        zone_year_file = os.path.join(raw_data_dir, f'{zone_code}_{year}_hourly.csv')

        raw_df = pd.read_csv(zone_year_file)
        carbon_trace = raw_df['Carbon Intensity gCO₂eq/kWh (LCA)']

        zone_temp_df = pd.concat([zone_temp_df, carbon_trace])
    
    zone_temp_df.columns = [zone_code]
    zone_temp_df.reset_index(drop=True, inplace=True)

    combined_df  = pd.concat([combined_df,zone_temp_df], axis=1)

combined_df[zone_code_list] = combined_df[zone_code_list].bfill().ffill()


save_name = os.path.join(save_to_dir, 'combined_carbon.csv')
combined_df.to_csv(save_name, index=False)

    