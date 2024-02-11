import pandas as pd

def get_year_df(df, selectedyear=2022): 
    copy_df = df.copy(deep=True)
    copy_df = format_df(copy_df)
    year_df = copy_df.loc[copy_df["year"] == str(selectedyear)].reset_index(drop=True)
    year_df = year_df.ffill().bfill()

    return year_df

def format_df(df): 
    copy_df = df.copy(deep=True)
    copy_df[["date", "time"]] = copy_df["datetime"].str.split("T", expand=True)
    copy_df[["year", 'month', "day"]] = copy_df['date'].str.split("-", expand=True)
    copy_df['time'] = copy_df['time'].str.slice(0,8)
    return copy_df 

