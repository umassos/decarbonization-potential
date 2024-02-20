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

datadir = 'data_output'
savetodir = 'plot_output'
std_dev = False # yerr bars, if False then use standard error

mean_df = pd.read_csv(f'{datadir}/savings_mean.csv', index_col='migration').rename_axis(None).T

if std_dev:
    std_df = pd.read_csv(f'{datadir}/savings_std_dev.csv', index_col='migration').rename_axis(None).T
else: 
    std_df = pd.read_csv(f'{datadir}/savings_std_err.csv', index_col='migration').rename_axis(None).T

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


plt.legend(
    custom_legend, legend_label, 
    bbox_to_anchor=(0.,0.83,1,0.2),
    columnspacing=1,
    mode='expand',
    ncol=len(legend_label),
    frameon=False,
    prop=dict(size=legendsize), 
    handletextpad=0.35, 
)


if std_dev: 
    file_tag = 'std_dev'
    y_upper = 125
else: 
    file_tag = 'std_error'
    y_upper = 100

y_lower = 0
step = 25
plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360,fontsize=ticklabelsize+2)
plt.yticks(np.arange(y_lower,y_upper+1,step),fontsize=ticklabelsize)
plt.ylabel(r"Global Avg. Savings (%)",fontsize=14)
plt.xlabel("Latency Limit (ms)",fontsize=14, color="#FFFF")

plt.ylim([y_lower,y_upper])


savename = f"{savetodir}/migrate_geo_lowest_{file_tag}.pdf"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()