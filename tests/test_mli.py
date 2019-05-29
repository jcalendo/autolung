"""
unit test for the Mean Linear Intercept function

input images to this function are all binary and thus can be tested using np.arrays
"""
import numpy as np
from autolung.measure import mli


# test on full array simulated as 100x100 image
img_100 = np.ones((100,100))
def test_1():
    assert mli(img_100) == 100.0

# test on array with varying lengths of consecutive 'pixels'
img_threes = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]])
def test_2():
    assert mli(img_threes) == 3.0


# test on array where consecutive stretches differ in length
img_scattered = np.array([[1, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [1, 1, 1, 1, 0, 0, 0, 0, 0, 1], 
                          [1, 1, 1, 1, 1, 1, 0, 0, 0, 0], 
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                          [1, 1, 0, 0, 1, 1, 1, 0, 0, 0], 
                          [0, 1, 0, 1, 1, 0, 0, 0, 1, 1]])  
# function should return the mean of the consecutive lengths [2,4,1,6,2,3,1,2,2]
def test_3():
    assert mli(img_scattered) == np.mean([[2,4,1,6,2,3,1,2,2]])


