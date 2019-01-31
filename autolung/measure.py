"""
This script will control the mesurement of the airspaces in labelled binary images
"""
import numpy as np
from scipy import stats
from collections import namedtuple
from skimage.measure import regionprops


def airspace_properties(labeled_img):
    """Get area, perimeter, diameter mesurements for all airspaces in an image"""
    props = regionprops(labeled_img)
    
    areas = [p.area for p in props]
    dias = [p.equivalent_diameter for p in props]
    pers = [p.perimeter for p in props]
    obj_num = len(areas)

    Measurements = namedtuple('Measurements', ['obj_num', 'areas', 'dias', 'pers'])
    m = Measurements(obj_num, areas, dias, pers)

    return m


def mli(labeled_img):
    """Calculate the Mean linear intercept by raster scanning the image and determining the length
    of unbroken stretches of airspace"""
    # get length of consecutive stretches of white pixels per row
    intercepts = []
    for row in labeled_img:
        result = np.diff(np.where(np.concatenate(([row[0]], row[:-1] != row[1:], [True])))[0])[::2]
        for measurement in result:
            intercepts.append(measurement)

    mli = np.mean(intercepts)
    
    return mli 


def expansion(labeled_img):
    """calculate the EXP index of the image"""
    # calculate the shape of the image and then the total area in pixels
    x, y = labeled_img.shape
    total_area = x * y

    # calculate the sum of all airspaces measured in the image 
    airspace_area = np.sum(airspace_properties(labeled_img).areas)
    tissue_area = total_area - airspace_area
    exp =  airspace_area / tissue_area * 100

    Expansion_Index = namedtuple("Expansion_Index", ['width', 'height', 'airspace_area', 'tissue_area', 'exp'])
    e = Expansion_Index(x, y, airspace_area, tissue_area, exp) 
    
    return e 


def d_indeces(dia_ar):
    """Return the D Indeces calculated from the equivalent diameter measurements"""
    D0 = np.mean(dia_ar) 
    D0_var = np.var(dia_ar)
    D0_skew = stats.skew(dia_ar)

    D1 = D0 * (1 + (D0_var / D0**2))
    D2 = (D0 * (1 + (D0_var / (D0**2 + D0_var)) * (2 + ((np.sqrt(D0_var) * D0_skew) / D0))))

    D_Indeces = namedtuple('D_Indeces', ['D0', 'D1', 'D2'])
    d = D_Indeces(D0, D1, D2)

    return d


def measure_all(labeled_img, **kwargs):
    """Combine all measurement functions into a single call and return stats
    in calibrated units"""
    # scale of images is in pixels / um
    scale = kwargs.get('scale')
    um = 1 / scale
    sq_um = (1 / scale) ** 2

    airspaces = airspace_properties(labeled_img)
    m = mli(labeled_img)
    e = expansion(labeled_img)
    d = d_indeces(airspaces.dias)

    obj_num = airspaces.obj_num
    mean_area = np.mean(airspaces.areas) * sq_um
    stdev_area = np.std(airspaces.areas) * sq_um
    mean_dia = np.mean(airspaces.dias) * um
    mean_per = np.mean(airspaces.pers) * um
    width = e.width * um
    height = e.height * um
    air_area = e.airspace_area * sq_um
    tissue_area = e.tissue_area * sq_um
    exp = e.exp
    D0 = d.D0 * um
    D1 = d.D1 * um
    D2 = d.D2 * um

    # create a dictionary of all collected data
    data = {"Image_Width(um)": width, "Image_Height(um)" : height, "Obj_Num" : obj_num, 
        "Mean_Area(sq_um)" : mean_area, "Mean_Dia(um)" : mean_dia,
        "Mean_Per(um)" : mean_per, "Total_Airspace_Area(sq_um)" : air_area, 
        "Total_Tissue_Area(sq_um)" : tissue_area, "EXP" : exp, "Lm(um)": m, "D0" : D0, "D1" : D1, "D2" : D2,
        "Stdev_Area(sq_um)" : stdev_area}
        
    return data



