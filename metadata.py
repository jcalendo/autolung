"""
this script will extract metadat from the configuration file and the image filename
and then return that data as a dictionary to be incorporated into the final results
spreadsheet
"""
import os
import numpy as np


def collect_images(input_dir):
    """iterate through the input directory and collect image files into a list.
    return the list for processing if files exist"""

    # create empty list for images that wil be processed
    to_process = []

    # define allowed extensions
    ext = [".tif"]

    for file in os.listdir(input_dir):
        if file.endswith(tuple(ext)):
            to_process.append(os.path.join(input_dir, file))
        else:
            print("{} is not compatible for image processing. Must be .tif".format(file))

    return to_process


def get_id(fname):
    """Extract the first field (animal_id) from the file name"""
    try:
        animal_id = fname.split('-')[0].strip()
    except:
        print("ERROR: Could not extract animal_ID from {}".format(fname))
        print("animal_ID set to 'NaN in output")
        animal_id = np.nan
    
    return animal_id


def get_location(fname):
    """Extract the second field (location) from the file name"""
    try:
        location = fname.split('-')[1].strip()
    except:
        print("ERROR: Could not extract location from {}".format(fname))
        print("location set to 'NaN' in output")
        location = np.nan
    
    return location


def get_img_num(fname):
    """Extract the third field (image number) from the file name"""
    try:
        img_num = int(fname.split('-')[2][:-4])
    except:
        print("ERROR: Could not extract img_num from {}".format(fname))
        print("img_num set to 'NaN' in output")
        img_num = np.nan
    
    return img_num


def extract_metadata(fpath, **kwargs):
        """Parse the fpath to the image to obtain information about the animal
        
        Files should be named in a standard format (specific to our lab)
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