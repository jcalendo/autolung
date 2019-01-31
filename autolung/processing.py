"""
This module will control all of the image processing steps. 
"""
from skimage import io
from skimage.color import rgb2gray
from skimage.filters import threshold_local
from skimage.morphology import remove_small_holes, remove_small_objects, label
import matplotlib.pyplot as plt
import numpy as np


def convert_to_grey(img):
    """Convert the original RGB image to a greyscale image."""
    orig = io.imread(img)
    gray = rgb2gray(orig)
    return gray


def binarize(grey_img, **kwargs):
    """Threshold the grayscale image. Return the binary image."""
    block_size = kwargs.get('block_size')
    constant = kwargs.get('constant')
    local_thresh = threshold_local(grey_img, block_size, method='mean', offset=constant)
    binary_local = grey_img > local_thresh

    return binary_local


def fill_holes(binary_img, **kwargs):
    """Use morphological operations to fill holes in the binary image."""
    min_alv_size = kwargs.get('min_alv_size')
    max_speckle_size = kwargs.get('max_speckle_size')

    remove_objects = remove_small_objects(binary_img, min_size=min_alv_size)
    remove_holes = remove_small_holes(remove_objects, area_threshold=max_speckle_size)

    return remove_holes


def label_image(filled_binary_img):
    """Perform labeling of the filled binary image"""
    return label(filled_binary_img)


def preview_process(grey, thresh, filled, labeled):
    """If the preview option is selected show a four panel display of the
    processed images"""
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


def process(img, preview, **kwargs):
    """Perform the processing pipeline. Return the filled image."""
    print("Converting image to Grayscale...")
    grey = convert_to_grey(img)
    print("Thresholding (this make take a while for large images/block_sizes)...")
    binary = binarize(grey, **kwargs)
    print("Performing morphology operations...")
    filled = fill_holes(binary, **kwargs)
    print("Performing connected components labeling...")
    labeled = label_image(filled)

    if preview == "Yes":
        print("Open Preview - Exit preview window to continue")
        preview_process(grey, binary, filled, labeled)
    else:
        pass

    return labeled