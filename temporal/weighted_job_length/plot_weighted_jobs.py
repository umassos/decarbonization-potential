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

weight_mode = 'azure' # equal, azure, gcp
slack = 24*365
std_dev = False # yerr bars, if False then use standard error

main_data_dir = f'data_output/{weight_mode}'
save_to_dir = f'plot_output/{weight_mode}'
check_dir(save_to_dir)

mean_file = os.path.join(main_data_dir, "mean.csv")
if std_dev:
    std_file = os.path.join(main_data_dir, "std_dev.csv")
else:
    std_file = os.path.join(main_data_dir, "std_err.csv")

mean_df = pd.read_csv(mean_file, index_col="slack").rename_axis(None)
std_df = pd.read_csv(std_file, index_col="slack").rename_axis(None)

mean_df = mean_df.loc[slack]
std_df = std_df.loc[slack]

sns.set()
sns.set_style('ticks')
plt.rcParams['font.family'] = graph_templates.get_font(1)
plt.rcParams['font.size'] = 14

fig, ax = plt.subplots(figsize=(4,3.5))
mean_df.plot.bar(ax=ax,
                   yerr=std_df, 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   hatch=["","","//","",""], 
                   edgecolor="k"
                   )

plt.tick_params(left=False, bottom=False)
plt.xticks(rotation=360)
plt.ylim([0,100])
plt.ylabel(r"Global Avg. Savings (%)",fontsize=14)
plt.xlabel("Slack",fontsize=14, color="#FFFF")

plt.tight_layout()
if std_dev: 
    file_tag = 'std_dev'
else: 
    file_tag = 'std_error'

savename = os.path.join(save_to_dir, f"{weight_mode}_slack_{slack}_{file_tag}.pdf")

plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()