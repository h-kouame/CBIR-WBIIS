import os


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


def load_db_wt(base_dir='../Database/'):
    wt_dir = "Wavelets/"
    wts = {}
    for filename in os.listdir(wt_dir):
        wt = load_wt(wt_dir + filename)
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


# for debugging
def main():
    load_db_std()


if __name__ == '__main__':
        main()
