import search as s
import os
import image_ops as ops


def load_db_std(base_dir='../Database/', filename='standard_deviation.csv'):
    path = base_dir + filename
    std_dev = {}
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        temp = line.split(',')
        std_dev[temp[0]] = clean_line(temp[1:])
    return std_dev


def load_wt(path='../Database/Wavelets/807.csv'):
    wt = {'cA': {'C1': [], 'C2': [], 'C3': []},
          'cH': {'C1': [], 'C2': [], 'C3': []},
          'cV': {'C1': [], 'C2': [], 'C3': []},
          'cD': {'C1': [], 'C2': [], 'C3': []}}
    with open(path, 'r') as f:
        lines = f.readlines()
    coeff_names = ['cA', 'cH', 'cV', 'cD']
    comp_names = ['C1', 'C2', 'C3']
    for line in lines:
        line = line.strip('\n')
        if line in coeff_names:
            coeff_name = line
            continue
        if line in comp_names:
            comp_name = line
            continue
    # [:-1] trim last empty element
        wt[coeff_name][comp_name].append(line.split(',')[:-1])

    return wt


def load_db_wt(base_dir='../Database/Wavelets/'):
    wts = {}
    for filename in os.listdir(base_dir):
        wt = load_wt(base_dir + filename)
        imagename = filename[:-3] + 'jpg'
        wts[imagename] = wt
    return wts


def load_images_wt(imagenames, base_dir='../Database/Wavelets/'):
    wts = {}
    for name in imagenames:
        path = base_dir + name[:-3] + 'csv'
        wt = load_wt(path)
        wts[name] = wt
    return wts


def clean_line(line):
    new_line = []
    for elt in line:
        elt = elt.strip()
        elt = elt.strip('\n')
        new_line.append(float(elt))
    return new_line


def main():
    base_dir = '../Data/image.orig/'
    # base_dir = '../Data/image.orig - original/'
    query_image = '204.jpg'
    path = base_dir + query_image
    query_components = ops.preprocess(path, width=128, height=128, bits_per_pixel=24)
    query_features = ops.form_feature_vector(query_components)
    query_std = query_features['std']
    query_wt = query_features['wt']

    db_std = load_db_std()
    percent = 50
    first_matches = s.std_search(db_std, query_std, percent=percent)
    print "number of matches on stage 1:", ' ', len(first_matches)
    print first_matches

    # db_wt = load_db_wt()
    db_wt = load_images_wt(first_matches)
    distances = s.compute_distances(query_wt, db_wt)
    matches = s.get_matches(distances, 10)
    for imagename in matches:
        imagepath = base_dir + imagename
        print imagename
        ops.display_image(imagepath, imagename)


if __name__ == '__main__':
    main()
