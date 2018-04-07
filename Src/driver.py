import search as s
import os
import image_ops as ops


def load_std(base_dir='../Database/', filename='standard_deviation.csv'):
    path = base_dir + filename
    std_dev, lines = [], []
    with open(path, 'r') as f:
        for line in f:
            temp = line.split(',')
            std_dev.append(clean_line(temp))
    return std_dev


def load_wt(base_dir='../Database/Wavelets/', filename='807.csv'):
    path = base_dir + filename[:-3] + 'csv'
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
        wt = load_wt(base_dir, filename)
        imagename = filename[:-3] + 'jpg'
        wts[imagename] = wt
    return wts


def clean_line(line):
    new_line = []
    for elt in line:
        elt = elt.strip()
        elt = elt.strip('\n')
        new_line.append(float(elt))
    return new_line


def main():
    # db_std = load_std()
    # percent = 30
    # matches = s.query(db_std, percent=percent, imagename='807.jpg')
    # print "number of matches", ' ', len(matches)
    # print matches

    query_wt = load_wt(filename='400.csv')
    db_wt = load_db_wt()
    distances = s.compute_distances(query_wt, db_wt)
    matches = s.get_matches(distances, 100)
    base_dir = '../Data/image.orig - original/'
    for imagename in matches:
        print imagename
        path = base_dir + imagename
        ops.display_image(path, imagename)


if __name__ == '__main__':
    main()
