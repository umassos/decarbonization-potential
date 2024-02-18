import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns 
import sys
import os 


currdir = os.path.dirname(__file__)
global_module = os.path.join(currdir, "../..", "global_modules")
sys.path.append(global_module)

import regions
import graph_templates 

file_path = 'emissions.csv'
savetodir = 'plot_output'

data_df = pd.read_csv(file_path, index_col='zonecode').rename_axis(None)

idle_cap = 50 # in percent 
# idle_cap = 99

groupings = ["Oceania", "Europe" ,"Asia", "Americas", "Global",]

combined_df = pd.DataFrame(index=["avg", "std"])


baseline = data_df['0'].sum()

for grouping in groupings: 

    members = regions.get_grouping_members(grouping)

    member_emission_df = data_df.loc[members]

    zero_idle_emissions =  member_emission_df['0']
    w_idle_emissions =  member_emission_df[str(idle_cap)]
    abs_savings =  (zero_idle_emissions - w_idle_emissions).sum()

    normalized_savings = (abs_savings/baseline)*100

    max_savings = normalized_savings.max()
    min_savings = normalized_savings.min()
  


    member_savings = normalized_savings.mean()
    # member_std = (abs_savings.std()/baseline)*100 # local based line
    std_savings = ((zero_idle_emissions - w_idle_emissions).std()/baseline)*100
    combined_df.loc["avg", grouping] = member_savings
    combined_df.loc["std", grouping] = std_savings 
combined_df = combined_df.T
print(combined_df)

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
                   yerr=combined_df["std"], 
                   capsize=4, 
                   facecolor="#FFFFFF", 
                   hatch=["","","","","//"], 
                   edgecolor="k")

y_lower = 0
y_upper = 100

plt.ylim([y_lower, y_upper])

ax.set_ylabel(r"Global CO$_2$. Savings (%)",fontsize=mainlabelsize)
ax.tick_params(left=False, bottom=False)

ax.set_xticklabels(ax.get_xticklabels(), rotation=360,fontsize=ticklabelsize)

# adjust for sizes in the paper
ax.set_xlabel("Global Idle Capacity (%)",fontsize=mainlabelsize, color='#FFFF')
savename = f"{savetodir}/one_migration_w_cap_{idle_cap}"
plt.tight_layout()
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close()