from scipy.spatial import distance_matrix
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from collections import OrderedDict
import sys
import argparse


def distance(lista, listb):
    return sum((b - a) ** 2 for a, b in zip(lista, listb)) ** .5


def get_data(line, num):
    try:
        x = float(line.split(',')[num].strip())
        # print('gd_x=', x)
        return x
    except:
        return 0


def main():

    parser = argparse.ArgumentParser(description="Heirarchical cluster analysis using an alignment .csv file")

    parser.add_argument("-c",
                        action="store",
                        dest="csvf",
                        nargs="?",
                        type=str,
                        default="/workdir2/cpowell/rasp2018/",
                        help="Location of .csv file to be analyzed; Default= '/tmp/' ")

    parser.add_argument("-o",
                        action="store",
                        dest="opn",
                        nargs="?",
                        type=str,
                        default="/tmp/",
                        help="location to store the HCA .png output file",
                        )

    args = parser.parse_args()
    print(args)

    # with open('/home/cocopalacelove/tmp/sb_out/beta1_area.csv', 'r') as f:
    with open(args.csvf, 'r') as f:
        i = 0
        species_dict = OrderedDict()
        list_o_species = []
        total = 0
        for line in f:
            num = line.count('\t')
            num2 = line.count(',')

            if num > 0:
                total = num + 1
                print('total=' + str(total))
            print('i1=', i)

            if i != 0:
                count = 0
                for j in range(num2):
                    y = get_data(line, j)
                    species_dict[list_o_species[j]].append(get_data(line, j + 1))
            else:
                for i in range(num2):
                    print('rang_n2', range(num2))
                    print('i0=', i)
                    j = i + 1

                    species_dict[line.split(',')[j].strip()] = []
                    u = line.split(',')[j].strip()
                    print('u=' + str(u) + '\n')
                    x = line.split(',')[j].strip()
                    list_o_species.append(x)
            i = 1
        print(species_dict)

    dm_list = []
    names = []
    name2 = []

    x = 0
    for l in species_dict:
        if x == 0:
            print(l)
            x += 1
        else:
            print(l, species_dict[l])
            dm_list.append(species_dict[l])
            names.append(l)
    print('names=', names)

    for n in names:
        print('n=', n)
        if str(n).endswith('.cdf"'):
            print('yes')
            name2.append(n)
        else:
            print('no')

    d = distance_matrix(dm_list, dm_list)
    linked = linkage(d, 'ward')

    plt.figure(figsize=(10, 10))
    dendrogram(linked,
               orientation='top',
               labels=name2,
               distance_sort='descending',
               show_leaf_counts=True)

    plt.savefig(args.opn + '.svg', format='svg')
    plt.show()
    
if __name__ == "__main__":
    main()