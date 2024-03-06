import pandas as pd 
import os 
import sys 
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import graph_templates

rawfile = "data_output/carbon_sample.csv"
savetodir = "plot_output"
colorlist = ["royalblue","violet", "seagreen","firebrick" ]


name_dict = {
"CA-ON":'Ontario', 
"US-CAL-CISO":"California", 
"AU-VIC":"Victoria", 
"IN-MH":"Mumbai"

}

raw_df = pd.read_csv(rawfile)[name_dict.keys()].bfill().ffill()


xlabels = ["Dec 12","Dec 13", "Dec 14", "Dec 15"]
xcoors = [12, 36,60 ,84]
line_styles= [ (0, (3, 1, 1, 1)),'solid', 'dashed', (0, (1, 1))]
custom_line = []


sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'


width = 1.9

for i in range(len(name_dict)): 
    custom_line.append(Line2D([0], [0], linestyle=line_styles[i], color=colorlist[i], linewidth=width))

fig, ax = plt.subplots(figsize=(5,3))
raw_df.plot(ax=ax, linewidth=width, color=colorlist)


lines = ax.get_lines()
for i, line in enumerate(lines): 
    line.set_linestyle(line_styles[i])
plt.axvline(x = 23, color = '#BABABA',ls=':')
plt.axvline(x = 47, color = '#BABABA',ls=':')
plt.axvline(x = 71, color = '#BABABA',ls=':')

ax.spines[['right', 'top']].set_visible(False)
mainlabelsize = 18
ticklabelsize = 12
legendsize = 12
plt.ylim([0,800])
plt.xlim([0,96])
plt.xticks(xcoors, xlabels,fontsize=ticklabelsize+2)
x = r"Avg. Daily Coefficient of Variation (CV)"

plt.yticks(np.arange(0,801, 200),fontsize=ticklabelsize)
plt.ylabel(r"Avg. CO$_{2}$ Intensity (g.CO$_{2}$eq/kWh)", size=ticklabelsize)
plt.tick_params(left=False, bottom=False)

plt.legend(
    
            custom_line, name_dict.values(),
            frameon=False,
            bbox_to_anchor=(-0.015,0.99, 1, 0.2), 
            loc="upper center",
            # borderaxespad=0, 
            # mode="expand", 
            handletextpad=0.3,
            columnspacing=0.4,
            handlelength = 1.5,
            labelspacing=0,
            fontsize=12,
            ncol=5
           )                                    
plt.tight_layout()
savename = f"{savetodir}/general_pattern"
plt.savefig(savename, dpi=300, bbox_inches='tight',pad_inches = 0.1)

