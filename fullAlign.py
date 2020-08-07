import fnmatch
import sys, os

from pyms.Experiment.IO import load_expr
from pyms.Peak.List.DPA.Class import PairwiseAlignment
from pyms.Peak.List.DPA.Function import align_with_tree, exprl2alignment
import argparse


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

            name = filename.rsplit('/tmp/')[-1]
            names.append(name)

    return matches, names


def rep_dict(cdfs):
    breed_dict = {}
    name_dict = {}

    for i in cdfs:
        a = i.split('-')
        print(a)
        b = list(a)
        # print a
        c = (b[3]).split('_')

        if c[0] in breed_dict:
            expr = load_expr(i)
            name_dict[c[0]].append(i)
            breed_dict[c[0]].append(expr)
        else:
            expr = load_expr(i)
            name_dict[c[0]] = [i]
            breed_dict[c[0]] = [expr]

    print(breed_dict)
    return breed_dict, name_dict


def singleAlign(exprs, dir, mod, gp, mp, nameTag):

    F1 = exprl2alignment(exprs)
    T1 = PairwiseAlignment(F1, mod, gp)
    A1 = align_with_tree(T1, min_peaks=mp)

    A1.write_csv(str(dir) + nameTag + "_s_rt.csv", 
                 str(dir) + nameTag + "_s_area.csv")
    
    print(str(dir) + nameTag + "_s_rt.csv", 
          str(dir) + nameTag + "_s_area.csv")


def repAlign(exprs, dir, mod1, mod2, gp1, gp2, mp1, mp2, nameTag):

    bG = []
    T2 = []

    for i, v in exprs.items():
        F1 = exprl2alignment(v)
        T1 = PairwiseAlignment(F1, mod1, gp1)
        A1 = align_with_tree(T1, min_peaks=mp1)
        T2.append(A1)
        print('v=', v)
        print("i=", i)
        print(len(F1), F1)
    print('bG=', bG)
    print(T2)

    T3 = PairwiseAlignment(T2, mod2, gp2)
    A2 = align_with_tree(T3, min_peaks=mp2)

    # T3 = PairwiseAlignment(T2, mA, gp)

    A2.write_csv(str(dir) + nameTag + '_rep_rt.csv',
                 str(dir) + nameTag + '_rep_area.csv')
    print(str(dir) + nameTag + '_rep_rt.csv',
          str(dir) + nameTag + '_rep_area.csv')

    # A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/sw2_csv/test_area.csv')


def main():
    parser = argparse.ArgumentParser(description="Pre-processing & Peak detection tool for GC-MS .cdf formatted data")

    parser.add_argument("-e",
                        action="store",
                        dest="exprDir",
                        nargs="?",
                        type=str,
                        default="/workdir2/cpowell/rasp2018/",
                        help="Location of .expr files to be aligned; Default= '/tmp/' ")

    parser.add_argument("-o",
                        action="store",
                        dest="opDir",
                        nargs="?",
                        type=str,
                        default="/tmp/",
                        help="location to store the alignment .csv output file",

                        )

    parser.add_argument("-m",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=2.5,
                        help="Modulation time allowed between peaks considered similar; Default=2.5",
                        dest="mod",
                        )

    parser.add_argument("-m2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=2.5,
                        help="* For rep only: 2nd modulation time allowed between peaks considered similar; Default=2.5",
                        dest="mod2",
                        )

    parser.add_argument("-g",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=0.30,
                        help="Gap penalty; Default=0.30",
                        dest="gap",
                        )

    parser.add_argument("-g2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=0.30,
                        help="For rep only: 2nd gap penalty; Default=0.30",
                        dest="gap2",
                        )

    parser.add_argument("-p",
                        action="store",
                        nargs="?",
                        const=1,
                        type=int,
                        default=2,
                        help="Minimum number of peaks pre sample required for alignment ; Default=2",
                        dest="minPeak",
                        )

    parser.add_argument("-p2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=int,
                        default=2,
                        help="For rep only: 2nd minimum number of peaks pre sample required for alignment ; Default=2",
                        dest="minPeak2",
                        )

    parser.add_argument("-n",
                        action="store",
                        nargs="?",
                        type=str,
                        default="alignment",
                        help="Number of points used to determine window size for peak detection; Default='alignment'",
                        dest="nameTag"
                        )

    parser.add_argument("-as",
                        choices=['single', 'rep'],
                        type=str,
                        default="single",
                        dest='alignS')

    args = parser.parse_args()
    print(args)

    list_of_exprs, names = glob(glob_pattern='*.expr', directoryname=args.exprDir)
    if args.alignS == "single":
        print('single run')
        expr_loaded = []

        for i in list_of_exprs:
            print(i)
            expr = load_expr(i)
            expr_loaded.append(expr)

        singleAlign(expr_loaded, args.opDir, args.mod, args.gap, args.minPeak, args.nameTag)
        print('Done!')

    elif args.alignS == "rep":
        print('replicate run')

        berries, name = rep_dict(list_of_exprs)

        print("berries=", berries)
        print("names", name)

        repAlign(berries,
                 args.opDir,
                 args.mod,
                 args.mod2,
                 args.gap,
                 args.gap2,
                 args.minPeak,
                 args.minPeak2,
                 args.nameTag)
    #


if __name__ == "__main__":
    main()
