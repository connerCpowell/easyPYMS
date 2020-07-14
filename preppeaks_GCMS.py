from pyms.GCMS.IO.ANDI.Function import ANDI_reader
from pyms.GCMS.Function import build_intensity_matrix
from pyms.Noise.SavitzkyGolay import savitzky_golay
from pyms.Baseline.TopHat import tophat
from pyms.Deconvolution.BillerBiemann.Function import BillerBiemann, rel_threshold, num_ions_threshold
from pyms.Peak.Class import Peak
from pyms.Peak.Function import peak_sum_area
from pyms.Experiment.Class import Experiment
from pyms.Experiment.IO import store_expr
import itertools
import fnmatch
import os
from pyms.Noise.Analysis import window_analyzer
import csv
import argparse
from datetime import datetime



def glob(glob_pattern, directoryname, splitPattern):
    """
    Walks through a directory and its subdirectories looking for files matching
    the glob_pattern and returns a list.

    :param directoryname: Any accessible folder name on the filesystem.
    :param glob_pattern: A string like "*.txt", which would find all text files.
    :param splitPattern: Location in file path to split the file name on
    :return: A list of absolute filepaths matching the glob pattern.
    """

    matches = []
    names = []
    for root, dirnames, filenames in os.walk(directoryname):
        for filename in fnmatch.filter(filenames, glob_pattern):
            absolute_filepath = os.path.join(root, filename)
            matches.append(absolute_filepath)

            name = filename.rsplit(splitPattern)[-1]
            names.append(name)

    print('.cdf names', names)
    return matches, names


def matrix_from_cdf(cdffile, name):
    """
    Intakes a .cdf file and produces an intensity matrix and a noise level .
    The noise level info is obtained by producing a TIC and using the window_analyzer
    method to extract a noise approximation.

    @param cdffile: Absolutepath to a .cdf file to be processed into matrix
    @param name: file name associated with .cdf file
    @return: An intensity matrix and a corresponding noise level value
    """

    data = ANDI_reader(cdffile)
    print('File name', name)
    data.info()
    tic = data.get_tic()
    noise_lvl = window_analyzer(tic)
    print('Noise value=', noise_lvl)

    return build_intensity_matrix(data), noise_lvl


def Preprocess_IntensityMatrices(matrices):
    """
    Baseline correction and smoothing of Intensity Matrices
    input matrix list, outputs corrected/"cleansed" matrix list

    @param matrices: List of matrices generated by the matrix_from_cdf method
    @return: List of matrices that have been baseline corrected & smoothed for peak detection
    """

    count = 1
    for im in matrices:

        n_s, n_mz = im.get_size()
        count += 1

        for ii in range(n_mz):
            ic = im.get_ic_at_index(ii)
            ic_smoof = savitzky_golay(ic)
            ic_bc = tophat(ic_smoof, struct='1.5m')
            im.set_ic_at_index(ii, ic_bc)

    return (matrices)  # save to file


def Peak_detector(pp_im, noise, name, points, scans, percent, ni, name_tag, sdir):
    """
    Intake cleansed intensity matrices and CMD args
    Produces list of peaks and corresponding mass spectrum of each sample

    @param pp_im: Cleansed intensity matrices from the Preprocess_IntensityMatrices method
    @param noise: Noise level approximation produced by the matrix_from_cdf method
    @param name: Sample name use from creating mass spectrum .csv files
    @param points: Size of window use for peak detection in BillerBiemann method
    @param scans: Number of adjacent windows to compare for peak detection in BillerBiemann method
    @param percent: Percentile threshold a peak must exceed to be considered an informative peak
    @param ni: Number of ions required per peak to be considered an informative peak
    @param name_tag: String consisting of CMD args for identification, ie. 'p140s25%3n3'
    @param sdir: Directory to save the mass spectrum .csv files
    @return: List of peaks per sample
    @return: csv files containing mass spectrum corresponding to each peak
    """

    peakz = []
    savePath = sdir
    ms_data_files = []

    print("len pp_im", len(list(pp_im)))
    print("len noise", len(noise))
    print("len name", len(name), name)

    for im, n, na in itertools.izip(list(pp_im), noise, name):

        poss_peaks = BillerBiemann(im, points=points, scans=scans)
        pi = rel_threshold(poss_peaks, percent=percent)
        nin = num_ions_threshold(pi, n=ni, cutoff=n)

        completeName = os.path.join(savePath, na + name_tag + "ms_data.csv")
        with open(completeName, 'w') as f:
            w = csv.writer(f)
            head = ['Area', 'RTs'] + [float(i) for i in range(35,221)]


            w.writerow(head)
            for peak in nin:

                area = peak_sum_area(im, peak)
                peak.set_area(area)
                ms = peak.get_mass_spectrum()
                p_rt = peak.get_rt()
                its = []
                ms_items = list(ms.mass_spec)
                for spec in ms_items:
                    f_spec = float(spec)
                    its.append(f_spec)

                ms_d = ([area] + [p_rt] + its)

                w.writerow(ms_d)

            f.close()

        peakz.append(nin)
        ms_data_files.append(completeName)
    print('ms_data_files:', ms_data_files)

    return [peakz, ms_data_files]


def replacementWriter(stringIn, stringOut, chars):
    """
    Cleans out unwanted characters for strings

    @param stringIn: Input string to be edited
    @param stringOut: Output string w/ unwanted chars removed
    @param chars: List of characters to be removed
    @return: String to append to the list of MS data
    """

    stringIn = str(stringIn)
    for c in chars:
        stringIn = stringIn.replace(c, '')
    stringOut.write(stringIn + "\n")

def MS_process(file_list):
    """
    Processes mass spectrum data from .csv file to a .txt file formatted for the
    NIST MS_Search program

    @param file_list: List of .csv files to be processed
    @return: Produces corresponding .txt files for every MS .csv file
    """

    ratio_set = []
    print("fl=", file_list)

    for n in file_list:
        peaks = []
        areas = []
        print('n=', n)
        with open(n, 'r') as f:
            next(f)
            for line in f:
                sline = line.split(',')
                a = sline[0]
                p = sline[1]
                sline.pop(0)
                sline.pop(0)
                peaks.append(p)
                areas.append(a)

                ratios = []
                maxi = max(map(float, sline))

                c = 34.0
                for i in sline:
                    r = float(i) / float(maxi)
                    rx = int(r * 999)
                    ratios.append([c, rx])
                    c += 1

                ratio_set.append(ratios)

            name1 = n.rsplit('ms_data.csv')
            name2 = name1[0] + '.txt'
            print('n2=', name2)

            with open(name2, "w+") as pp:
                for ratios, p, a, in zip(ratio_set, peaks, areas):
                    replacementWriter(stringIn=('Name:', p, 'Area-', a), stringOut=pp, chars="',()")
                    replacementWriter(stringIn=('Num Peaks:', 10), stringOut=pp, chars="',()")

                    for i in sorted(ratios, key=lambda t: t[1], reverse=True)[:10]:
                        replacementWriter(stringIn=i, stringOut=pp, chars="[],")
                    pp.write("\n")


def Experiment_store(names, peakz, name_tag, sdir2):
    """
    Stores peak information used in the peak alignment scripts ()
    Using CMD args for the names and storage directory

    @param names: .cdf file names processed by this script
    @param peakz: peak data corresponding to each .cdf file
    @param name_tag: Identifier expressing peak detection variables used in this processing run
    @param sdir2: Location to store to .expr files corresponding to each .cdf file
    @return: list of files saved
    """

    for n, p in itertools.izip(names, peakz):
        expr = Experiment(n, p)
        expr.sele_rt_range(["1m", "50m"])
        store_expr(sdir2 + n + name_tag + ".expr", expr)
        print(n, "checked")

def main():

    parser = argparse.ArgumentParser(description="Pre-processing & Peak detection tool for GC-MS .cdf formatted data")

    parser.add_argument("-f",
                        action="store",
                        dest="dirc",
                        nargs="?",
                        type=str,
                        default="./tmp/",
                        help="Location of .cdf files to be processed; Default= '/tmp/' ")

    parser.add_argument("-n",
                        action="store",
                        nargs="?",
                        type=str,
                        help="location in .cdf file name to split on",
                        dest="name"
                        )

    parser.add_argument("-p",
                        action="store",
                        nargs="?",
                        const=1,
                        type=int,
                        default=140,
                        help="Number of points used to determine window size for peak detection; Default=140",
                        dest="points",
                        )

    parser.add_argument("-s",
                        action="store",
                        dest="scans",
                        nargs="?",
                        const=1,
                        type=int,
                        default=25,
                        help="Number of scans (adjacent windows) to average across for peak detection; Default=25")

    parser.add_argument("-t",
                        action="store",
                        dest="threshold",
                        nargs="?",
                        const=1,
                        type=int,
                        default=3,
                        help="Minimum percentage threshold required to qualify as a peak; Default=3")

    parser.add_argument("-i",
                        action="store",
                        dest="ion",
                        nargs="?",
                        const=1,
                        type=int,
                        default=3,
                        help="Minimum number of Ions required to qualify as a peak; Default=3")

    parser.add_argument("-c",
                        action="store",
                        dest="sdir",
                        nargs="?",
                        default="tmp/",
                        help="Location to save MS extraction .csv files")

    parser.add_argument("-e",
                        action="store",
                        dest="sdir2",
                        nargs="?",
                        default="tmp/",
                        help="Location to save the .expr files for alignment scripts")
    args = parser.parse_args()

    print(args)

    name_tag = str('p' + str(args.points) + 's' + str(args.scans) + '%' + str(args.threshold) + 'n' + str(args.ion))

    print("CDF file directory:", args.dirc)
    print("split:", args.name)
    print("Points:", args.points)
    print("Scans:", args.scans)
    print("Percent:", args.threshold)
    print("num. of ions:", args.ion)
    print("Name_tag:", name_tag)
    print("Storage directory (csv):", args.sdir)
    print("Storage dir (expr):", args.sdir2)

    matrices = []
    noise = []

    startTime = datetime.now()

    list_of_cdffiles, names = glob(glob_pattern='*.cdf', directoryname=args.dirc, splitPattern=args.name)

    for cdffile, name in itertools.izip(list_of_cdffiles, names):
        print('name=', name)
        m_c = matrix_from_cdf(cdffile, name)
        matrices.append(m_c[0])
        noise.append(m_c[1])

    print('names=', names)

    pp_im = Preprocess_IntensityMatrices(matrices)
    peak_m = Peak_detector(pp_im, noise, names, args.points, args.scans, args.threshold, args.ion, name_tag, args.sdir)
    #print(peak_m)
    Experiment_store(names, peak_m[0], name_tag, args.sdir2)

    #print('p1=', peak_m[1])
    MS_process(peak_m[1])

    timeR = datetime.now() - startTime
    print('Seconds:', str(timeR))



if __name__ == "__main__":
    main()