import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans
import seaborn as sns
import pandas as pd 
import os 
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../global_modules")
sys.path.append(moduledir)

import graph_templates

start_year = 2020
end_year = 2022

start_file = f'data_output/mean_and_cv_{start_year}.csv'
end_file = f'data_output/mean_and_cv_{end_year}.csv'

savetodir = 'plot_output'

y = r"Change in Carbon Intensity (g.CO$_2$eq/kWh)"
x = r"Change in Avg. Daily Coefficient of Variation"


startyear_df = pd.read_csv(start_file,index_col='zone_code').rename_axis(None)
endyear_df = pd.read_csv(end_file,index_col='zone_code').rename_axis(None)
stat_df = endyear_df - startyear_df

k = 3
km = KMeans(n_clusters=k,init='k-means++', random_state = 1)
km.fit(stat_df)
labels = km.labels_
stat_df['cluster'] = labels

stat_df.columns = [y,x,'cluster']

no_change_label = stat_df[stat_df[y] == 0]['cluster'][0]
greener_change_label = stat_df[stat_df[y] <= -50]['cluster'][0]
less_green_change_label = stat_df[stat_df[y] >= 50]['cluster'][0]

red_df  = stat_df.loc[stat_df["cluster"] == less_green_change_label]
green_df  = stat_df.loc[stat_df["cluster"] == greener_change_label]
no_df  = stat_df.loc[stat_df["cluster"] == no_change_label]

total = len(stat_df)
red_count = len(red_df) / total
green_count = len(green_df) / total
no_count = len(no_df) / total

checker = len(red_df) + len(green_df)+len(no_df)

if checker != total: 
    print("BUG !!! checker != total")
    exit()

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

markersize = 50
markers = ['o','X','.']
colorlist = ['g', 'r', '#8C8C8C']


fig, ax = plt.subplots(figsize=(5,4))

green_df.plot.scatter(x=x, y=y,ax=ax,
                      c = colorlist[0],
                      marker=markers[0],
                      s=markersize,
                      edgecolors='k',
                      linewidth=0.2
                    )
red_df.plot.scatter(x=x, y=y,ax=ax,
                      marker=markers[1],
                      c = colorlist[1],
                      s=markersize,
                      edgecolors='k',
                      linewidth=0.2
                    )
no_df.plot.scatter(x=x, y=y,ax=ax,
                      c = colorlist[2],
                      edgecolors='k',
                      marker=markers[2],
                      s=markersize,
                      linewidth=0.2
                    )

columns = ["Higher renewable sources", 
           "Higher brown sources", 
           "No substantial changes"          
           ]

custom_line = []
for i in range(3): 
    custom_line.append(Line2D([], [], color="k", marker=markers[i], markerfacecolor=colorlist[i],markeredgewidth=0.8))


plt.ylim([-120, 120])
plt.xlim([-0.12, 0.12])

plt.tick_params( left=False, bottom=False)
plt.grid(alpha=0.7, zorder=-99)
plt.ylabel(y)
plt.xlabel(x)

plt.legend(
    custom_line, columns, handlelength=0, 
    bbox_to_anchor=(0.014,-0.03),
    markerscale=1.2,
    loc="lower left", ncol = 1, 
    frameon=False, 
)

plt.tight_layout()
# filename = f"{savetodir}/change_overtime"
filename = f"{savetodir}/change_overtime.pdf"
plt.savefig(filename, dpi=300, bbox_inches='tight',pad_inches = 0.1)