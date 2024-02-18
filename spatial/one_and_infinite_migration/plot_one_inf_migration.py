import pandas as pd 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns 
import numpy as np
import sys
import os 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import graph_templates 

savetodir = 'plot_output'

mean_df = pd.read_csv('savings_mean.csv', index_col='migration').rename_axis(None).T
std_df = pd.read_csv('savings_std.csv', index_col='migration').rename_axis(None).T
# max_df = pd.read_csv('savings_max.csv', index_col='migration').rename_axis(None).T
# min_df = pd.read_csv('savings_min.csv', index_col='migration').rename_axis(None).T



sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'
mainlabelsize = 14
ticklabelsize = 10
legendsize = 12

colorlist = graph_templates.colorlist
hatchlist = ["//", ".."]
custom_legend = [] 

legend_label = [
    '1-Migration',
    r'$\infty$-Migrations',
]
for i in range(len(legend_label)): 
    custom_legend.append(patches.Patch( facecolor="#FFFF",hatch=hatchlist[i],edgecolor=colorlist[i]))
fig, ax = plt.subplots(figsize=(4,3.5))

mean_df.plot.bar(ax=ax,
                yerr=std_df, 
                #  yerr=max_df,
                #  yerr=min_df,
                capsize=4, 
                facecolor="#FFFF",
                legend=False
                )


bars= ax.patches

c_counter = 0
h_counter = 0
for i, bar in enumerate(bars): 

    bar.set_hatch(hatchlist[h_counter])
    bar.set_edgecolor(colorlist[c_counter])
    if i == len(mean_df.index)-1:
        c_counter += 1
        h_counter += 1


# min_df = mean_df - min_df
# max_df = max_df - mean_df

# bar_min_maxs = np.vstack((list(zip(min_df['one'], max_df['one'])),
#                           list(zip(min_df['inf'], max_df['inf']))))

# print(bar_min_maxs)
# assert len(bar_min_maxs) == len(ax.patches)

# for patch, (min_y, max_y) in zip(ax.patches, bar_min_maxs):
#     plt.vlines(patch.get_x() + patch.get_width()/2,
#                min_y, max_y, color='k')


plt.legend(
    custom_legend, legend_label, 
    bbox_to_anchor=(0.,0.83,1,0.2),
    columnspacing=1,
    mode='expand',
    # loc="lower left",
    ncol=len(legend_label),
    frameon=False,
    prop=dict(size=legendsize), 
    handletextpad=0.35, 
)

y_lower = 0
y_upper = 100
step = 25
plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360,fontsize=ticklabelsize+2)
plt.yticks(np.arange(y_lower,y_upper+1,step),fontsize=ticklabelsize)
plt.ylabel(r"Global CO$_2$ Savings (%)",fontsize=14)
plt.xlabel("Latency Limit (ms)",fontsize=14, color="#FFFF")

plt.ylim([y_lower,y_upper])

savename = f"{savetodir}/migrate_geo_lowest"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()