"""Collect images from the specified directory
(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University
"""
from pathlib import Path


def collect(input_dir):
    """Iterate through image directory collecting image paths for processing
    This method currently only accepts .tif images
    
    Arguments:
        input_dir {str} -- path to the directory containing images
    
    Returns:
        list -- list of image paths to process
    """

    p = Path(input_dir)
    image_files = [f.absolute() for f in p.glob('**/*.tif') if f.is_file()]

    return image_files