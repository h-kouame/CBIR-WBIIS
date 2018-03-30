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


def main():
    image = load()
    display(image)
    rescaled_image = rescale(image)
    display(rescaled_image)
    save(image, '../Output/original.jpg')
    save(rescaled_image, '../Output/rescaled.jpg')


if __name__ == '__main__':
    if __name__ == '__main__':
        main()

