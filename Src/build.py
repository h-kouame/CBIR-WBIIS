import image_ops as ops
import os
import sys
import getopt
import time
import gc


def preprocess(base_dir="../Data/image.orig/", width=128, height=128, bits_per_pixel=24):
    components = {}
    for imagename in os.listdir(base_dir):
        components[imagename] = ops.preprocess(base_dir + imagename, width, height, bits_per_pixel)
    return components


def wavelet_transform(components, w_type='db8', mode='per', level=3):
    coefficients = {}
    imagenames = components.keys()
    for name in imagenames:
        C = components[name]
        coefficients[name] = ops.wavelet_transform(C, w_type, mode, level)
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


def save_wt(coefficients, base_dir='../Database/'):
    wt_dir = base_dir + 'Wavelets/'
    if not os.path.exists(wt_dir):
        os.makedirs(wt_dir)
    imagenames = coefficients.keys()
    for imagename in imagenames:
        path = wt_dir + imagename[:-3] + "csv"
        wt = coefficients[imagename]
        data = ops.rearrange_wt(wt)
        stream = ''
        coeff_names = data.keys()
        for coeff_name in coeff_names:
            stream = stream + coeff_name + '\n'
            components = data[coeff_name]
            comp_names = components.keys()
            for comp_name in comp_names:
                stream = stream + comp_name + '\n'
                component_weights = components[comp_name]
                height, width = len(component_weights), len(component_weights[0])
                for y in range(height):
                    for x in range(width):
                        stream = stream + str(component_weights[y][x]) + ','
                    stream = stream + '\n'

        if os.path.isfile(path):
            os.remove(path)
        with open(path, 'a') as f:
            f.write(stream)


def main(argv):
    height = 128
    width = 128
    # image_db_path = '../Data/image.orig - original/'
    image_db_path = '../Data/image.orig/'
    out_wt_dir = '../Database/'
    pixel_depth = 24
    try:
        opts, args = getopt.getopt(argv, "hi:y:x:d:o:", ["idb=", "ydim=", "xdim=", "pdepth=" "odb="])
    except getopt.GetoptError:
        print 'build.py -i <image database path> -y <rescaling height> -x <rescaling width> ' \
              '-o <output feature directory>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'build.py -i <image database path> -y <rescaling height> -x <rescaling width> ' \
                  '-o <output feature directory>'
            sys.exit()
        elif opt in ("-i", "--idb"):
            image_db_path = arg
        elif opt in ("-y", "--ydim"):
            height = int(arg)
        elif opt in ("-x", "--xdim"):
            width = int(arg)
        elif opt in ("-d", "--pdepth"):
            pixel_depth = int(arg)
        elif opt in ("-o", "--odb"):
            out_wt_dir = arg

    components = preprocess(base_dir=image_db_path, width=width, height=height, bits_per_pixel=pixel_depth)

    if width >= 256 and height >= 256:
        level = 4
    else:
        level = 3
    if gc.isenabled():
        gc.disable()
    start = time.time()
    wt = wavelet_transform(components, w_type="db8", mode="per", level=level)
    end = time.time() - start
    print "Wavelet transform computation took: ", end, " seconds"
    gc.enable()
    ul = get_upper_left_coefficients(wt)
    std = standard_dev(ul)
    save_wt(wt, base_dir=out_wt_dir)
    save_std(std, filename='standard_deviation.csv', base_dir=out_wt_dir)


if __name__ == '__main__':
    if gc.isenabled():
        gc.disable()
    tic = time.time()
    main(sys.argv[1:])
    toc = time.time() - tic
    print "Feature vector computation and storing took: ", toc, " seconds"
    gc.enable()

