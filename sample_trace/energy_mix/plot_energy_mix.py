import pandas as pd 
import matplotlib.pyplot as plt
import itertools
import numpy as np
import matplotlib as mpl
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import graph_templates

file_path = 'energy_mix.csv'
savetodir = 'plot_output'

raw_df = pd.read_csv(file_path, index_col='name').rename_axis(None)

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

colors_list = ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF",
            "#DEBB9B", "#FAB0E4", "#CFCFCF", "#FFFEA3", "#B9F2F0"]


fig, ax = plt.subplots(figsize=(5,3))
ax = raw_df.plot.bar(
    ax=ax, 
    stacked=True, 
    edgecolor='black',
    color=colors_list
)

bars = [thing for thing in ax.containers if isinstance(thing,mpl.container.BarContainer)]

# print(len(bars))
# print(len(ax.patches))
# exit()
patterns = ['//', 'oo', '\\\\', '++', '...']
# hatchlist = [p for p in patterns for _ in range(len(raw_df.columns)) ]
hatchlist = [p for _ in range(len(raw_df.columns)) for p in patterns  ]

for i , bar in enumerate(bars): 
    for patch in bar:

        patch.set_hatch(hatchlist[i])

mainlabelsize = 18
ticklabelsize = 12
legendsize = 12


plt.ylim([0,1])
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.legend(frameon=False,
            bbox_to_anchor=(-0.01,0.99, 1, 0.2), 
            loc="upper center",

            handletextpad=0.3,
            columnspacing=0.4,
            handlelength = 1.5,
            labelspacing=0,
            fontsize=12,
            ncol=5
           )

plt.ylabel("Source Ratio", size=ticklabelsize)
plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360,fontsize=ticklabelsize+2)


savename = f"{savetodir}/generation_mix.pdf"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)

