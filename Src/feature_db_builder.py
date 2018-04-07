import image_ops as ops
import os
import numpy as np


def preprocess(base_dir="../Data/image.orig/", width=128, height=128, bits_per_pixel=24):
    components = {}
    for imagename in os.listdir(base_dir):
        components[imagename] = ops.preprocess(base_dir + imagename, width, height, bits_per_pixel)
    return components


def wavelet_transform(components):
    coefficients = {}
    imagenames = components.keys()
    for name in imagenames:
        C = components[name]
        coefficients[name] = ops.wavelet_transform(C)
    return coefficients


def get_upper_left_coefficients(coefficients):
    upper_lefts = {}
    imagenames = coefficients.keys()
    for name in imagenames:
        upper_lefts[name] = coefficients[name][0]
    return upper_lefts


def standard_dev(upper_lefts):
    std_dev = {}
    imagenames = upper_lefts.keys()
    for name in imagenames:
        std_dev[name] = ops.standard_dev(upper_lefts[name])
    return std_dev


# def form_feature_vector(components):
#     wt = wavelet_transform(components)
#     upper_lefts = get_upper_left_coefficients(wt)
#     std = standard_dev(upper_lefts)
#     features = {}
#     features[]


def save_features(features, std_filename='standard_deviation.csv', base_dir='../Database/'):
    std = features['std']
    save_std(std, std_filename, base_dir)


def save_std(std, filename='standard_deviation.csv', base_dir='../Database/'):
    path = base_dir + filename
    imagenames = std.keys()
    stream = ''
    for name in imagenames:
        temp = str(std[name])
        stream = stream + name + "," + temp[1:-1] + '\n'
    if os.path.isfile(path):
        os.remove(path)
    with open(path, 'a') as f:
        f.write(stream)


def save_wt(coefficients, base_dir='../Database/Wavelets/'):
    imagenames = coefficients.keys()
    for imagename in imagenames:
        path = base_dir + imagename[:-3] + "csv"
        wt = coefficients[imagename]
        stream = ''
        comp_names = wt.keys()
        for comp_name in comp_names:
            stream = stream + comp_name + '\n'
            component_weights = wt[comp_name]
            height, width = len(component_weights), len(component_weights[0])
            for y in range(height):
                for x in range(width):
                    stream = stream + str(component_weights[y][x]) + ','
                stream = stream + '\n'

        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'a') as f:
            f.write(stream)


def main():
    components = preprocess(base_dir='../Data/image.orig - original/')
    # components = preprocess(base_dir='../Data/image.orig/')
    wt = wavelet_transform(components)
    save_wt(wt)
    # ul = get_upper_left_coefficients(wt)
    std = standard_dev(wt)
    save_std(std, filename='standard_deviation.csv')


if __name__ == '__main__':
    main()


