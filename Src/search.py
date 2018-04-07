import image_ops as ops
import operator


def query(db_std, base_dir='../Data/image.orig/', imagename='807.jpg', width=128, height=128, bits_per_pixel=24, percent=50):
    path = base_dir + imagename
    components = ops.preprocess(path, width, height, bits_per_pixel)
    wt = ops.wavelet_transform(components, w_type='db8')
    upper_left = ops.get_upper_left_coefficients(wt)
    q_std = ops.standard_dev(upper_left)
    matches = compare_std(db_std, q_std, percent)
    return matches



# def compare_std(query_std, candidate_std):
#     q_std1, q_std2, q_std3 = query_std[0], query_std[1], query_std[2]
#     c_std1, c_std2, c_std = candidate_std[0], candidate_std[1], candidate_std[2]


def compare_std(db_std, query_std, percent=50):
    beta = 1 - percent/100.0
    print beta
    q_std1, q_std2, q_std3 = query_std[0], query_std[1], query_std[2]
    indexes = []
    for i in range(len(db_std)):
        db_std1, db_std2, db_std3 = db_std[i][0], db_std[i][1], db_std[i][2]
        if (q_std1*beta < db_std1 and db_std1 < q_std1/beta) or \
           ((q_std2*beta < db_std2 and db_std2 < q_std2/beta) and \
            (q_std3*beta < db_std3 and db_std3 < q_std3/beta)):

             indexes.append(i)
    return indexes


# wt format
# wt = {'cA': {'C1': [], 'C2': [], 'C3': []},
#       'cH': {'C1': [], 'C2': [], 'C3': []},
#       'cV': {'C1': [], 'C2': [], 'C3': []},
#       'cD': {'C1': [], 'C2': [], 'C3': []}}
def compute_distance(query_wt, candidate_wt):
    coeff_names = query_wt.keys()
    comp_names = query_wt[coeff_names[0]].keys()
    distance = 0
    for coeff_name in coeff_names:
        for comp_name in comp_names:
            q_weights = query_wt[coeff_name][comp_name]
            c_weights = candidate_wt[coeff_name][comp_name]
            height, width = len(q_weights), len(q_weights[0])
            for y in range(height):
                for x in range(width):
                    distance = distance + abs(float(q_weights[y][x]) - float(c_weights[y][x]))
    return distance


def compute_distances(query_wt, db_wt):
    distances = {}
    imagenames = db_wt.keys()
    for name in imagenames:
        distances[name] = compute_distance(query_wt, db_wt[name])
    return distances


def get_matches(distances, number=10):
    sorted_distances = sorted(distances.items(), key=operator.itemgetter(1))
    closest_images = sorted_distances[: number]
    return [image[0] for image in closest_images]


def main():
    print 0


if __name__ == '__main__':
    main()






