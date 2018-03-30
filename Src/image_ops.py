import numpy as np
import cv2


def load(path='../Data/image.orig/121.jpg'):
    image = cv2.imread(path)
    return image


def display(image, name='image'):
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save(image, path='../Output/out.jpg'):
    cv2.imwrite(path, image)


def rescale(image_in, width = 128, height = 128):
    # Bipolar interpolation: experiment with CV_INTER_AREA
    image_out = cv2.resize(image_in, (width, height), 0, 0)
    return image_out


def rgb_to_components(rgb_image, bits_per_pixel = 24):
    max_pixel_value = pow(2, bits_per_pixel)
    dimensions = rgb_image.shape
    height, width = dimensions[0], dimensions[1]
    components_image = np.zeros((3, height, width))
    # C1[x][y] = components_image[0][x][y] = np.mean(rgb_image[x][y])
    components_image[0][:][:] = np.mean(rgb_image[:][:], 2)
    for x in range(height):
        for y in range(width):
            # components_image[0][x][y] = np.mean(rgb_image[x][y])
            # C2[x][y]
            components_image[1][x][y] = (rgb_image[x][y][0] + max_pixel_value - rgb_image[x][y][2]) / 2
            # C3[x][y]
            components_image[2][x][y] = (rgb_image[x][y][0] +
                                         2 * (max_pixel_value - rgb_image[x][y][1]) +
                                         rgb_image[x][y][2]) / 4
    return components_image


def main():
    image = load()
    display(image)
    rescaled_image = rescale(image, 2, 2)
    # print "rgb values"
    # print rescaled_image
    # components_image = rgb_to_components(rescaled_image)
    # print "component values"
    # print components_image
    # display(rescaled_image)
    # save(image, '../Output/original.jpg')
    # save(rescaled_image, '../Output/rescaled.jpg')


if __name__ == '__main__':
    if __name__ == '__main__':
        main()

