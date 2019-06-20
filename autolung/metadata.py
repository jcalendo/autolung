"""Extract metadata information from image filenames

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Collect metadata information from the image filenames and config file. 

NOTE: filename format is specific to our lab and follows the convention "[Animal_ID]-[Location]-[Image_Number].tif"
"""
import os

import numpy as np


def get_id(fname):
    """Extract the first field (animal_id) from the file name
    
    Arguments:
        fname {str} --  image filename
    
    Returns:
        str -- first field of the file name
    """
    try:
        animal_id = fname.split('-')[0].strip()
    except:
        print(f"ERROR: Could not extract animal_ID from {fname}")
        print("animal_ID set to 'NaN in output")
        animal_id = np.nan
    
    return animal_id


def get_location(fname):
    """Extract the second field (location) from the file name
    
    Arguments:
        fname {str} -- image filename
    
    Returns:
        str -- second field of the file name
    """
    try:
        location = fname.split('-')[1].strip()
    except:
        print(f"ERROR: Could not extract location from {fname}")
        print("location set to 'NaN' in output")
        location = np.nan
    
    return location


def get_img_num(fname):
    """Extract the third field (image number) from the file name
    
    Arguments:
        fname {str} -- image filename
    
    Returns:
        str -- third field of the file name
    """
    try:
        img_num = int(fname.split('-')[2][:-4])
    except:
        print(f"ERROR: Could not extract img_num from {fname}")
        print("img_num set to 'NaN' in output")
        img_num = np.nan
    
    return img_num


def extract_metadata(fpath, **kwargs):
        """Combine all above functions to extract metadata from file name
        
        Arguments:
            fpath {str} -- image file name
        
        Returns:
            dict -- dict of image file metadata extracted from file name
        """
        fname = os.path.basename(fpath)

        animal_id = get_id(fname)
        location = get_location(fname)
        img_num = get_img_num(fname)
        species = kwargs.get('species')
        mag = kwargs.get('magnification')
        field = kwargs.get('fixed_field')
        scale = kwargs.get('scale')

        md_dict = {"FileName" : fname,
                   "Animal_id" : animal_id,
                   "Location" : location,
                   "Img_num" : img_num,
                   "Species" : species,
                   "Magnification" : mag,
                   "Fixed_Field" : field,
                   "Scale(px/um)" : scale}
        
        return md_dict