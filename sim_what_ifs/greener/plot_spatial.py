import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import graph_templates


selected_region = "US-CAL-CISO"
main_data_dir = 'data_output/spatial_combined_df'
save_to_dir = 'plot_output/spatial_scenario'
check_dir(save_to_dir)

multipliers = [i for i in range(0,100+1, 20)]


data_df = pd.DataFrame(index=multipliers, columns=["Carbon-Agnostic", "Carbon-Aware"])

for multiplier in multipliers:
    absfile = os.path.join(main_data_dir, f'added_{multiplier}.csv')
    df = pd.read_csv(absfile)

    inf_trace = df.min(axis=1)

    inf_emissions = inf_trace.mean()
    region_emissions = df[selected_region].mean()

    data_df.loc[multiplier, 'Carbon-Aware'] = inf_emissions
    data_df.loc[multiplier, 'Carbon-Agnostic'] = region_emissions

mainlabelsize = 14
ticklabelsize = 12
legendsize = 12
sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

fig, ax = plt.subplots(figsize=(4,3.5))
colorlist = ["k","#bd2d2d"]
other_styles=["o:",  "X:"]

lw = 2
data_df.plot(
            ax=ax, 
            color=colorlist, 
            style=other_styles,
            lw=lw

            )

plt.legend(
    prop=dict(size=legendsize),
    frameon=False
)  

plt.ylabel(r"Carbon Emissions (g.CO$_2$eq)", fontsize=mainlabelsize)
plt.xlabel("Added Renewables (%)", fontsize=mainlabelsize )
plt.xlim([0, 103])

y_lower = 0
y_upper = 300
step = 100
plt.ylim([0,y_upper])
plt.yticks(np.arange(0,y_upper+1, step), fontsize=ticklabelsize)

ax.spines[['right', 'top']].set_visible(False)
plt.grid(alpha=0.8, zorder=-1)
plt.tick_params(bottom=False,left=False)
savename = os.path.join(save_to_dir, f'spatial_greener_{selected_region}')
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()