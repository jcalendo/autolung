"""Image Pre-Processing steps

(c) 2019 Gennaro Calendo, Laboratory of Marla R. Wolfson, MS, PhD at Lewis Katz School of Medicine at Temple University

The techniques for image preprocessing were derived from:
Muñoz-Barrutia, et al., (2012), Jacob et al., (2009), Parameswaran et al., (2006), and Salon et al., (2015).

RGB images are converted to grayscale by extracting the green channel. Contrast is enhanced. Images are then
thresholded using a local thresholding method ('mean'). Small holes in the thresholded image are then filled. 
the filled image is then used as inout for connected component labelling. Measurements are then made on the 
labeled image.
"""
from pathlib import Path
import warnings

from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_local
from skimage.morphology import remove_small_holes, remove_small_objects, label
from skimage.exposure import equalize_adapthist
import matplotlib.pyplot as plt
import numpy as np

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
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        enhanced = equalize_adapthist(grey_img)

    return enhanced


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
    met = kwargs.get('method')

    local_thresh = threshold_local(grey_img, block_size, method=met, offset=constant)
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


def preview_process(img, grey, thresh, filled, labeled, **kwargs):
    """If "Yes", save the image processing steps for QC

    By default, saves the image in the same location as the original image in a new folder called QC
    
    Arguments:
        grey {ndarray} -- grayscale image
        thresh {ndarray} -- thresholded image (binary)
        filled {ndarray} -- binary image with holes filled
        labeled {ndarray} -- labelled image
    """
    # create new folder 'QC' in images dir and save preview figure as jpg files
    p = Path(img)
    Path(p.parent.joinpath('QC')).mkdir(parents=True, exist_ok=True)
    savename = str(p.stem) + ".jpg"
    save_loc = p.parent.joinpath('QC', savename)

    # Create mask for the labeled image
    l = np.ma.masked_where(labeled < 0.05, labeled)
    cmap_l = plt.cm.get_cmap('prism')
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
    figure = plt.gcf()
    figure.set_size_inches(10, 8)

    print(f"Saving QC image to {save_loc}...")
   
    plt.savefig(save_loc, dpi=800)
    plt.close()


def process_img(img, preview, **kwargs):
    """Perform all pre-processing functions on a given image. 

    The final labelled image is used as input for the measurements module.
    
    Arguments:
        img {str} -- Path to image to be processed
        preview {str} -- "Yes" or "No" if preview should be displayed
    
    Returns:
        ndarray -- Labeled array, where all connected regions are assigned the same integer value
    """
    print("Converting image to grayscale...")
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
        preview_process(img, grey_scaled, binary, filled, labeled)

    return labeled
