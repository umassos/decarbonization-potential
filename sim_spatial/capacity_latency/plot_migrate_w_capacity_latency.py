import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np
import sys
import os 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import graph_templates 

file_path = 'data_output/emissions.csv'
savetodir = 'plot_output'

idle_cap_list = [99,50]
emission_df = pd.read_csv(file_path, index_col='latency').rename_axis(None)
emission_df.columns = emission_df.columns.astype(int)
baseline = emission_df[0]

savings_df = emission_df.T.subtract(baseline,axis=1) * -1
savings_df /= baseline
savings_df *= 100

savings_df = savings_df.T[idle_cap_list]


column_names = [r"$\infty$ Capacity","50% Utilization",]
savings_df.columns = column_names

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
mainlabelsize = 16
ticklabelsize = 10
legendsize = 14
lw = 2

fig, ax = plt.subplots(figsize=(4,3.5))
styles=["o:", "s:","D-","^:", "P:", "s:", "P:"]
styles=[ "D:","o:",]

colorlist = ["#bd2d2d","k"]
savings_df.plot(ax=ax,
                 color=colorlist, 
                 style=styles, 
                 lw=lw
                 )

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
mainlabelsize = 16
ticklabelsize = 10
legendsize = 14
lw = 2

ax.spines[['right', 'top']].set_visible(False)
plt.yticks(np.arange(0,121,20))
plt.ylim([0,100])
plt.xlim([5,310])
xticks_int = [5, 50]
xticks_str = ["5", "50"]

for i in range(100, 301, 50):
    xticks_int.append(i)
    xticks_str.append(str(i))
    
plt.xticks(xticks_int, xticks_str)
plt.xlabel("Latency Limit (ms)",fontsize=14)
plt.ylabel(r"Global Carbon Reduction (%)",fontsize=14)
plt.tick_params(bottom=False,left=False)
plt.legend(frameon=False, fontsize=12, 
           bbox_to_anchor=(-0.0,0.83,1,0.2),
           loc='upper left', 
           handletextpad=1, 
           handlelength =0    
           )
plt.grid(alpha=0.7)
plt.tight_layout()

savename = f"{savetodir}/cap_gcp_latency"


plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()