import numpy as np
import cv2
import pywt
from PIL import Image


def load(path='../Data/image.orig - original/400.jpg'):
    image = cv2.imread(path)
    return image


def display(image, frame_name='image'):
    cv2.imshow(frame_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_image(path, frame_name):
    image = load(path)
    display(image, frame_name)


def display_component(component, name='component'):
    cv2.imshow(name, component)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save(image, path='../Output/out.jpg'):
    cv2.imwrite(path, image)


def rescale(image_in, width=128, height=128):
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


def preprocess(path='../Data/image.orig - original/400.jpg', width=128, height=128, bits_per_pixel=24):
    image = load(path)
    rescaled_image = rescale(image, width, height)
    components = rgb_to_components(rescaled_image, bits_per_pixel)
    return components


def wavelet_transform(data3D, w_type='db8', cutoff=16):
    C1, C2, C3 = data3D[0], data3D[1], data3D[2]
    # get the wavelet coefficients
    coeff_C1 = pywt.wavedec2(C1, wavelet=w_type)
    coeff_C2 = pywt.wavedec2(C2, wavelet=w_type)
    coeff_C3 = pywt.wavedec2(C3, wavelet=w_type)
    # get the wavelet approximation of the 4th level
    W1, W2, W3 = coeff_C1[0], coeff_C2[0], coeff_C3[0]
    # throw away the 3rd level details
    # details1, details2, details3 = coeff_C1[1], coeff_C2[1], coeff_C3[1]
    # get the 16x16 upper left coefficients & Throw away higher coefficients
    # lower_W1 = [[entire_W1[0][i][j] for j in range(cutoff)]
    #                     for i in range(cutoff)]
    # lower_W2 = [[entire_W2[0][i][j] for j in range(cutoff)]
    #             for i in range(cutoff)]
    # lower_W3 = [[entire_W3[i][j] for j in range(cutoff)]
    #             for i in range(cutoff)]

    # coefficients = [lower_W1, lower_W2, lower_W3]
    # return coefficients
    # W1 <==> 8x8 & W1 + details1 <==> 16x16 but are currently 29x29 and 58x58
    return {'C1': W1, 'C2': W2, 'C3': W3}


def standard_dev(data):
    W1, W2, W3 = data['C1'], data['C2'], data['C3']
    return [np.std(W1), np.std(W2), np.std(W3)]


def form_feature_vector(components, w_type='db8'):
    wt = wavelet_transform(components, w_type)
    # upper_left = get_upper_left_coefficients(wt)
    std = standard_dev(wt)
    return {'std': std, 'wt': wt}


# def join_coefficients(wt):
#     height = len(wt[0][0]) + len(wt[1][0])
#     width = len(wt[0][0][0]) + len(wt[1][0][0])
#     components = np.zeros((3, height, width))
#
#     for c in range(3):
#         W = wt[0][c]
#         details = wt[1][c]
#         for


def get_upper_left_coefficients(coefficients):
    return coefficients[0]


def image_from_array(data):
    image = Image.fromarray(data)
    return image


def main():
    image = load()
    # display(image)
    rescaled_image = rescale(image, 128, 128)
    # print "rgb values"
    # print rescaled_image
    components = rgb_to_components(rescaled_image)
    wt = wavelet_transform(components)
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

