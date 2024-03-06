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

import graph_templates
file_path = 'data_output/emissions.csv'
save_to_dir = 'plot_output'

df = pd.read_csv(file_path, index_col='slack').rename_axis(None)
inf = 1000
slack_list = list(df.index)
slack_list[-1] = inf
df.index = slack_list

groupings = [ "Asia", "Americas", "Global", "Europe", "Oceania"]

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

df.loc[:,df.columns != "Global"].plot(ax=ax,
                   style=other_styles, 
                   color=colorlist
                   )

df["Global"].plot(
    ax=ax, 
    style='D-',
    color=global_color,
    lw=lw
)

plt.legend(
    custom_line, groupings, 
    bbox_to_anchor=(-0.07,0.94,1,0.2), 
    loc="lower left",

    ncol=len(df.columns), 
    prop=dict(size=legendsize),
    frameon=False, handlelength=0,
    markerscale=1.1,
    handletextpad=0.4, 
    columnspacing=0.5
)  
 

slack_list = list(df.index)
plt.xlabel("Slack", fontsize=mainlabelsize )
plt.ylabel(r"Carbon Reduction (g.CO$_2$eq)", fontsize=mainlabelsize)

plt.yticks(fontsize=ticklabelsize)
plt.xticks(slack_list, slack_list)

yupper = 200
ystep = 50


plt.ylim([0,yupper])
plt.xlim([0,inf+20])
xticksint = [0,24,168, 480, 720, inf]
xticksstr = ["", "24H","7D", "20D", "30D", "1Y"]
plt.xticks(xticksint, xticksstr)
plt.grid(alpha=0.8, zorder=-1)
plt.tick_params(bottom=False,left=False)

savename = f"{save_to_dir}/vary_slack"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()