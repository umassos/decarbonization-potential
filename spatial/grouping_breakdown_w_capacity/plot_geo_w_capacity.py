import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns 
import sys
import os 


currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import regions
import graph_templates 

file_path = 'data_output/emissions.csv'
savetodir = 'plot_output'

data_df = pd.read_csv(file_path, index_col='zonecode').rename_axis(None)

idle_cap = 99 # in percent we use 50 and 99 (for infinite capacity) in our paper 
std_dev = False # yerr bars, if False then use standard error

groupings = ["Asia", "Americas" ,"Global", "Europe", "Oceania",]

combined_df = pd.DataFrame(index=["avg", "std"])


global_baseline = data_df['0'].mean().mean()


for grouping in groupings: 

    members = regions.get_grouping_members(grouping)

    member_emission_df = data_df.loc[members]

    zero_idle_emissions =  member_emission_df['0']
    w_idle_emissions =  member_emission_df[str(idle_cap)]

    region_savings = zero_idle_emissions - w_idle_emissions
    region_savings /= global_baseline
    region_savings *= 100

    mean_savings = region_savings.mean()

    if std_dev: 
        std_savings = region_savings.std()
    else:
        std_savings = region_savings.sem()

    combined_df.loc["avg", grouping] = mean_savings
    combined_df.loc["std", grouping] = std_savings 
combined_df = combined_df.T

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'


mainlabelsize = 14
ticklabelsize = 10
legendsize = 14

fig, ax = plt.subplots(figsize=(4,3.5))
combined_df["avg"].plot.bar(ax=ax,
                   yerr=combined_df["std"], 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   hatch=["","","//","",""], 
                   edgecolor="k")

y_lower = 0
y_upper = 200
step = 50

plt.ylim([y_lower, y_upper])
plt.yticks(np.arange(y_lower, y_upper+1, step))

ax.set_ylabel(r"Global Avg. Savings (%)",fontsize=mainlabelsize)
ax.tick_params(left=False, bottom=False)

ax.set_xticklabels(ax.get_xticklabels(), rotation=360,fontsize=ticklabelsize)

if std_dev: 
    file_tag = 'std_dev'
else: 
    file_tag = 'std_error'
savename = f"{savetodir}/one_migration_w_cap_{idle_cap}_{file_tag}.pdf"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()