import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys 

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../..","global_modules")
sys.path.append(moduledir)

from check_dir import check_dir
import graph_templates

weight_mode = 'equal' # equal, azure, gcp
slack = 24*365


main_data_dir = f'data_output_v2/{weight_mode}'
save_to_dir = f'plot_output_v2/{weight_mode}'
check_dir(save_to_dir)

mean_file = os.path.join(main_data_dir, "mean.csv")
std_file = os.path.join(main_data_dir, "conf.csv")


mean_df = pd.read_csv(mean_file, index_col="slack").rename_axis(None)
conf_data_df = pd.read_csv(std_file, index_col="slack").rename_axis(None)

mean_df = mean_df.loc[slack]
index_list = conf_data_df.columns
conf_tups = conf_data_df.loc[slack].tolist()
conf_tups = list(map(eval,conf_tups))

std_df = pd.DataFrame(index=index_list, columns=['high', 'low'])
for idx, conf in enumerate(conf_tups): 

    high = conf[0]
    low = conf[1]
    std_df.loc[index_list[idx], 'high'] = high
    std_df.loc[index_list[idx], 'low'] = low


yerr = std_df[["low", "high"]].T.values

sns.set()
sns.set_style('ticks')
plt.rcParams['font.family'] = graph_templates.get_font(1)
plt.rcParams['font.size'] = 14

fig, ax = plt.subplots(figsize=(4,3.5))
mean_df.plot.bar(ax=ax,
                   yerr=yerr, 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   hatch=["","","//","",""], 
                   edgecolor="k"
                   )

plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360)
plt.ylim([0,350])
plt.ylabel(r"Carbon Reduction (g.CO$_2$eq)",fontsize=14)
plt.xlabel("Slack",fontsize=14, color="#FFFF")

plt.tight_layout()

savename = os.path.join(save_to_dir, f"{weight_mode}_slack_{slack}")
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()