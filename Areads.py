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

def matrix_from_cdf(cdffile, name):
    data = ANDI_reader(cdffile)
    print(name)
    data.info()
    tic = data.get_tic()
    noise_lvl = window_analyzer(tic)

    return build_intensity_matrix(data), noise_lvl


def Preprocess_IntensityMatrixes(matrixes):
    # noise removal and baseline correction of Intensity Matricies
    #input matrix list, outputs corrected matrix list

    count = 1
    for im in matrixes:

        n_s, n_mz = im.get_size()
        count += 1

        for ii in range(n_mz):

            print("Working on IC#", ii+1, " Unit", count)
            ic = im.get_ic_at_index(ii)
            ic_smoof = savitzky_golay(ic)
            ic_bc = tophat(ic_smoof, struct='1.5m')
            im.set_ic_at_index(ii, ic_bc)

    #print(matrixes)
    return(matrixes)        #save to file



def Peak_detector(pp_im, n, var): #n,
    # Peak detection and filtering and selection
    peakz = []
    counter = 1

    for im in list(pp_im):

        print(var)
        poss_peaks = BillerBiemann(im, points=var, scans=25)                   #increase scan #
        pi = rel_threshold(poss_peaks, percent=2)
        nin = num_ions_threshold(pi, n=3, cutoff=n)
        for peak in nin:
            area = peak_sum_area(im, peak)
            peak.set_area(area)

        peakz.append(nin)
        print("...", counter)
        counter += 1

    for pkz in peakz:
        print("Peaks detected: ", len(pkz))


    return peakz


def Experiment_store(names,  peakz, var):   #peakz,

    for n, p in itertools.izip(names, peakz):
        expr = Experiment(n, p)
        expr.sele_rt_range(["1m", "50m"])
        store_expr("/home/juicebox/Desktop/StrawberryExotic/parameters_v/bigFold2/"+n+".p"+str(var)+"_s25_%2_n3expr", expr)
        print(n, "checked")

    for n in names:
        print("/home/juicebox/Desktop/StrawberryExotic/parameters_v/bigFold2/"+n+".p"+str(var)+"_s25_%2_n3expr")

def main():
    folder_with_cdffiles = '/home/juicebox/Desktop/StrawberryExotic'
    matrixes = []
    noise = []

    list_of_cdffiles, names = glob(glob_pattern='*.cdf', directoryname=folder_with_cdffiles)
    for cdffile, name in itertools.izip(list_of_cdffiles, names):
        print name
        m_c = matrix_from_cdf(cdffile, name)
        matrixes.append(m_c[0]) #m_c[0]
        noise.append(m_c[1])
    print(matrixes)
    print(noise)


    pp_im = Preprocess_IntensityMatrixes(matrixes)
    for i, n in itertools.izip(pp_im, noise):
        print(i)

    for i in range(40, 145, 5):
        print(i)
        peak_m = Peak_detector(pp_im, n, i)  #pp_im for name
        Experiment_store(names, peak_m,  i)  # peak_m


   # print(names)

if __name__ == "__main__":
    main()