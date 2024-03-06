import matplotlib.pyplot as plt
import statsmodels.stats.api as sms
import pandas as pd
import numpy as np
import seaborn as sns 
import sys
import os 


currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import regions
import graph_templates 
from check_dir import check_dir

file_path = 'data_output/processed_mix_loads/processed_savings.csv'
savetodir = 'plot_output/mixed_workload'
check_dir(savetodir)
mix_list = [i for i in range(20, 100+1, 20)] # batch job
combined_df = pd.read_csv(file_path, index_col='stats').rename_axis(None)
combined_df.columns = combined_df.columns.astype(int)
combined_df = combined_df[mix_list]

combined_df = combined_df.T
yerr = combined_df[["low", "high"]].T.values

sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'


mainlabelsize = 14
ticklabelsize = 10
legendsize = 14

fig, ax = plt.subplots(figsize=(4,3.5))

combined_df["avg"].plot.bar(ax=ax,
                   yerr=yerr, 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   edgecolor="k"
                   )
y_lower = 0
y_upper = 450
step = 150

plt.ylim([y_lower, y_upper])
plt.yticks(np.arange(y_lower, y_upper+1, step))

ax.set_xlabel(r"Migratable Workload (%)",fontsize=mainlabelsize)
ax.set_ylabel(r"Carbon Reduction (g.CO$_2$eq)",fontsize=mainlabelsize)
ax.tick_params(left=False, bottom=False)

ax.set_xticklabels(ax.get_xticklabels(), rotation=360,fontsize=ticklabelsize)

savename = f"{savetodir}/mixed_workloads"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()