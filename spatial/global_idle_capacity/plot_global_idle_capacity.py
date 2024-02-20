import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import graph_templates 


file_path = "data_output/emissions.csv"
savetodir = "plot_output"
df = pd.read_csv(file_path,index_col='zonecode').rename_axis(None)

idle_cap_list = [i for i in range(0, 100, 10)]
idle_cap_list.append(99)

emission_df = df.sum()
emission_df.index = emission_df.index.astype(int)
baseline = emission_df.loc[0]
savings_df = emission_df.subtract(baseline) * -1
savings_df /= baseline
savings_df *= 100




sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

fig, ax= plt.subplots(figsize=(4,3.5))

savings_df = savings_df.round(decimals=2)

savings_df.plot(
    ax=ax, 
    # linewidth = ,
    style=['D-','o-','.--','s:'],

    color = '#fc2647', 
    lw=2
)


for i in idle_cap_list:
    y = savings_df.loc[i]
    annon = f"{y}"
    ax.annotate( annon,(int(i)-3,y-6), fontsize=7, rotation=0)


mainlabelsize = 14
ticklabelsize = 10
legendsize = 14

y1_lower = 0
y1_upper = 100
step = 20

percent_ticks = [i for i in range(0, y1_upper+1, step)]

ax.set_ylim([y1_lower, y1_upper])
ax.set_xlim([y1_lower, 106])


ax.set_yticks(percent_ticks)
ax.spines[['right', 'top']].set_visible(False)
ax.tick_params(left=False, bottom=False)
ax.set_ylabel(r"Global CO$_2$. Savings (%)",fontsize=mainlabelsize)
ax.set_xlabel("Global Idle Capacity (%)",fontsize=mainlabelsize)


plt.xticks(rotation=360,fontsize=ticklabelsize)

plt.tick_params(left=False, bottom=False)
ax.grid(alpha=0.7, zorder=-99)
plt.tight_layout()
# savename = f"{outputdir}/per_region_cap_percent_v2"
savename = f"{savetodir}/global_idle_cap"
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)

plt.close()