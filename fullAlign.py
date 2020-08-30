import fnmatch
import os
from pyms.Experiment.IO import load_expr
from pyms.Peak.List.DPA.Class import PairwiseAlignment
from pyms.Peak.List.DPA.Function import align_with_tree, exprl2alignment
import argparse


def glob(glob_pattern, directoryname):
    """
    Walks through a directory and its subdirectories looking for files matching
    the glob_pattern and returns a list=[].

    :param directoryname: Any accessible folder name on the filesystem.
    :param glob_pattern: A string like "*.txt", which would find all text files.
    :return: A list=[] of absolute filepaths matching the glob pattern.
    """

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
    """
    @summary: Creates two dictionaries, one consisting of the experiment names, ordered by ID number
    the second consisting of the sample names, ordered by ID number as well.
    These dictionaries allow for the replicate grouping alignment.

    @param cdfs: List of .expr files to be aligned with each other
    @return:  Breed_dict[], dictionary containing loaded experiments
    @return: name_dict[], dictionary containing sample name associated to experiment files
    """

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
    """
    @summary: Converts experiments into alignments then models the pairwise alignments.
    The alignments are then aligned using the pairwise alignment object.
    The alignment tree is then exported and saved as a .csv file

    @param exprs: List containing .expr files to be aligned
    @param dir: Directory to save the output alignment .csv files
    @param mod: Retention time tolerance, in seconds
    @param gp: Gap penalty
    @param mp: Minimum peaks required
    @param nameTag: Identifier for saving .csv file
    @return: Two .csv files which express the similarities of each sample in retention time & peak area
    """

    F1 = exprl2alignment(exprs)
    T1 = PairwiseAlignment(F1, mod, gp)
    A1 = align_with_tree(T1, min_peaks=mp)

    A1.write_csv(str(dir) + nameTag + "_s_rt.csv", 
                 str(dir) + nameTag + "_s_area.csv")
    
    print(str(dir) + nameTag + "_s_rt.csv", 
          str(dir) + nameTag + "_s_area.csv")


def repAlign(exprs, dir, mod1, mod2, gp1, gp2, mp1, mp2, nameTag):
    """
    @summary: Converts experiments into alignments then models the pairwise alignments
    The alignments are then aligned using the pairwise alignment object.
    The alignment tree is then exported and saved as a .csv file

    @param exprs: Dictionary containing .expr files and sample identifiers
    @param dir: Directory to save the output alignment .csv files
    @param mod1: Retention time tolerance, in seconds (inner-state)
    @param mod2: Retention time tolerance, in seconds (between-state)
    @param gp1: Gap penalty (inner-state)
    @param gp2: Gap penalty (between-state)
    @param mp1: Minimum peaks required (inner-state)
    @param mp2: Minimum peaks required (between-state)
    @param nameTag: Identifier for saving .csv file
    @return: Two .csv files which express the similarities of each sample in retention time & peak area
    """

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
    parser = argparse.ArgumentParser(description="Peak alignment tool with adjustable tolerances & grouping strategies")

    parser.add_argument("-e",
                        action="store",
                        dest="exprDir",
                        nargs="?",
                        type=str,
                        default="/workdir2/cpowell/rasp2018/",
                        help="Location of .expr files to be aligned; Default= '/workdir2/cpowell/rasp2018/' ")

    parser.add_argument("-o",
                        action="store",
                        dest="opDir",
                        nargs="?",
                        type=str,
                        default="/tmp/",
                        help="location to store the alignment .csv output file; Default= '/tmp/' ",

                        )

    parser.add_argument("-m",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=2.5,
                        help="Retention time tolerance value between compared peaks; Default=2.5",
                        dest="mod",
                        )

    parser.add_argument("-m2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=2.5,
                        help="*Between-state: 2nd Retention time tolerance value between compared peaks; Default=2.5",
                        dest="mod2",
                        )

    parser.add_argument("-g",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=0.30,
                        help="Gap penalty for a non-aligning peak; Default=0.30",
                        dest="gap",
                        )

    parser.add_argument("-g2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=float,
                        default=0.30,
                        help="*Between-state: 2nd gap penalty for a non-aligning peak; Default=0.30",
                        dest="gap2",
                        )

    parser.add_argument("-p",
                        action="store",
                        nargs="?",
                        const=1,
                        type=int,
                        default=2,
                        help="Minimum number of peaks per sample required for alignment; Default=2",
                        dest="minPeak",
                        )

    parser.add_argument("-p2",
                        action="store",
                        nargs="?",
                        const=1,
                        type=int,
                        default=2,
                        help="*Between-state: 2nd minimum number of peaks pre sample required for alignment; Default=2",
                        dest="minPeak2"
                        )

    parser.add_argument("-n",
                        action="store",
                        nargs="?",
                        type=str,
                        default="alignment-",
                        help="Identifier string used for .csv file storage; Default='alignment-'",
                        dest="nameTag"
                        )

    parser.add_argument("-as",
                        choices=['inner', 'between'],
                        type=str,
                        default="inner",
                        help="Alignment strategies: inner-state, between-state; Default='inner' ",
                        dest='alignS')

    args = parser.parse_args()
    print(args)

    list_of_exprs, names = glob(glob_pattern='*.expr', directoryname=args.exprDir)
    if args.alignS == "inner":
        print('Singular alignment run')
        expr_loaded = []

        for i in list_of_exprs:
            # print(i)
            expr = load_expr(i)
            expr_loaded.append(expr)

        singleAlign(expr_loaded, args.opDir, args.mod, args.gap, args.minPeak, args.nameTag)
        print('Done!')

    elif args.alignS == "between":
        print('Between-state alignment run')

        berries, name = rep_dict(list_of_exprs)

        # print("berries=", berries)
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
        print('Done!')
    #


if __name__ == "__main__":
    main()
