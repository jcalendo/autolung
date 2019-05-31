"""Main app and GUI

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

Controls the main app and gui for the autloung program
"""
from gooey import Gooey
from gooey import GooeyParser

from load_config import load_settings
from load_images import collect
from processing import process_all
from export import write_output


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
    data = process_all(images, args.preview, **params)
    write_output(data, outpath)


if __name__ == "__main__":
    main()
