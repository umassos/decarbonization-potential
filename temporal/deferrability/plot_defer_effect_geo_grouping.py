import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import regions
import graph_templates


mode = "absolute_slack"
slack = 24

main_data_dir = f'data_output/{mode}'
save_to_dir = 'plot_output'
file_path = os.path.join(main_data_dir, f"slack_{slack}.csv")
savings_df = pd.read_csv(file_path, index_col='job')
savings_df.index = savings_df.index.astype(int)


groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]
job_length_list  = [1,6,12,24,48,96,168]

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

colorlist = ["#448ee4", "#ffa756","#fc2647", "#6fc276", "#b790d4",]

custom_line = []
markers=["o", "s", "D","^", "P", "s", "P"]
for i in range(len(groupings)): 
    custom_line.append(Line2D([], [], color=colorlist[i], marker=markers[i], markerfacecolor=colorlist[i],markeredgewidth=1,  markersize=5))

global_color = colorlist[2]

colorlist.remove(global_color)

other_styles=["o:", "s:","^:", "P:", "s:", "P:"]
fig, ax = plt.subplots(figsize=(4,3.5))

ax.spines[['right', 'top']].set_visible(False)

mainlabelsize = 14
ticklabelsize = 12
legendsize = 12
lw = 2
# exit()
savings_df.loc[:,savings_df.columns != "Global"].plot(ax=ax,
                   style=other_styles, 
                   color=colorlist
                   )
savings_df["Global"].plot(
    ax=ax, 
    style='D-',
    color=global_color,
    lw=lw
)
xticks_str = [str(i) for i in range(0, 168+1) if i in job_length_list]
strmapp = [str(i) for i in job_length_list]
joblist_corr = []
joblist_label = []
for i in range(1, 168+1): 

    if i in job_length_list: 
        joblist_corr.append(i)
        joblist_label.append(str(i))

plt.legend(
    custom_line, groupings, 
    bbox_to_anchor=(-0.07,0.94,1,0.2), 
    loc="lower left",
    # mode="expand",
    ncol=len(savings_df.columns), 
    prop=dict(size=legendsize),
    frameon=False, handlelength=0,
    markerscale=1.1,
    handletextpad=0.4, 
    columnspacing=0.5
)  
 
plt.xlabel("Job Length (Hour)", fontsize=mainlabelsize )
plt.ylabel(r"Avg. Defer Savings (%)", fontsize=mainlabelsize)

plt.xticks(joblist_corr, joblist_label,fontsize=ticklabelsize-2)
plt.xlim([0,171])

y_lower = 0
y_upper = 60
plt.ylim([0,y_upper])
plt.yticks(np.arange(0,y_upper+1, 10), fontsize=ticklabelsize)
plt.grid(alpha=0.8, zorder=-1)
plt.tick_params(bottom=False,left=False)


savename = f"{save_to_dir}/defer_slack_{slack}"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()