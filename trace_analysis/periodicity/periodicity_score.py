import pandas as pd 
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import graph_templates
import regions 
import get_flags


file_path = 'data_output/periodicity_score.csv'
savetodir = 'plot_output'

stat_df = pd.read_csv(file_path, index_col='zone_code').rename_axis(None)

order = regions.get_year_order()

stat_df = stat_df.reindex(order).dropna(axis=0 ,how='all')

selected_period = ["0","24","168"]
other_period = ["48","72" ,"96","120","144" ]

other_period_mean = stat_df[other_period].mean(axis=1, numeric_only=True)

df = stat_df[selected_period]
df["Others"] = other_period_mean
df = df.round(decimals=2)

zonecodelist = df.index
flagtaglist = []

for z in zonecodelist: 
    flag_tag = regions.get_flag_tag(z)
    flagtaglist.append(flag_tag)

df.index = flagtaglist


sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

# boldfont = graph_templates.get_font()
markers = [ "o" , "s" , "H","^"]


fig, ax = plt.subplots(figsize=(7,0.9))
columns = df.columns
# colorlist = graph_templates.colorlist
# colorlist = ["skyblue", "bisque", "lightgreen", "sandybrown"]
colorlist = ["#7bc8f6",
             "#ffb2d0", 
             "#9af764", 
            "#BABABA"]

# colorlist = colorlist[::-1]
# markers = markers[::-1]


for i, col in enumerate(columns[::-1]):
    i = -(i+1)
    plt.scatter(df.index, df[col], label=col, 
                c=colorlist[i], 
                edgecolors="k",linewidths=0.8,
                marker=markers[i],s=70)

for i, c in enumerate(flagtaglist):
    get_flags.offset_image(i, c, ax)

plt.tick_params(direction='in', color='#BABABA',grid_alpha=0.30,bottom=False, left=False)
plt.yticks(np.arange(0,1.3,0.5), fontsize=10)

plt.xticks( rotation=90, fontsize=9, y=-0.27)
plt.ylabel("Score",  fontsize=14,x=1)
plt.grid(alpha=0.85)

custom_line = []
for i in range(len(columns)): 
    custom_line.append(Line2D([], [], color="k", marker=markers[i], markerfacecolor=colorlist[i],markeredgewidth=1,  markersize=9))

plt.legend(
    custom_line, columns, handlelength=0, 
    bbox_to_anchor=(0.29,0.86,1,0.2),

    loc="lower left", ncol = len(custom_line), 
    frameon=False, 
    )
fig.subplots_adjust(left=0, right=1, bottom=0, top=0.8)
plt.ylim([-0.1, 1.2])
plt.xlim([-0.5,39.5])

savename = f"{savetodir}/periodicity_score.pdf"

plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0)
