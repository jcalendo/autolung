"""Collect images from the specified directory

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University
"""
import os


def collect(input_dir):
    """Iterate through image directory collecting image paths for processing
    
    Arguments:
        input_dir {str} -- path to the directory containing images
    
    Returns:
        list -- list of image paths to process
    """

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