import pandas as pd

def format_df(df): 
    copy_df = df.copy(deep=True)
    copy_df['datetime'] = copy_df['datetime'].str.slice(stop=-6)
    copy_df['datetime'] = pd.to_datetime(copy_df['datetime'])
    copy_df = copy_df.bfill().ffill()
    return copy_df

def get_year_df(df, selected_year = 2022, drop_datetime=True): 
    copy_df = format_df(df)


    copy_df = copy_df[copy_df['datetime'].dt.year == selected_year]
    if drop_datetime: 
        copy_df.drop(columns=['datetime'], inplace=True)
        copy_df.reset_index(drop=True, inplace=True)

    return copy_df



