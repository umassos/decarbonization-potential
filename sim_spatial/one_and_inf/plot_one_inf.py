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

mean_df = pd.read_csv(f'{datadir}/savings_mean.csv', index_col='migration').rename_axis(None).T

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

colorlist = ["#FFFF","k"]
hatchlist = ["", "..."]
custom_legend = [] 

legend_label = [
    '1-Migration',
    r'$\infty$-Migrations',
]
for i in range(len(legend_label)): 
    custom_legend.append(patches.Patch( facecolor="#FFFF",hatch=hatchlist[i],edgecolor='k'))
fig, ax = plt.subplots(figsize=(4,3.5))

one_low_df = list(mean_df["one_low"].T.values)
one_high_df = list(mean_df["one_high"].T.values)
inf_low_df = list(mean_df["inf_low"].T.values)
inf_high_df = list(mean_df["inf_high"].T.values)

yerr = [one_high_df, inf_high_df,one_low_df,inf_low_df ]
print(yerr)

mean_df[[ "one", "inf"]].plot.bar(ax=ax,
                yerr=yerr, 
                capsize=4, 
                facecolor="#FFFF",
                color = colorlist,
                legend=False
                )


bars= ax.patches

c_counter = 0
h_counter = 0
for i, bar in enumerate(bars): 

    bar.set_hatch(hatchlist[h_counter])
    bar.set_edgecolor('k')
    if i == len(mean_df.index)-1:
        c_counter += 1
        h_counter += 1


plt.legend(
    custom_legend, legend_label, 
    bbox_to_anchor=(0.,0.83,1,0.2),
    columnspacing=1.2,
    mode='expand',
    ncol=len(legend_label),
    frameon=False,
    prop=dict(size=legendsize), 
    handletextpad=0.35, 
)

y_upper = 400
y_lower = 0
step = 100
plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360,fontsize=ticklabelsize+2)
plt.ylabel(r"Carbon Reducion (g.CO$_2$eq)",fontsize=14)
# plt.xlabel("Latency Limit (ms)",fontsize=14, color="#FFFF") # height adjustment for the paper 

plt.ylim([y_lower,y_upper])
plt.yticks(np.arange(y_lower,y_upper+1,step),fontsize=ticklabelsize)


savename = f"{savetodir}/migrate_geo_lowest"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()