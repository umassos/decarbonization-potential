import os 
import matplotlib.font_manager as fm
currdir = os.path.dirname(__file__)
fontdir = f"{currdir}/fonts"

colorlist = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
          "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
style=["o:", "s:", "D:","^:", "P:", "s:", "P:"]

latex_1_path = f"{fontdir}/LinLibertine_R.ttf"
latex_2_path = f"{fontdir}/LinLibertine_RZ.ttf"
latex_3_path = f"{fontdir}/LinLibertine_RB.ttf"



latex_dict = {
    "latex_1":latex_1_path,
    "latex_2":latex_2_path,
    "latex_3":latex_3_path
}

def set_font(path, name):
    fe = fm.FontEntry(
    fname=path,
    name=name, 
    size='scalable')
    fm.fontManager.ttflist.insert(0, fe)

def get_font(level=1): 

    font_name = f"latex_{level}"

    if font_name not in fm.fontManager.ttflist:
        set_font(latex_dict[font_name], font_name)
    return font_name

