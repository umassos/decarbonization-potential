import pandas as pd 
import matplotlib.pyplot as plt 
import matplotlib as mpl

import itertools
import seaborn as sns
import sys
import os 

currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import regions
import format_df
import graph_templates 
import get_flags

year = 2022

# plot the same destination regions as the periodicity graph
period_file =  '../../sim_trace_analysis/periodicity/data_output/periodicity_score.csv'
period_df = pd.read_csv(period_file, index_col='zone_code').rename_axis(None)
zone_code_list =  regions.get_year_order()
period_df = period_df.reindex(zone_code_list).dropna(axis=0 ,how='all')


data_dir = f'data_output'
save_to_dir = 'plot_output'

job = 1
slacklist = [24*365, 24]
annontate = ["One-Year Slack", "24H Slack"]

low_regions = list(period_df.index)
actual_names = []

for z in low_regions: 
    flag_tag = regions.get_flag_tag(z)
    actual_names.append(flag_tag)

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'


fig, ax = plt.subplots(2,1, figsize=(8,4), sharex=True)
suplabelsize = 16
fig.supylabel(r"Global Carbon Reduction (%)", y=0.40,  x=-0.08,fontsize=suplabelsize)
fig.supxlabel("Destination Regions", y=-0.26, x=0.53,fontsize=suplabelsize)


ax = ax.ravel()
hatches = ["///", "..."]
colorlist = ("#90e4c1",
             "#ffb07c")

linecolor = "#0652ff"
patterns  = list(itertools.chain.from_iterable(itertools.repeat(x, len(low_regions)) for x in hatches))

colors = list(itertools.chain.from_iterable(itertools.repeat(x, len(low_regions)) for x in colorlist))
mainlabelsize = 14
ticklabelsize = 12
legendsize = 14

for slack_index, slack in enumerate(slacklist): 

    file_path = os.path.join(data_dir, f'slack_{slack}.csv')
    combined_df = pd.read_csv(file_path, index_col='data').rename_axis(None)[low_regions]
    if slack_index == 0: 
        combined_df = combined_df.T.sort_values(by='Net', ascending=False)
        sort_list = combined_df.index
    else: 
        combined_df = combined_df.T
        combined_df = combined_df.reindex(sort_list)

    barplot = combined_df[["Spatial", "Temporal"]]
    lineplot = combined_df["Net"].T

    barplot.plot.bar(
        ax=ax[slack_index], 
        color=colorlist,
        stacked=True
    )
    lineplot.plot(ax=ax[slack_index], 
                style="o:", 
                markersize=4, 
                color=linecolor)

    bars = ax[slack_index].patches

    for i, bar in enumerate(bars):
        bar.set_facecolor("#FFFFFF")
        bar.set_hatch(patterns[i])
        bar.set_edgecolor(colors[i])

    ax[slack_index].tick_params(left=False, bottom=False)
    ax[slack_index].grid(alpha=0.7)
    ax[slack_index].set_ylim([-130, 130])
    ax[slack_index].set_xlim([-0.5,39.5])

    if slack_index != len(slacklist) - 1: 
        ax[slack_index].annotate(annontate[slack_index],
                                 xycoords='axes fraction',
                                   xy=(1,0.13), rotation=270,fontsize=ticklabelsize+2)
        ax[slack_index].legend().set_visible(False)
    if slack_index == len(slacklist) - 1: 
        xticks = ax[slack_index].set_xticks

        ax[slack_index].annotate(annontate[slack_index],xycoords='axes fraction',
                                  xy=(1,0.27), rotation=270,fontsize=ticklabelsize+2)
        ax[slack_index].set_xticklabels(actual_names, rotation=90,  y=-0.09,fontsize=ticklabelsize)
        ax[slack_index].legend(frameon=False, ncol=3,
                                loc="lower left",
                               bbox_to_anchor=(-0.01,-0.07, 1, 0.2),
                                 fontsize=legendsize)
    
        for ix, c in enumerate(actual_names):
            get_flags.offset_image(ix, c, ax[slack_index],y=-120)
    
fig.subplots_adjust(left=0, right=1, bottom=0, top=0.8)
fig.subplots_adjust(wspace=0, hspace=0.0)
savename = f"{save_to_dir}/combined_savings_stacked"

plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()
    