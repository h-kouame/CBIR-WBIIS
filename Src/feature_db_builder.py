import image_ops as ops
import os
import numpy as np


def preprocess(dir_path = "../Data/image.orig/", width=128, height=128, bits_per_pixel=24):
    components = []
    for imagename in os.listdir(dir_path):
        components.append(ops.preprocess(dir_path + imagename, width, height, bits_per_pixel))
    return components


def wavelet_transform(components):
    coefficients = []
    for i in components:
        coefficients.append(ops.wavelet_transform(i))
    print len(coefficients[0][0])
    return coefficients


def get_upper_left(coefficients):
    return coefficients[:][0]


def standard_dev(data):
    std_dev = []
    for i in data:
        std_dev.append(ops.standard_dev(i))
    return std_dev


def main():
    components = preprocess()
    wt = wavelet_transform(components)
    ul = get_upper_left(components)
    std = standard_dev(ul)
    print std[0]
    print std[1]


if __name__ == '__main__':
    main()


