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


def main():
    image = load()
    display(image)
    save(image)


if __name__ == '__main__':
    if __name__ == '__main__':
        main()