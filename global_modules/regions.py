import pandas as pd
import json
import os 
 
curr_dir = os.path.dirname(__file__)
raw_data_dir = os.path.join(curr_dir, '..', 'rawdata')
static_file_dir = os.path.join(curr_dir, 'static_files')

order_file = os.path.join(raw_data_dir, 'mean_order.json')
mean_file = os.path.join(raw_data_dir, 'mean_stats.csv')

region_grouping_file = os.path.join(static_file_dir, 'name_stats.csv')
provider_regions_file = os.path.join(static_file_dir,'data_regions.csv')


with open(order_file, "r") as of: 
    order_dict = json.load(of)

region_grouping_df = pd.read_csv(region_grouping_file)
provider_region_df = pd.read_csv(provider_regions_file)

mean_stats_df = pd.read_csv(mean_file, index_col="zonecode").rename_axis(None)

def get_year_order(year=2022): 
    order = order_dict[str(year)]
    return order

def get_grouping_members(geo_grouping): 
    
    if geo_grouping != "Global":
        names = region_grouping_df.loc[region_grouping_df[geo_grouping] == 1]['zone_code'].values
    else: 
        names = region_grouping_df['zone_code'].values

    return names

def get_provider_members(geo_grouping, provider):

    if geo_grouping != "Global":
        names = provider_region_df.loc[provider_region_df[geo_grouping] == 1]#['zone_code']#.dropna().values
    else: 
        names = provider_region_df
    names = names.loc[names[provider] == 1]['zone_code'].dropna().values
    return names


def get_mean(members, year): 
    
    year_df = mean_stats_df[str(year)]
    member_df = year_df[year_df.index.isin(members)]
    mean = member_df.mean()

    return mean

def get_member_mean(member, year=2022): 
    year_df = mean_stats_df[str(year)]
    member_mean = year_df.loc[member]
    return member_mean

def get_group_mean(geo_grouping, year=2022): 
    members = get_grouping_members(geo_grouping)
    mean = get_mean(members, year)
    return mean

def get_year_mean_df(year=2022): 
    year_df = mean_stats_df[str(year)]
    order = get_year_order(year)
    year_df = year_df.reindex(order)
    return year_df

def get_flag_tag(zonecode):
    row = region_grouping_df.loc[region_grouping_df['zone_code'] == zonecode]
    countryname = row['flag_tag']
    return countryname.values[0]

def get_other_tag(zonecode):
    row = region_grouping_df.loc[region_grouping_df['zone_code'] == zonecode]
    countryname = row['other_name']
    return countryname.values[0]

if __name__ == "__main__":
    names = get_provider_members("Europe", "gcp")
    n2 = get_grouping_members("Europe")
    print(names)
    print(n2)