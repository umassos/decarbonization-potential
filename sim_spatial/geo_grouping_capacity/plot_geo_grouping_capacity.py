import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
import scipy.stats as st
import math
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

idle_cap = 50 # in percent we use 50 and 99 (for infinite capacity) in our paper 

groupings = ["Asia", "Americas" ,"Global", "Europe", "Oceania",]

combined_df = pd.DataFrame(index=["avg", "low" ,'high'])

for grouping in groupings: 

    members = regions.get_grouping_members(grouping)

    member_emission_df = data_df.loc[members]
    

    zero_idle_emissions =  member_emission_df['0']
    w_idle_emissions =  member_emission_df[str(idle_cap)]


    w_idle_mean = w_idle_emissions.mean(numeric_only=True)
    zero_idle_mean = zero_idle_emissions.mean(numeric_only=True)
    if math.isnan(w_idle_mean): 
        w_idle_mean = 0

    mean_savings =  zero_idle_mean - w_idle_mean


    conf_interval = list(st.t.interval(0.95, len(members)-1, loc=mean_savings))
    
    high_end = conf_interval[1] - mean_savings
    low_end =   mean_savings - conf_interval[0]

    combined_df.loc["avg", grouping] = mean_savings    
    combined_df.loc["low", grouping] = low_end
    combined_df.loc["high", grouping] = high_end

combined_df = combined_df.T
yerr = combined_df[["low", "high"]].T.values


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
                   yerr=yerr, 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   hatch=["","","//","",""], 
                   edgecolor="k")
index_list = combined_df.index

y_lower = 0
y_upper = 750
step = 250

plt.ylim([y_lower, y_upper])
plt.yticks(np.arange(y_lower, y_upper+1, step))

ax.set_xlabel("Global Idle Capacity (%)",fontsize=mainlabelsize, color='#FFFF')
ax.set_ylabel(r"Carbon Reduction (g.CO$_2$eq)",fontsize=mainlabelsize)
ax.tick_params(left=False, bottom=False)

ax.set_xticklabels(ax.get_xticklabels(), rotation=360,fontsize=ticklabelsize)

savename = f"{savetodir}/geo_grouping_w_cap_{idle_cap}"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()