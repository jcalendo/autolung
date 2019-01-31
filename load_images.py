"""
This module loads files from the specified directory
"""
import os


def collect(input_dir):
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