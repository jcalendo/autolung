"""Main app and GUI

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Controls the main app and gui for the autloung program
"""
from pathlib import Path
from gooey import Gooey
from gooey import GooeyParser

from load_config import load_settings
from processing import process
from load_images import collect
from measure import measure_all
from metadata import extract_metadata
from export import write_output


def process_dataset(images, preview, **parameters):
    """Perform processing steps on all images
    
    Arguments:
        images {list} -- list of image paths to be processed
        preview {str} -- "Yes" or "No" choice to preview processing steps
    
    Returns:
        list -- list of the associated data (dictionaries) for each image
    """
    data = []
    num_images = len(images)
    for i, img in enumerate(images, start=1):
        img_name = Path(img).name

        print(f"Processing image {i}/{num_images}...")
        print(f"Processing {img_name}...")
        p = process(img, preview, **parameters)
        print("Done.\n")
        print(f"Measuring airspace statistics on {img_name}...")
        d = measure_all(p, **parameters)
        print("Done.\n")
        print(f"Extracting metadata from {img_name}...")
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
