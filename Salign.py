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

def singleAlign(exprs, dir, mod, gp, mp, nameTag):

    #mod = 2.5
    #gp = 0.30

    F1 = exprl2alignment(exprs)
    T1 = PairwiseAlignment(F1, mod, gp)
    A1 = align_with_tree(T1, min_peaks=mp)

    #A1.write_csv('/home/cocopalacelove/tmp/sb_out/A1a_rt.csv', '/home/cocopalacelove/tmp/sb_out/A1a_area.csv')
    #A1.write_csv(str(dir)+"rasp2018_rt.csv", str(dir)+"rasp2018_area.csv")
    #print(str(dir)+"rasp2018_rt.csv", str(dir)+"rasp2018_area.csv")

    A1.write_csv(str(dir) + nameTag + "_rt.csv", str(dir) + nameTag + "_area.csv")
    print(str(dir) + nameTag + "_rt.csv", str(dir) + nameTag + "_area.csv")


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

    parser.add_argument("-g",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=0.30,
                        help="Gap penalty; Default=0.30",
                        dest="gap",
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

    parser.add_argument("-n",
                        action="store",
                        nargs="?",
                        type=str,
                        default="alignment",
                        help="Number of points used to determine window size for peak detection; Default='alignment'",
                        dest="nameTag",
                        )

    args = parser.parse_args()

    print(args)

    #folder_with_exprs = sys.argv[1]
    #align_dir = sys.argv[2]
    #mod = sys.argv[3]
    #gp = sys.argv[4]

    expr_loaded = []

    list_of_exprs, names = glob(glob_pattern='*.expr', directoryname=args.exprDir)
    for i in list_of_exprs:
        print(i)
        expr = load_expr(i)
        expr_loaded.append(expr)

    singleAlign(expr_loaded, args.opDir, args.mod, args.gap, args.minPeak, args.nameTag)
    print('Done!')


if __name__ == "__main__":
    main()
