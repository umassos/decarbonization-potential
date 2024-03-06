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

from check_dir import check_dir
import graph_templates

temporal_file = 'data_output/processed_weighted_job/equal.csv'
spatial_file = 'data_output/spatial_savings/mean_inf_spatial.csv'


save_to_dir = 'plot_output/error'
check_dir(save_to_dir)

error_list = range(0, 100+1, 20)

temporal_df = pd.read_csv(temporal_file)
spatial_df = pd.read_csv(spatial_file)

spatial_df = spatial_df[spatial_df['error'].isin(error_list)]
temporal_df = temporal_df[temporal_df['error'].isin(error_list)]

combined_df = pd.DataFrame()

combined_df[r"Spatial: $\infty$-Migrations"] = spatial_df['inf']
combined_df["Temporal: One-Year Slack"] = temporal_df['8760']
combined_df.index = temporal_df['error']



# selected_index = [i for i in range(20, 100+1, 20)]
# combined_df = combined_df.loc[combined_df.index.isin(selected_index)]


mainlabelsize = 14
ticklabelsize = 12
legendsize = 12
lw = 2


sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'

fig, ax = plt.subplots(figsize=(4,3.5))
styles = [':P', ':o']
colors = ["#f76623","#0249a3", ]
combined_df.plot(
                ax=ax,
                style=styles, 
                color=colors, 
                lw=lw
                 )

y_lower = 0
y_upper = 50
step = 10
plt.ylim([0,y_upper])
plt.yticks(np.arange(0,y_upper+1, step), fontsize=ticklabelsize)
plt.legend(frameon=False,
        #    handlelength=2,

           handletextpad=1, 
           handlelength =0,   
            bbox_to_anchor=(-0.0,0.82,1,0.2), 
            loc='upper left', 
            fontsize=12, )

upper = 50
step = 10
# plt.xticks([i for i in range(0, upper+1, step)], [f"{i/100}" for i in range(0, upper+1, step)])
plt.xlim([-0.04, 104])
plt.ylabel(r"Carbon Increase (%)", fontsize=mainlabelsize)
plt.xlabel("Prediction Error (%)", fontsize=mainlabelsize )

ax.spines[['right', 'top']].set_visible(False)
plt.grid(alpha=0.8, zorder=-1)
plt.tick_params(bottom=False,left=False)

savename = os.path.join(save_to_dir, 'prediction_error')
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()