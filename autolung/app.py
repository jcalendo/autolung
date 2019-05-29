"""
This file will control the main program and GUI
"""
from gooey import Gooey
from gooey import GooeyParser
import matplotlib.pyplot as plt
import matplotlib
import skimage.io
import numpy as np

from load_config import load_settings
from processing import process
from load_images import collect
from measure import measure_all
from metadata import extract_metadata
from export import write_output


def process_dataset(images, preview, **parameters):
    """Process all images in the dataset. return list of dictionaries containing the data"""
    data = []
    num_images = len(images)
    for i, img in enumerate(images, start=1):
        print("Processing image {}/{}...".format(i, num_images))
        print("Processing {}...".format(img))
        p = process(img, preview, **parameters)
        print("Done.\n")
        print("Measuring airspace statistics on {}...".format(img))
        d = measure_all(p, **parameters)
        print("Done.\n")
        print("Extracting metadata from {}...".format(img))
        md = extract_metadata(img, **parameters)
        print("Done.\n")

        results = {**md, **d}
        data.append(results)

    return data


@Gooey(program_name="autolung", default_size=(700, 530))
def main():
    parser = GooeyParser(description="Perform automated lung image analysis.\nWritten by Gennaro Calendo for the Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine\nTemple University, 2019")
    parser.add_argument("images", help="path to the directory of images to be analyzed", widget='DirChooser')
    parser.add_argument("output_path", help="path the where you want to save the output file", widget="DirChooser")
    parser.add_argument("config_file", help="The configuration file for this image set", widget="FileChooser")
    parser.add_argument("preview", help="Select if you would like to preview the processing steps", choices=['Yes', 'No'], default="No")
    args = parser.parse_args()

    outpath = args.output_path
    params = load_settings(args.config_file)
    images = collect(args.images)
    data = process_dataset(images, args.preview, **params)
    write_output(data, outpath)


if __name__ == "__main__":
    main()
