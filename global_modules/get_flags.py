
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage,AnnotationBbox
import matplotlib.pyplot as plt
from PIL import Image
import os


currdir = os.path.dirname(__file__)

flagdir = f"{currdir}/flags_dir"

savetodir = "/nfs/obelix/users1/tsukprasert/formatted_map/global_modules/outputs/flags"
def get_flag(zonecode, size=16): 
    file = f"{flagdir}/{size}/{zonecode}.png"

    im = Image.open(file).rotate(90, expand=True)
    # im = im.
    return im

def offset_image(coord, name, ax, y=0):

    name = name.split("-")[0]
    img = get_flag(name)
    im = OffsetImage(img)
    im.set(width=7,height=11)
    im.image.axes = ax

    # ab = AnnotationBbox(im, (coord, -120),  xybox=(0, -14.), frameon=False,
    #                     xycoords='data',  boxcoords="offset points", pad=0)
    ab = AnnotationBbox(im, (coord, y),  xybox=(0, -14.), frameon=False,
                        xycoords='data',  boxcoords="offset points", pad=0)

    ax.add_artist(ab)



