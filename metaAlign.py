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

    mA = 10.0

    bG = []
    T2 = []
    for i in exprs:
        F1 = exprl2alignment(i)
        print(len(F1), F1)
        bG.append(F1)
    print('bG=',bG)


    #count = 0
    # for s in bG:
    #     #count += 1
    #     print('s=',s)
    #     T1 = PairwiseAlignment(s, mod, gp)
    #     T2.append[T1]
    # print(T2)
    groups = [[],[],[],[],[],[],[],[],[]]

    for s, g in zip(bG, groups):
        #count += 1
        print('s=',s)
        g = PairwiseAlignment(s, mod, gp)
        print('g=',g)
    print(groups)


    # T3 = PairwiseAlignment(T2, mA, gp )
    # A1 = align_with_tree(T3, min_peaks=2)
    #
    # A1.write_csv('/home/juicebox/Desktop/StrawberryExotic/output/bigFold/alpha_rt.csv', '/home/juicebox/Desktop/StrawberryExotic/output/bigFold/alpha_area.csv')

def main():
    folder_exprs = '/home/juicebox/Desktop/StrawberryExotic/parameters_v/bigFold'


    llamas = [ 'Alexandria', 'Bucharica', 'Capron', 'Tortona', 'Mara', 'Mignonette', 'Strawberry', 'Viridis']
    listem = []
    bigF = []

    for name in llamas:
        nomo = '*' + name + '*' + '.cdf.expr'
        print('nomo=', nomo)
        list_of_expr, names = glob(glob_pattern=nomo, directoryname=folder_exprs)
        print('LoE=', list_of_expr)
        print('name=', name)
        listem.append(list_of_expr)


    for var in listem:
        print(var)
        expr_loaded = []
        for straw in var:

            expr = load_expr(straw)
            expr_loaded.append(expr)
        print(len(expr_loaded))
        bigF.append(expr_loaded)
    print('bigF=', bigF)

    aligner(bigF)
    print('Done!')


if __name__ == "__main__":
    main()
