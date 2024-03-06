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


carbon_aware_file = 'data_output/processed_weighted_interrupt/slack_8760.csv'
carbon_agnostic_file = 'data_output/processed_weighted_slack0/slack_8760.csv'


save_to_dir = 'plot_output/temporal_scenario'
check_dir(save_to_dir)

selected_region = "US-CAL-CISO"

carbon_aware_df = pd.read_csv(carbon_aware_file, index_col='multiplier')
carbon_agnostic_df = pd.read_csv(carbon_agnostic_file, index_col='multiplier')

carbon_aware_df = carbon_aware_df[selected_region]
carbon_agnostic_df = carbon_agnostic_df[selected_region]


data_df = pd.DataFrame()
data_df["Carbon-Agnostic"] = carbon_agnostic_df
data_df["Carbon-Aware"] = carbon_aware_df

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
savename = os.path.join(save_to_dir, f'temporal_greener_{selected_region}_v2')
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()