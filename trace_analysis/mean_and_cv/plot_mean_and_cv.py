import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import os 
import sys

currdir = os.path.dirname(__file__)
moduledir = os.path.join(currdir, "../../","global_modules")
sys.path.append(moduledir)

import graph_templates
import regions

def annon(zonecode,x,y,ax,rot=0, flag=False,zorder=99): 
    name = regions.get_other_tag(zonecode)
    if flag:
        name = regions.get_flag_tag(zonecode)
    ax.annotate(name, xy=(x,y),xycoords='data',fontsize=tagfont, font=boldfont, rotation=rot,zorder=zorder)

year = 2022
file_path = f'data/mean_and_cv_{year}.csv'
savetodir = 'plot_output'


tagfont = 6
boldfont = graph_templates.get_font(2)

stat_df = pd.read_csv(file_path, index_col='zone_code').rename_axis(None)

x = "Average Daily Coefficient of Variation (CV)"
y = r"Average Carbon Intensity (g.CO$_2$eq/kWh)"
stat_df.columns = [y,x]


sns.set()
sns.set_style('ticks')
plt.rcParams["font.family"] = graph_templates.get_font(1)
plt.rcParams['text.color'] = 'k'
plt.rcParams['axes.labelcolor'] = 'k'
plt.rcParams['xtick.color'] = 'k'
plt.rcParams['ytick.color'] = 'k'



fig, ax = plt.subplots(figsize=(5,4))
xmin = -0.009
xmax = 0.45
ymin = 0
ymax = 1000
stat_df.plot.scatter(x=x, 
                     y=y,c=y,cmap="RdYlGn_r",
                     ax=ax,
                     s=50,
                      colorbar=False,
                      vmin=ymin,
                      vmax=ymax, 
                      edgecolors='k',
                      linewidth=0.15
                    )


plt.tick_params(direction='in', color='grey', left=False, bottom=False)

lw = 0.8

global_avg = 368.39
global_cv = 0.12
plt.axhline(global_avg, color = 'grey', linestyle = 'dashdot',linewidth=lw)
plt.axvline(x=global_cv, color = 'grey', linestyle = 'dashdot',linewidth=lw)
intensity_stats = f"Global Avg. Intensity"
cv_stats = f"Global Avg. CV"


ax.annotate(intensity_stats , xy=(0.335,415),xycoords='data', size=8)
ax.annotate(global_avg , xy=(0.411,378),xycoords='data', size=8)
ax.annotate(cv_stats, xy=(0.123,850),xycoords='data', size=8, rotation=0)
ax.annotate(global_cv, xy=(0.123,820),xycoords='data', size=8, rotation=0)

plt.xlabel(x)
plt.ylabel(y)
plt.ylim([ymin,ymax])
plt.xlim([xmin,xmax])

annon("SE-SE1",0.07,27,ax=ax,flag=True)
annon("CA-QC",0.019,33,ax=ax,rot=45,flag=True)
annon("NO-NO1",0.102,47,ax=ax)
annon("CA-ON",0.345,60,ax=ax,rot=45)
annon("FR",0.117,95,ax=ax)
annon("NZ",0.095,105,ax=ax)
annon("US-NW-BPAT",0.142,96,ax=ax,flag=True)
annon("CH",0.257,153,ax=ax)
annon("BE",0.179,172,ax=ax)
annon("BR-CS",0.061,102,ax=ax,flag=True)
annon("ES",0.151,202,ax=ax)
annon("FI",0.074,148,ax=ax)
annon("DK-DK1",0.202,202,ax=ax,flag=True)
annon("AT",0.1334,246,ax=ax,flag=True)
annon("GB",0.164,236,ax=ax)
annon("CL-SEN",0.223,214,ax=ax, flag=True)
annon("US-CAL-CISO",0.228,266,ax=ax, flag=True)
annon("US-NW-PACW",0.195,237,ax=ax,rot=45,flag=True)
annon("IT-NO",0.0775,347,ax=ax,flag=True)
annon("IE",0.155,405,ax=ax)
annon("US-TEX-ERCO",0.107,406,ax=ax,rot=45,flag=True)
annon("US-MIDA-PJM",0.014,365,ax=ax,rot=45,flag=True)
annon("HK",-0.006,447,ax=ax)
annon("US-CAR-SCEG",0.089,413,ax=ax,rot=45,flag=True)
annon("GR",0.185,440,ax=ax,flag=True)
annon("NL",0.134,410,ax=ax,flag=True)
annon("DE",0.145,489,ax=ax,rot=45,flag=True)
annon("US-SW-AZPS",0.09,461,ax=ax,rot=45,flag=True)
annon("JP-KN",0.0512,457,ax=ax)
annon("US-SE-SOCO",0.011,407,ax=ax,rot=45,flag=True)
annon("KR",0.0275,496,ax=ax)
annon("SG",0.001,490,ax=ax)
annon("US-NW-NEVP",0.155,484,ax=ax,rot=45,flag=True)
annon("TW",0.042,539,ax=ax,rot=45)
annon("JP-TK",0.078,555.136,ax=ax)
annon("US-MIDW-MISO",0.050,500,ax=ax, flag=True)
annon("AU-VIC",0.087,531.068,ax=ax)
annon("US-NW-PACE",0.125,668,ax=ax,rot=45,flag=True)
annon("AU-NSW",0.154,600,ax=ax,rot=45)
annon("US-MIDW-AECI",0.066,676,ax=ax,rot=45,flag=True)
annon("ZA",0.032,701,ax=ax)
annon("IN-MH",0.013, 740,ax=ax,rot=45)
annon("IN-UP",0.026, 740,ax=ax,rot=45)
annon("US-NW-WACM",0.057, 770,ax=ax,flag=True)
annon("PL",0.078, 819.20,ax=ax)
annon("ID",0, 658,ax=ax)
annon("US-MIDW-LGEE",0.022,864,ax=ax)
annon("IL",0.025, 580,ax=ax)
annon("US-NE-ISNE",0.059, 227,ax=ax,rot=45,flag=True)
annon("US-NY-NYIS",0.028,225,ax=ax,rot=45,flag=True)
annon("NO-NO2",0.332,62,ax=ax,rot=45)
annon("AU-SA",0.4,190,ax=ax,rot=45)
annon("DK-BHM",0.386,57,ax=ax)
annon("US-CENT-SPA",0.303,290,ax=ax,flag=True)
annon("CY",0.143,949.7636,ax=ax)
annon("US-HI-OA",0.079,920,ax=ax,flag=True)
annon("US-NW-NWMT",0.0565, 695,ax=ax,rot=45,flag=True)
# annon("US-NW-GCPD",0.182, 37.15,ax=ax,rot=45,)
annon("AU-QLD",0.138, 659,ax=ax,rot=45)
annon("AU-WA",0.207, 434.886,ax=ax)
annon("GB-NIR",0.196, 326,ax=ax)
annon("UY",0.221,99,ax=ax)
annon("PE",0.080,211,ax=ax)
annon("LU",0.204,372,ax=ax)
annon("US-NW-SCL",-0.001,28,ax=ax,rot=45, flag=True)
annon("US-TEN-TVA",0.017,308,ax=ax,rot=45, flag=True)
annon("SE-SE4",0.216,47,ax=ax)

filename = f"{savetodir}/mean_and_cv"
# filename = f"{savetodir}/mean_and_cv.pdf"
plt.tight_layout()
plt.savefig(filename, dpi=300, bbox_inches='tight',pad_inches = 0.1)
plt.close() 