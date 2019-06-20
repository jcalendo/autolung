"""Measure Airspace Parameters

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Main 'measurements' file. Controls all measurements performed on a given image. 
"""
from collections import namedtuple

import numpy as np
from scipy import stats
from skimage.measure import regionprops


def airspace_properties(labeled_img):
    """Return the properties of the airspaces.

    Measures the areas, perimeters, equivalent diameters of airspaces, and 
    the number of airspaces in a given image. measurements are returned in
    pixels.
    
    Arguments:
        labeled_img {np.array} -- binary image, uint16 numpy array
    
    Returns:
        [named tuple] -- area, perimeter, equivalent diameter, and number of objects
    """
    props = regionprops(labeled_img)
    
    areas = [p.area for p in props]
    dias = [p.equivalent_diameter for p in props]
    pers = [p.perimeter for p in props]
    obj_num = len(areas)

    Measurements = namedtuple('Measurements', ['obj_num', 'areas', 'dias', 'pers'])
    m = Measurements(obj_num, areas, dias, pers)

    return m


def mli(labeled_img):
    """Calculates the Mean Linear Intercept
    
    Calculates the Mean Linear Intercept (mli) by raster scanning the image and 
    returning a list of the lengths of unbroken 'airspace' segments

    Arguments:
        labeled_img {np.array} -- binary image, uint16 numpy array
    
    Returns:
        float -- length of Mean linear intercept in pixels
    """
    # get length of consecutive stretches of white pixels per row
    intercepts = []
    for row in labeled_img:
        result = np.diff(np.where(np.concatenate(([row[0]], row[:-1] != row[1:], [True])))[0])[::2]
        for measurement in result:
            intercepts.append(measurement)

    mli = np.mean(intercepts)
    
    return mli


def expansion(labeled_img):
    """Calculate the Expansion Index

    Ratio of the total area of the airspaces : total area of the tissue
    
    Arguments:
        labeled_img {np.array} -- binary image, uint16 numpy array
    
    Returns:
        float -- estimate of the Expansion Index
    """
    # calculate the shape of the image and then the total area in pixels
    x, y = labeled_img.shape
    total_area = x * y

    # calculate the sum of all airspaces measured in the image 
    airspace_area = np.sum(airspace_properties(labeled_img).areas)
    tissue_area = total_area - airspace_area
    exp =  airspace_area / tissue_area * 100

    Expansion_Index = namedtuple("Expansion_Index", ['width', 'height', 'airspace_area', 'tissue_area', 'exp'])
    e = Expansion_Index(y, x, airspace_area, tissue_area, exp) 
    
    return e 


def d_indeces(dia_ar):
    """Calculate the D indeces from the equivalent diameter measurements

    Return weighted measurements for the equivalent diameters - a measure of heterogeneity.
    For a full treatment of how D indeces are calculated see:
        Parameswaran, 2006. Quantitative characterization of airspace enlargement in emphysema.
    
    Arguments:
        dia_ar {numpy array} -- numpy array of equivalent diameter measurements for all airspaces in an image
    
    Returns:
        tuple -- D0, D1, and D2 index
    """
    D0 = np.mean(dia_ar) 
    D0_var = np.var(dia_ar)
    D0_skew = stats.skew(dia_ar)

    D1 = D0 * (1 + (D0_var / D0**2))
    D2 = (D0 * (1 + (D0_var / (D0**2 + D0_var)) * (2 + ((np.sqrt(D0_var) * D0_skew) / D0))))

    D_Indeces = namedtuple('D_Indeces', ['D0', 'D1', 'D2'])
    d = D_Indeces(D0, D1, D2)

    return d


def measure_all(labeled_img, **kwargs):
    """Call all measurement functions and return data in calibrated units
    
    Arguments:
        labeled_img {np.array} -- binary image, uint16 numpy array
    
    Returns:
        dict -- all measurements for a given image
    """
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
    lm = m * um
    D0 = d.D0 * um
    D1 = d.D1 * um
    D2 = d.D2 * um

    # create a dictionary of all collected data
    data = {"Image_Width(um)": width, "Image_Height(um)" : height, "Obj_Num" : obj_num, 
        "Mean_Area(sq_um)" : mean_area, "Mean_Dia(um)" : mean_dia,
        "Mean_Per(um)" : mean_per, "Total_Airspace_Area(sq_um)" : air_area, 
        "Total_Tissue_Area(sq_um)" : tissue_area, "EXP" : exp, "Lm(um)": lm, "D0" : D0, "D1" : D1, "D2" : D2,
        "Stdev_Area(sq_um)" : stdev_area}
        
    return data



