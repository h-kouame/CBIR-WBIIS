import image_ops as ops
import os
import numpy as np


def preprocess(dir_path = "../Data/image.orig/", width=2, height=2, bits_per_pixel=24):
    components = []
    for imagename in os.listdir(dir_path):
        components.append(ops.preprocess(dir_path + imagename, width, height, bits_per_pixel))
    return components


def wavelet_transform(components):
    coefficients = []
    for i in components:
        coefficients.append(ops.wavelet_transform(components))
    return coefficients


def main():
    # components = preprocess()
    # wt = wavelet_transform(components)
    # print wt


if __name__ == '__main__':
    main()


