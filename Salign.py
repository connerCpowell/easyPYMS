import fnmatch
import sys, os

from pyms.Experiment.IO import load_expr
from pyms.Peak.List.DPA.Class import PairwiseAlignment
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

            name = filename.rsplit('/StrawberryExotic/')[-1]
            names.append(name)

    return matches, names

def aligner(exprs):

    mod = 2.5
    gp = 0.30

    F1 = exprl2alignment(exprs)
    T1 = PairwiseAlignment(F1, mod, gp)
    A1 = align_with_tree(T1, min_peaks=2)

    A1.write_csv('/home/juicebox/Desktop/StrawberryExotic/output/10point_rt.csv', '/home/juicebox/Desktop/StrawberryExotic/output/10point_area.csv')


def main():
    folder_with_exprs = '/home/juicebox/Desktop/StrawberryExotic/parameters_v/point'
    expr_loaded = []

    list_of_exprs, names = glob(glob_pattern='*.cdf10b.expr', directoryname=folder_with_exprs)
    for i in list_of_exprs:
        print(i)
        expr = load_expr(i)
        expr_loaded.append(expr)

    aligner(expr_loaded)
    print('Done!')


if __name__ == "__main__":
    main()
