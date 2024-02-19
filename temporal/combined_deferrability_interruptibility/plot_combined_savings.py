import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

import graph_templates


mode = "absolute_slack"
slack = 24


main_data_dir = f'data_output/{mode}'
save_to_dir = 'plot_output'

file_path = os.path.join(main_data_dir, f"slack_{slack}.csv")
combined_df = pd.read_csv(file_path, index_col='stats')

job_length_list  = [1,6,12,24,48,96,168]

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
mainlabelsize = 14
ticklabelsize = 12
legendsize = 12

fig, ax = plt.subplots(figsize=(4,3.5))
combined_df.T.plot.bar(ax=ax, stacked=True, legend=False, facecolor="#FFFF")
bars = ax.patches
hatchlist = ["//", "xx"]
counter = 0
colorlist = graph_templates.colorlist
indexlist = ["Defer", "Interrupt"]


for i , bar in enumerate(bars): 

    if i != 0 and i % len(job_length_list) == 0: 
        counter +=1 
    bar.set_hatch(hatchlist[counter])
    bar.set_edgecolor(colorlist[counter])
custom_line = []


for i in range(len(indexlist)): 
    custom_line.append(patches.Patch(facecolor="#FFFF",hatch=hatchlist[i],edgecolor=colorlist[i]))

plt.tick_params(direction='in', color='#BABABA',grid_alpha=0.35,bottom=False,left=False)
plt.ylim([0,45])
plt.xticks(rotation=360, fontsize=ticklabelsize-2)

plt.yticks(np.arange(0,45+1,15),fontsize=ticklabelsize)

plt.ylabel("Global Avg. Savings (%)", fontsize=mainlabelsize)
plt.xlabel("Job Length (Hour)", fontsize=mainlabelsize-2)
plt.legend(custom_line, indexlist,
            loc='upper right',
            bbox_to_anchor=(1.02, 1.03),
            frameon=False,
            prop=dict(weight="bold",size=12),)
plt.tight_layout()

savename = f"{save_to_dir }/combined_savings_slack_{slack}"
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()
