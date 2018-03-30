import image_ops as ops
import os


# def load_rescale(dir_path = "../Data/image.orig/"):
#     images = []
#     for imagename in os.listdir(dir_path):
#         imagepath = dir_path + imagename
#         print imagepath
#         image = ops.load(imagepath)
#         rescaled_image = ops.rescale(image)
#         images.append(image)
#         ops.display(rescaled_image, imagename)
#     return images


# def get_components(images):
#     components = [len(images)]
#     for i in range(len(images)):
#         components[i] = ops.rgb_to_components(images[i])
#     return components


def preprocess(dir_path = "../Data/image.orig/"):
    components = []
    for imagename in os.listdir(dir_path):
        components.append(ops.preprocess(dir_path + imagename))
    return components


def main():
    components = preprocess()
    components.shape


if __name__ == '__main__':
    main()


