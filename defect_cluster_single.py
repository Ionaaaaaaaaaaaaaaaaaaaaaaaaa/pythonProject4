from math import atan2
import sklearn
from sklearn.cluster import AgglomerativeClustering, FeatureAgglomeration
import numpy as np
import argparse
import csv
from pathlib import Path
from tqdm import tqdm
from functools import cmp_to_key
import matplotlib.pyplot as plt


def binary_search(arr, elem):
    total = len(arr)
    l = 0
    r = total

    while r - l > 1:
        cur = (l + r) // 2
        if elem < arr[cur]:
            r = cur
        elif elem > arr[cur]:
            l = cur
        else:
            return cur, arr[cur]
    return l, arr[l]


def list_to_str(l: list) -> list[str]:
    for i in range(len(l)):
        l[i] = str(l[i])
    return l


def cmp_format(x, y):
    if x < y:
        return -1
    if x > y:
        return 1
    return 0


def compare_bonds(bond1, bond2):
    x1, y1, z1 = bond1[0], bond1[1], bond1[2]
    x2, y2, z2 = bond2[0], bond2[1], bond2[2]

    if abs(z1 - z2) > 1e-6:
        return cmp_format(z1, z2)

    r1 = (x1 ** 2 + y1 ** 2) ** 0.5
    r2 = (x2 ** 2 + y2 ** 2) ** 0.5

    if abs(r1 - r2) > 1e-6:
        return cmp_format(r1, r2)
    
    phi1 = atan2(y1, x1)
    phi2 = atan2(y2, x2)

    return cmp_format(phi1, phi2)


def make_clusters(
        filename: str, output_dir: str, dist_thr: float, 
        step: float, integral: bool, show: bool):
    xlist = []
    ylist = []
    zlist = []
    deathtlist = []
    num_clusters_to_show = 10

    print(f'Loading {filename}')
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=' ')

        for row in reader:
            xlist.append(float(row['BondX,mm']))
            ylist.append(float(row['BondY,mm']))
            zlist.append(float(row['BondZ,mm']))
            deathtlist.append(float(row['DeathT,s']))

    time_points = []
    with open(str(Path(filename).parent /'time_points.txt'), 'r') as tpf:
        l = tpf.readline().split(' ')[:-1]
        for el in l:
            time_points.append(float(el))

    time_points = np.linspace(time_points[0], time_points[-1], int((time_points[-1] - time_points[0]) / step))

    data = {tp: [] for tp in time_points} # key: timepoint value: [np.array([x, y, z])]
    for cx, cy, cz, t in zip(xlist, ylist, zlist, deathtlist):
        round_t = binary_search(time_points, t)[1]
        data[round_t].append(np.array([cx, cy, cz]))

    if integral:
        for idx, t in enumerate(time_points[1:]):
            data[t] += data[time_points[idx]]

    print('Loading finished')

    #for t in tqdm(data, desc='Conversion to numpy', total=len(data)):
    #    data[t] = np.asarray(data[t])
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    for t, bonds in tqdm(data.items(), desc='Clustering', total=len(data)):
        with open(str(Path(output_dir) / 'cluster_{:.6f}.txt').format(t), 'w') as f:
            f.write(' '.join(['X,mm', 'Y,mm', 'Z,mm', 'D,mm', 'N']) + '\n')
            # try-catch is KOSTYL'
            try:
                part_len = 15000
                num_parts = (len(bonds) + part_len - 1) // part_len
                bonds.sort(key=cmp_to_key(compare_bonds))

                fig = plt.figure()
                ax = plt.axes(projection='3d')  
                ax.set_label(f'Time {t}')

                for part in range(num_parts):
                    clustering = AgglomerativeClustering(
                        n_clusters=None,
                        linkage='single',
                        memory=str(Path.cwd()), 
                        distance_threshold=dist_thr,
                        compute_full_tree=True).fit(bonds[part * part_len:min((part + 1) * part_len, len(bonds))])
                    
                    clustered = [[] for _ in range(clustering.n_clusters_)]

                    clustered_x = [[] for _ in range(clustering.n_clusters_)]
                    clustered_y = [[] for _ in range(clustering.n_clusters_)]
                    clustered_z = [[] for _ in range(clustering.n_clusters_)]


                    for label, elem in zip(clustering.labels_, bonds):
                        clustered[label].append(elem)

                    for label in range(len(clustered)):
                        clustered[label] = np.asarray(clustered[label])

                    for label in range(len(clustered)):
                        clustered_x[label] = np.asarray(clustered[label][:, 0])
                        clustered_y[label] = np.asarray(clustered[label][:, 1])
                        clustered_z[label] = np.asarray(clustered[label][:, 2])

                    ordered_labels = sorted(list(range(clustering.n_clusters_)), 
                                    key=lambda idx: len(clustered_x[idx]))

                    #center_x = [0] * len(clustering.n_clusters_) # idx -- label
                    #center_y = [0] * len(clustering.n_clusters_)
                    #center_z = [0] * len(clustering.n_clusters_)
                    #diameters = [0] * len(clustering.n_clusters_)

                    for label, elements in enumerate(clustered):
                        # Calculate center of cluster
                        cx = 0
                        cy = 0
                        cz = 0
                        for elem in elements:
                            cx += elem[0]
                            cy += elem[1]
                            cz += elem[2]
                        cx /= len(elements)
                        cy /= len(elements)
                        cz /= len(elements)

                        # Calculate diameter of cluster
                        furthest_element = max(elements, 
                            key=lambda elem: (elem[0] - cx) ** 2 + (elem[1] - cy) ** 2 + (elem[2] - cz) ** 2)
                        d = ((furthest_element[0] - cx) ** 2 + (furthest_element[1] - cy) ** 2 + (furthest_element[2] - cz) ** 2) ** 0.5

                        #center_x[label] = cx
                        #center_y[label] = cy
                        #center_z[label] = cz
                        #diameters[label] = d
                        f.write(' '.join(list_to_str([cx, cy, cz, d, len(clustered[label])])) + '\n')

                        if label in ordered_labels[-num_clusters_to_show:]:
                            ax.scatter3D(clustered_x[label], clustered_y[label], clustered_z[label])
                if show:
                    plt.show()
                plt.savefig(f'{output_dir}/img_' + '{:5f}.png'.format(t) )

            except Exception as e:
                print(f'Exception occured: {e}')
        

def main():
    parser = argparse.ArgumentParser(description='Musen defect clusteriser')
    parser.add_argument('--input', '-i', default='bonds_preprocessed.txt', type=str,
                        help='Preprocessed bond file')
    parser.add_argument('--output', '-o', default='clustered', type=str,
                        help='Directory for output with clustered bonds')
    parser.add_argument('--distance', '-d', default=0.5, type=float,
                        help='Distance threshold for clustring')
    parser.add_argument('--step', '-s', default=0.001, type=float,
                        help='Time interval to build clusters')
    parser.add_argument('--integral', action='store_false',
                        help='Integral storage of bonds')
    parser.add_argument('--show', action='store_true',
                        help='Show plots')                        

    args = parser.parse_args()
    make_clusters(
        args.input, args.output, args.distance,
        args.step, args.integral, args.show)


if __name__ == '__main__':
    main()
