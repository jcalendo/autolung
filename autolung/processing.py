"""Image Pre-Processing steps

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

The techniques for image preprocessing were derived from:
Muñoz-Barrutia, et al., (2012), Jacob et al., (2009), Parameswaran et al., (2006), and Salon et al., (2015).

RGB images are converted to grayscale by extracting the green channel. Contrast is enhanced. Images are then
thresholded using a local thresholding method ('mean'). Small holes in the thresholded image are then filled. 
the filled image is then used as inout for connected component labelling. Measurements are then made on the 
labeled image.
"""
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_local
from skimage.morphology import remove_small_holes, remove_small_objects, label
from skimage.exposure import equalize_adapthist
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

from measure import measure_all
from metadata import extract_metadata


def convert_to_grey(img):
    """Convert RBG image to gray
    
    Arguments:
        img {ndarray} -- RGB image, image to convert
    
    Returns:
        ndarray -- converted image (grayscale)
    """
    orig = io.imread(img)
    grey = rgb2gray(orig)
    return grey


def enhance_contrast(grey_img):
    """Enhance the contrast of the greyscale image using CLAHE
    
    Arguments:
        grey_img {ndarray} -- grayscale image
    
    Returns:
        ndarray -- grayscale image with enhanced contrast
    """
    return equalize_adapthist(grey_img)


def binarize(grey_img, **kwargs):
    """Apply a threshold to the gray image

    'block size' and 'constant' are gathered from the config file and are 
    used in the thresholding function.
    
    Arguments:
        grey_img {ndarray} -- grayscale image
    
    Returns:
        ndarray -- binary image
    """
    block_size = kwargs.get('block_size')
    constant = kwargs.get('constant')
    local_thresh = threshold_local(grey_img, block_size, method='mean', offset=constant)
    binary_local = grey_img > local_thresh

    return binary_local


def fill_holes(binary_img, **kwargs):
    """Fill holes in the thresholded image

    Fill small holes that are not actual airspaces using morphological operations.
    
    Arguments:
        binary_img {ndarray} -- binary (thresholded) image
    
    Returns:
        ndarray -- binary image with small holes filled
    """
    min_alv_size = kwargs.get('min_alv_size')
    max_speckle_size = kwargs.get('max_speckle_size')

    remove_objects = remove_small_objects(binary_img, min_size=min_alv_size)
    remove_holes = remove_small_holes(remove_objects, area_threshold=max_speckle_size)

    return remove_holes


def label_image(filled_binary_img):
    """Perform connected components labelling
    
    Arguments:
        filled_binary_img {ndarray} -- binary, filled image
    
    Returns:
        ndarray -- Labeled array, where all connected regions are assigned the same integer value
    """
    return label(filled_binary_img)


def preview_process(grey, thresh, filled, labeled):
    """If "Yes", preview the image processing steps for QC
    
    Arguments:
        grey {ndarray} -- grayscale image
        thresh {ndarray} -- thresholded image (binary)
        filled {ndarray} -- binary image with holes filled
        labeled {ndarray} -- labelled image
    """
    # Create mask for the labeled image
    l = np.ma.masked_where(labeled < 0.05, labeled)
    cmap_l = plt.cm.prism
    cmap_l.set_bad(color = 'black')

    _, axarr = plt.subplots(2,2)
    axarr[0, 0].imshow(grey, cmap='gray')
    axarr[0, 1].imshow(thresh, cmap='gray')
    axarr[1, 0].imshow(filled, cmap='gray')
    axarr[1, 1].imshow(l, interpolation='none', cmap=cmap_l)

    axarr[0, 0].set_title('Gray Scale Image')
    axarr[0, 1].set_title('Thresholded Image')
    axarr[1, 0].set_title('Filled Image')
    axarr[1, 1].set_title('Connected Components - Airspaces Colored')

    plt.tight_layout()
    plt.show()


def process_img(img, preview, **kwargs):
    """Perform all pre-processing functions on a given image. 

    The final labelled image is used as input for the measurements module.
    
    Arguments:
        img {ndarray} -- RGB image
        preview {str} -- "Yes" or "No" if preview should be displayed
    
    Returns:
        ndarray -- Labeled array, where all connected regions are assigned the same integer value
    """
    print("Converting image to Grayscale...")
    grey = convert_to_grey(img)
    print("Enhancing contrast...")
    grey_scaled = enhance_contrast(grey)
    print("Thresholding (this may take a while for large images/block_sizes)...")
    binary = binarize(grey_scaled, **kwargs)
    print("Performing morphology operations...")
    filled = fill_holes(binary, **kwargs)
    print("Performing connected components labeling...")
    labeled = label_image(filled)

    if preview == "Yes":
        print("Open Preview - Exit preview window to continue")
        preview_process(grey_scaled, binary, filled, labeled)
    else:
        pass

    return labeled


def process_all(images, preview, **parameters):
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
        p = process_img(img, preview, **parameters)
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