import setup
import image_ops as ops
import search as s
import os
import sys
import getopt
import shutil
import time
import gc


def main(argv):
    feature_dir = '../Database/'
    image_db_dir = '../Data/image.orig/'
    # image_db_dir = '../Data/image.vary.jpg/'
    # image_db_dir = '../Data/image.orig - original/'

    query_image = '0.jpg'
    number_of_images = 100
    pixel_depth = 24
    out_image_dir = "../Output/"
    percent = 50
    height, width = 128, 128

    try:
        opts, args = getopt.getopt(argv, "hq:n:i:f:d:p:o:y:x:", ["qimage=", "nimages=", "idb=", "fdb=", "percent", "pdepth=", "opath=", "ydim=", "xdim="])
    except getopt.GetoptError:
        print 'python driver.py -q <query image name> -n <number of images to return> ' \
              '-i <image database path> -f <feature vector database directory> ' \
              '-d <image database path> -p <image pixel depth> -o <output image directory> ' \
              '-y <rescaling height> -x <rescaling width>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'python driver.py -q <query image name> -n <number of images to return> ' \
              '-i <image database path> -f <feature vector database directory> ' \
                  '-d <image database path> -p <image pixel depth> -o <output image directory>' \
                  ' -y <rescaling height> -x <rescaling width>'
            sys.exit()
        elif opt in ("-q", "--qimage"):
            query_image = arg
        elif opt in ("-n", "--nimages"):
            number_of_images = int(arg)
        elif opt in ("-i", "--idb"):
            image_db_dir = arg
        elif opt in ("-f", "--fdb"):
            feature_dir = arg
        elif opt in ("-p", "--percent"):
            percent = int(arg)
        elif opt in ("-d", "--pdepth"):
            width = int(arg)
        elif opt in ("-o", "--opath"):
            out_image_dir = arg
        elif opt in ("-y", "--ydim"):
            height = int(arg)
        elif opt in ("-x", "--xdim"):
            width = int(arg)
    if width >= 256 and height >= 256:
        level = 4
    else:
        level = 3
    query_imagepath = image_db_dir + query_image

    if gc.isenabled():
        gc.disable()
    start = time.time()

    query_components = ops.preprocess(query_imagepath, width=width, height=height, bits_per_pixel=pixel_depth)
    query_features = ops.form_feature_vector(query_components, level=level)
    query_std = query_features['std']
    query_wt = query_features['wt']

    db_std = setup.load_db_std(base_dir=feature_dir)
    first_matches = s.std_search(db_std, query_std, percent=percent)
    print "number of matches on stage 1:", ' ', len(first_matches), 'out of', len(db_std)
    # print first_matches

    db_wt = setup.load_images_wt(first_matches)
    distances = s.compute_distances(query_wt, db_wt)
    matches = s.get_matches(distances, number_of_images)
    counter = 0
    for match in matches:
        if -1 < int(match[:-4]) < 100:
            counter = counter + 1
    print "accuracy ", 100*counter/100.0
    end = time.time() - start
    gc.enable()
    print "Time taken to find matches: ", end

    if os.path.exists(out_image_dir):
        shutil.rmtree(out_image_dir)
    os.makedirs(out_image_dir)
    print "Best matches in order:"
    ops.display_image(query_imagepath, 'Query_Image.jpg')
    out_image_path = out_image_dir + 'Query_Image.jpg'
    ops.save_image(out_image_path=out_image_path, imagename=query_image, db_base_dir=image_db_dir)
    print matches
    for i in range(len(matches)):
        imagename = matches[i]
        imagepath = image_db_dir + imagename
        print imagename
        frame_name = 'Match_' + str(i) + '.jpg'
        ops.display_image(imagepath, frame_name)
        out_image_path = out_image_dir + frame_name
        ops.save_image(out_image_path=out_image_path, imagename=imagename, db_base_dir=image_db_dir)


if __name__ == '__main__':
    if gc.isenabled():
        gc.disable()
    tic = time.time()
    main(sys.argv[1:])
    toc = time.time() - tic
    print "Total interaction time: ", toc, " seconds"
    gc.enable()
