import numpy as np
import cv2
import pywt
from PIL import Image
import os


def load(path='../Data/image.orig - original/400.jpg'):
    image = cv2.imread(path)
    return image


def display(image, frame_name='image'):
    cv2.imshow(frame_name, image)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


def display_image(path, frame_name):
    image = load(path)
    display(image, frame_name)


def display_component(component, name='component'):
    cv2.imshow(name, component)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


def save(image, path='../Output/out.jpg'):
    cv2.imwrite(path, image)


def save_image(out_image_path, imagename="out.jpg", db_base_dir='../Data/image.orig - original/400.jpg'):
    image_path = db_base_dir + imagename
    image = load(image_path)
    save(image, out_image_path)


def rescale(image_in, width=256, height=256):
    # Bipolar interpolation: experiment with CV_INTER_AREA
    image_out = cv2.resize(image_in, (width, height), 0, 0)
    return image_out


def rgb_to_components(rgb_image, bits_per_pixel=24):
    max_pixel_value = pow(2, bits_per_pixel)
    dimensions = rgb_image.shape
    height, width = dimensions[0], dimensions[1]
    components = np.zeros((3, height, width))
    # C1[x][y] = components[0][x][y] = np.mean(rgb_image[x][y])
    components[0][:][:] = np.mean(rgb_image[:][:], 2)
    for x in range(height):
        for y in range(width):
            # components[0][x][y] = np.mean(rgb_image[x][y])
            # C2[x][y]
            components[1][x][y] = (rgb_image[x][y][0] + max_pixel_value - rgb_image[x][y][2]) / 2
            # C3[x][y]
            components[2][x][y] = (rgb_image[x][y][0] +
                                         2 * (max_pixel_value - rgb_image[x][y][1]) +
                                         rgb_image[x][y][2]) / 4
    return components


def preprocess(path='../Data/image.orig - original/400.jpg', width=256, height=256, bits_per_pixel=24):
    image = load(path)
    rescaled_image = rescale(image, width, height)
    components = rgb_to_components(rescaled_image, bits_per_pixel)
    return components


def wavelet_transform(data3D, w_type='db8', mode='per', level=4):
    C1, C2, C3 = data3D[0], data3D[1], data3D[2]
    # get the wavelet coefficients
    coeff_C1 = pywt.wavedec2(C1, wavelet=w_type, mode=mode, level=level)
    coeff_C2 = pywt.wavedec2(C2, wavelet=w_type, mode=mode, level=level)
    coeff_C3 = pywt.wavedec2(C3, wavelet=w_type, mode=mode, level=level)
    # get the wavelet approximation of the 4th level
    W1, W2, W3 = coeff_C1[0], coeff_C2[0], coeff_C3[0]
    # throw away the 3rd level details
    details1, details2, details3 = coeff_C1[1], coeff_C2[1], coeff_C3[1]
    return [[W1, W2, W3], [details1, details2, details3]]


def rearrange_wt(wt):
    cA = {"C1": wt[0][0], "C2": wt[0][1], "C3": wt[0][2]}
    cH = {"C1":wt[1][0][0], "C2":wt[1][1][0], "C3":wt[1][2][0]}
    cV = {"C1": wt[1][0][1], "C2": wt[1][1][1], "C3": wt[1][2][1]}
    cD = {"C1": wt[1][0][2], "C2": wt[1][1][2], "C3": wt[1][2][2]}
    return {"cA": cA, "cH": cH, "cV": cV, "cD": cD}


def standard_dev(data):
    W1, W2, W3 = data[0], data[1], data[2]
    return [np.std(W1), np.std(W2), np.std(W3)]


def form_feature_vector(components, level=3):
    wt = wavelet_transform(components, level=level)
    upper_left = get_upper_left_coefficients(wt)
    std = standard_dev(upper_left)
    temp = rearrange_wt(wt)
    return {'std': std, 'wt':temp}


def get_upper_left_coefficients(coefficients):
    return coefficients[0]


def image_from_array(data):
    image = Image.fromarray(data)
    return image


# for debugging
def main():
    image = load()
    # display(image)
    rescaled_image = rescale(image, 128, 128)
    # print "rgb values"
    # print rescaled_image
    components = rgb_to_components(rescaled_image)
    wt = wavelet_transform(components)
    print wt[0][0]
    # display(image)
    # c = np.array(components[1])
    # print c
    # print coeffs
    # print "component values"
    # print components_image
    # display(rescaled_image)
    # save(image, '../Output/original.jpg')
    # save(rescaled_image, '../Output/rescaled.jpg')


if __name__ == '__main__':
        main()

