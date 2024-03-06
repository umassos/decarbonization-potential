import pandas as pd
import numpy as np
import os 
import sys 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "..", "global_modules")
sys.path.append(global_module)

from regions import get_year_order
from check_dir import check_dir

year = 2022
main_data_dir = 'data_output'
absolute = True # if then proportional slack

if absolute:
    modetag = f"absolute_slack_{year}"
    slacklist = [24,24*7, 24*20,24*30,24*365] # absolute slack
else:
    modetag = f"proportional_slack_{year}"
    slacklist = [i for i in range(1,10+1)] # proportional slack

datadir = f"{main_data_dir}/{modetag}"
mainsavetodir = f"{main_data_dir }/{modetag}_processed"
abs_dir = f"{mainsavetodir}/abs"

check_dir(mainsavetodir)
check_dir(abs_dir)

joblengthlist  = [1,6,12,24,48,96,168]
selected_year = 2022
country_order = get_year_order(year)

for job in joblengthlist: 

    abs_jobdir = f"{abs_dir}/job_{job}"
    check_dir(abs_jobdir)

    for slack in slacklist: 

        abs_slackdir = f"{abs_jobdir}/slack_{slack}"
        check_dir(abs_slackdir)

        non_interrupt_df_abs = pd.DataFrame(columns=country_order)
        interrupt_df_abs = pd.DataFrame(columns=country_order)
        combined_df_abs = pd.DataFrame(columns=country_order)
        slack0_df_abs = pd.DataFrame(columns=country_order)

        non_interrrupt_abs_file = f"{abs_slackdir}/non_interrupt.csv"
        interrrupt_abs_file = f"{abs_slackdir}/interrupt.csv"
        combined_abs_file = f"{abs_slackdir}/combined.csv"
        slack0_abs_file = f"{abs_slackdir}/slack0.csv"

        for c in country_order:

            absfile = f"{datadir}/job_{job}/slack_{slack}/{c}.csv"
            data_df = pd.read_csv(absfile).dropna()

            non_interrupt = data_df["non_interrupt"]
            interrupt = data_df["interrupt"]
            slack_0 = data_df["slack_0"]

            non_interrupt_abs_savings = (slack_0 - non_interrupt)
            combined_abs_savings = (slack_0 - interrupt)
            interrupt_abs_savings = non_interrupt - interrupt
            
            non_interrupt_df_abs[c] = non_interrupt_abs_savings
            interrupt_df_abs[c] = interrupt_abs_savings
            combined_df_abs[c] = combined_abs_savings
            slack0_df_abs[c] = slack_0

        non_interrupt_df_abs.to_csv(non_interrrupt_abs_file,index=False)
        interrupt_df_abs.to_csv(interrrupt_abs_file,index=False)
        combined_df_abs.to_csv(combined_abs_file,index=False)
        slack0_df_abs.to_csv(slack0_abs_file,index=False)
