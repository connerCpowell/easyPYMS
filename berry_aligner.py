import itertools
import fnmatch
import os

from pyms.Experiment.IO import load_expr
from pyms.Peak.List.DPA.Class import PairwiseAlignment, Alignment
from pyms.Peak.List.DPA.Function import align_with_tree, exprl2alignment


def glob(glob_pattern, directoryname):
    '''
    Walks through a directory and its subdirectories looking for files matching
    the glob_pattern and returns a list=[].

    :param directoryname: Any accessible folder name on the filesystem.
    :param glob_pattern: A string like "*.txt", which would find all text files.
    :return: A list=[] of absolute filepaths matching the glob pattern.
    '''


    matches = []
    names = []
    for root, dirnames, filenames in os.walk(directoryname):
        for filename in fnmatch.filter(filenames, glob_pattern):
            absolute_filepath = os.path.join(root, filename)
            matches.append(absolute_filepath)


            name = absolute_filepath.rsplit('/all_expr/')[-1]
            names.append(name)

    return matches, names

def lil_dictor(cdfs):

    breed_dict = {}
    name_dict = {}


    for i in cdfs:
        a = i.split('-')
        print(a)
        b = list(a)
        #print a
        print(b[1])

        if b[1] in breed_dict:
            expr = load_expr(i)
            name_dict[b[1]].append(i)
            breed_dict[b[1]].append(expr)
        else:
            expr = load_expr(i)
            name_dict[b[1]] = [i]
            breed_dict[b[1]] = [expr]

    print(breed_dict)
    return breed_dict, name_dict



def lil_aligner(exprs):

    mod = 2.5
    gp = 0.30

    mA = 10.0

    bG = []
    T2 = []

    for i, v in exprs.items():
        F1 = exprl2alignment(v)
        T1 = PairwiseAlignment(F1, mod, gp)
        A1 = align_with_tree(T1, min_peaks=3)
        T2.append(A1)
        print(len(F1), F1)
    print('bG=',bG)
    print(T2)


    T3 = PairwiseAlignment(T2, mA, gp)
    A2 = align_with_tree(T3, min_peaks=4)

   # T3 = PairwiseAlignment(T2, mA, gp)


    A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_p120s30pe10n3_p34_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_p120s30pe10n3_p34_area.csv')
    #A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_area.csv')




def aligner(exprs):

    mod = 2.5
    gp = 0.30

    mA = 10.0

    bG = []
    T2 = []

    for i, v in exprs.items():
        F1 = exprl2alignment(v)
        T1 = PairwiseAlignment(F1, mod, gp)
        A1 = align_with_tree(T1, min_peaks=3)
        T2.append(A1)
        print(len(F1), F1)
    print('bG=',bG)
    print(T2)


    T3 = PairwiseAlignment(T2, mA, gp)
    A2 = align_with_tree(T3, min_peaks=4)

   # T3 = PairwiseAlignment(T2, mA, gp)


    A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_p120s30pe10n3_p34_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_p120s30pe10n3_p34_area.csv')
    #A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_area.csv')


def main():

    folder_with_cdffiles = '/home/juicebox/Desktop/Acinis/CDFdata/all_expr'

    cdfs, names = glob(glob_pattern="*12030pe10n3", directoryname= folder_with_cdffiles)

    print(cdfs)
    print(names)


    berrys, names = lil_dictor(cdfs)
    print(berrys)
    print(names)

    aligner(berrys)



if __name__ == "__main__":
    main()