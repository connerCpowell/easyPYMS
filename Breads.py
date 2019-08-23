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
import pandas as pd

import timeit


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

            name = filename.rsplit('/CDFdata/')[-1]
            names.append(name)

    return matches, names

def matrix_from_cdf(cdffile, name):
    data = ANDI_reader(cdffile)
    #print(name)
    #data.info()
    tic = data.get_tic()
    noise_lvl = window_analyzer(tic)
    #print(noise_lvl)

    return build_intensity_matrix(data), noise_lvl


def Preprocess_IntensityMatrixes(matrixes):
    # noise removal and baseline correction of Intensity Matricies
    #input matrix list, outputs corrected matrix list

    count = 1
    for im in matrixes:

        n_s, n_mz = im.get_size()
        count += 1

        for ii in range(n_mz):

            #print("Working on IC#", ii+1, " Unit", count)
            ic = im.get_ic_at_index(ii)
            ic_smoof = savitzky_golay(ic)
            ic_bc = tophat(ic_smoof, struct='1.5m')
            im.set_ic_at_index(ii, ic_bc)

    #print(matrixes)
    return(matrixes)        #save to file



def Peak_detector(pp_im, noise, name):
    # Peak detection and filtering and selection
    peakz = []
    counter = 1
    savePath = '/home/juicebox/utils/easyGC/MS_peak_data'

    for im, n, na in itertools.izip(list(pp_im), noise, name):

        ms_data = []

        #print(na)
        poss_peaks = BillerBiemann(im, points=140, scans=20)                 #increase scan #
        pi = rel_threshold(poss_peaks, percent=2)
        nin = num_ions_threshold(pi, n=3, cutoff=n)



        completeName = os.path.join(savePath, na + "2y.csv")
        with open(completeName, 'w') as f:
            w = csv.writer(f)
            head = ['RTs', 35.0, 36.0, 37.0, 38.0, 39.0, 40.0, 41.0, 42.0, 43.0, 44.0, 45.0, 46.0, 47.0, 48.0, 49.0, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0, 57.0, 58.0, 59.0, 60.0, 61.0, 62.0, 63.0, 64.0, 65.0, 66.0, 67.0, 68.0, 69.0, 70.0, 71.0, 72.0, 73.0, 74.0, 75.0, 76.0, 77.0, 78.0, 79.0, 80.0, 81.0, 82.0, 83.0, 84.0, 85.0, 86.0, 87.0, 88.0, 89.0, 90.0, 91.0, 92.0, 93.0, 94.0, 95.0, 96.0, 97.0, 98.0, 99.0, 100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0, 107.0, 108.0, 109.0, 110.0, 111.0, 112.0, 113.0, 114.0, 115.0, 116.0, 117.0, 118.0, 119.0, 120.0, 121.0, 122.0, 123.0, 124.0, 125.0, 126.0, 127.0, 128.0, 129.0, 130.0, 131.0, 132.0, 133.0, 134.0, 135.0, 136.0, 137.0, 138.0, 139.0, 140.0, 141.0, 142.0, 143.0, 144.0, 145.0, 146.0, 147.0, 148.0, 149.0, 150.0, 151.0, 152.0, 153.0, 154.0, 155.0, 156.0, 157.0, 158.0, 159.0, 160.0, 161.0, 162.0, 163.0, 164.0, 165.0, 166.0, 167.0, 168.0, 169.0, 170.0, 171.0, 172.0, 173.0, 174.0, 175.0, 176.0, 177.0, 178.0, 179.0, 180.0, 181.0, 182.0, 183.0, 184.0, 185.0, 186.0, 187.0, 188.0, 189.0, 190.0, 191.0, 192.0, 193.0, 194.0, 195.0, 196.0, 197.0, 198.0, 199.0, 200.0, 201.0, 202.0, 203.0, 204.0, 205.0, 206.0, 207.0, 208.0, 209.0, 210.0, 211.0, 212.0, 213.0, 214.0, 215.0, 216.0, 217.0, 218.0, 219.0, 220.0]
            w.writerow(head)
            for peak in nin:

                area = peak_sum_area(im, peak)
                print('area=', area)
                peak.set_area(area)
                ms = peak.get_mass_spectrum()
                #print("Peaks rt: ", peak.get_rt())
                #print("Peaks ms_list: ", ms.mass_list)
                print("Peaks ms_spec: ", list(ms.mass_spec))
                p_rt = peak.get_rt()
                its = []
                items = list(ms.mass_spec)
                for i in items:
                    x = float(i)
                    its.append(x)
                ms_d = ([p_rt] + its)
                print(ms_d)
                # c = str(ms_d).split(',')
                #f.write(str(ms_d))

                w.writerow(ms_d)
        f.close()
        #
        #
        #         #print(peak.get_rt(), items)
        #         # ms_d = ([peak.get_rt()] + its)
        #         # print(ms_d)
        #         # w = csv.writer(f)
        #         # w.writerow(x for x in list(ms_d))
        #
        #         # w = csv.writer(f, delimiter=',')
        #         # w.writerows(list[p_rt + items])
        #         # ms_data.append((peak.get_rt(), list(ms.mass_spec)))
        #         # completeName = os.path.join(savePath, na+"2b.csv")
        #         # f = open(completeName, "w+")
        #         # for i in ms_data:
        #         #     f.write("%s" % str(i))
        #         # f.close()
        #         # with open(completeName, 'w') as f:
        #         #     f.write(str([peak.get_rt()] + items) + '\n')
        #         # f.write(str([peak.get_rt()] + items) + '\n')
        #         # f.write(str(peak.get_rt()) + str(items).replace('[', '').replace(']', '') + '\n')
        #         # x = str(peak.get_rt()) + str(items).replace('[', '').replace(']', '')
        #         # y = x.split(',')
        #         # print (str(y))
        #         # f.write(str(y) + '\n')

        peakz.append(nin)
        #print("...", counter)
        counter += 1

    #for pkz in peakz:
       # print("Peaks detected: ", len(pkz))
        #print("Peaks rt: ", pkz.get_rt())
        #print("Peaks ms: ", pkz.get_mass_spectrum())


    return peakz


def Experiment_store(names, peakz):

    for n, p in itertools.izip(names, peakz):
        expr = Experiment(n, p)
        expr.sele_rt_range(["1m", "50m"])
        #store_expr("/home/juicebox/Desktop/Acinis/CDFdata/small_batch/expr/"+n+"11020pe2n3", expr)
        #print(n, "checked")

def main():
    start_time = timeit.default_timer()
    folder_with_cdffiles = '/home/juicebox/Desktop/Acinis/CDFdata/small_batch'
    matrixes = []
    noise = []
    ms_list = []

    names = []

    list_of_cdffiles, names = glob(glob_pattern='*.cdf', directoryname=folder_with_cdffiles)
    for cdffile, name in itertools.izip(list_of_cdffiles, names):
        #print name
        names.append(name)
        m_c = matrix_from_cdf(cdffile, name)
        matrixes.append(m_c[0])
        noise.append(m_c[1])


    # print('len=', len(matrixes))
    # print('lenN=', len(names))
    # for i, n in itertools.izip(matrixes, names):
    #
    #     masses = i.get_mass_list()
    #     print('masses=', len(masses))
    #     #print('i=', i)
    #     #print(masses)
    #     for m in masses:
    #
    #         dex = i.get_index_of_mass(m)
    #         ms = i.get_ms_at_index(dex)
    #         print('dex=', dex)
    #         #print(ms.mass_list)
    #         ms_spec = ms.mass_spec
    #         x = ms.mass_spec
    #         print('ms=', len(ms_spec))
    #         print(n, dex, ms_spec, x)
    #         ms_list.append(ms_spec)
    # #print(c)


    #print(matrixes)
    #print(noise)

    pp_im = Preprocess_IntensityMatrixes(matrixes)
    # for i, n in itertools.izip(pp_im, noise):
    #     print(i, n)
    peak_m = Peak_detector(pp_im, noise, names)
    Experiment_store(names, peak_m)

    #print(names)
    elapsed = timeit.default_timer() - start_time
    #print(elapsed)

if __name__ == "__main__":
    main()