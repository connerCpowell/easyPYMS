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
        #print(root, dirnames, filenames)
        for filename in fnmatch.filter(filenames, glob_pattern):
            #print(filename)
            absolute_filepath = os.path.join(root, filename)
            #print(absolute_filepath)
            matches.append(absolute_filepath)

            name = absolute_filepath.rsplit('/all_expr')[-1]
            print('name=', name)
            names.append(name)

    print('names=', names)
    print(matches)

    return matches, names


def lil_dictor(cdfs):

    breed_dict = {}
    name_dict = {}


    for i in cdfs:
        a = i.split('-')
        print a
        b = list(a)
        #print a
        print b[1]

        if b[1] in breed_dict:
            expr = load_expr(i)
            name_dict[b[1]].append(i)
            breed_dict[b[1]].append(expr)
        else:
            expr = load_expr(i)
            name_dict[b[1]] = [i]
            breed_dict[b[1]] = [expr]

    #print breed_dict
    return breed_dict, name_dict

def dictor(breed, cdfs):


    breed_dict = {}
    name_dict = {}
    b_list = []

    for i in cdfs:
        if str(breed) in str(i):

            b_list.append(i)



    for ber in b_list:
        a = ber.split('-')
        print ('a=', a)
        b = list(a)
        #print a
        print ('b[1]=',b[1])

        if b[1] in breed_dict:
            expr = load_expr(ber)
            name_dict[b[1]].append(ber)
            breed_dict[b[1]].append(expr)
        else:
            expr = load_expr(ber)
            name_dict[b[1]] = [ber]
            breed_dict[b[1]] = [expr]

    #print breed_dict
    return breed_dict, name_dict

def aligner(exprs, bers, names):

    mod = 2.5
    gp = 0.30

    mA = 10.0

    # print exprs
    # print names


    for dict, n, b in zip(exprs, names, bers):
        print dict
        print '\n'
        print b
        print n
        print '\n'


        #for item, na in zip(dict.items(), n.items()):
        for item, v in dict.items():
            print item
            # print v
            F1 = exprl2alignment(v)
            T1 = PairwiseAlignment(F1, mod, gp)
            A1 = align_with_tree(T1, min_peaks=2)

            A1.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/CDF/output/'+item+'rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/CDF/output/'+item+'area.csv')

            # for typ, rep in item:
            #     print 'k=' + typ + '\n'
            #     print 'v=' + rep + '\n'

        # for key, values in dict:
        #     print 'k='+key+'\n'
        #     print 'v='+values+'\n'




            # for expr, berry in zip(item, na):
            #     print "expr"+str(expr)
            #     print "berry"+str(berry)



            # F1 = exprl2alignment(item)
            # T1 = PairwiseAlignment(F1, mod, gp)
            # A1 = align_with_tree(T1, min_peaks=2)
            #
            #
            # A1.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/CDF/output/', '/home/juicebox/Desktop/Acinis/CDFdata/CDF/output/clean_p110_s30_%2_n3area.csv')

def align2(exprs, names, bers):
    min = 1.5
    mod = 2.5

    gp = 0.30

    #mA = 10.0

    print()

    for dict, n, b in zip(exprs, names, bers):
        #print ('dict='+dict)
        #print '\n'
        #print ('b='+str(b))
        print ('b='+str(b))
        print '\n'
        T2 = []


        #for item, na in zip(dict.items(), n.items()):
        for item, v in dict.items():
            print ('item='+str(item))
            # print v
            F1 = exprl2alignment(v)
            T1 = PairwiseAlignment(F1, min, gp)
            A1 = align_with_tree(T1, min_peaks=2)
            T2.append(A1)

        T3 = PairwiseAlignment(T2, mod, gp)
        A2 = align_with_tree(T3, min_peaks=2)

        # print'b='+str(b)
        # print'n=' + str(n)

        A2.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/CDF/output2/'+str(b)+'_7035rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/CDF/output2/'+str(b)+'_7035area.csv')





def alignAll(exprs, bers, names):
    mod = 2.5
    gp = 0.30
    gp2 = 0.5

    mA = 10.0

    bG = []
    Tall = []

    for dict, n, b in zip(exprs, names, bers):
        print ('dict=', dict)
        print '\n'
        #print b
        print ('n=', n)
        print '\n'

        T2 = []
        # for item, na in zip(dict.items(), n.items()):
        for item, v in dict.items():
            print('itemCount=', len(dict.items()))
            print ('item=', item)
            # print v
            F1 = exprl2alignment(v)
            T1 = PairwiseAlignment(F1, mod, gp)
            A1 = align_with_tree(T1, min_peaks=2)
            T2.append(A1)

        print('t2=', T2)
        T3 = PairwiseAlignment(T2, mA, gp2)
        A2 = align_with_tree(T3, min_peaks=3)
        Tall.append(A2)

    T4 = PairwiseAlignment(Tall, mA, gp2)
    A3 = align_with_tree(T4, min_peaks=3)
    #

        # print'b='+str(b)
        # print'n=' + str(n)

    A3.write_csv('/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_10020pe2n3p233_rt.csv', '/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_10020pe2n3p233_area.csv')








def main():

    berrs = ['bk', 'be', 'rp', 'sw']

    folder_with_cdffiles = '/home/juicebox/Desktop/Acinis/CDFdata/all_expr'

    cdfs, names = glob(glob_pattern="*10020pe2n3", directoryname= folder_with_cdffiles)

    print cdfs

    thictionary = []
    naNames = []


    for i in berrs:
        b, n = dictor(i, cdfs)
        thictionary.append(b)
        naNames.append(n)

    # b, n = lil_dictor(cdfs)
    # print('b='+str(b))
    # print('n='+str(n)+'\n')
    # align2(b, n)


       # print 'n='+str(n)
       #
       #  print '\n'
       #  for k,v in b.items():
       #      print k, v

    # print naNames
    # print len(naNames)
    # print '\n'
    # print ('thick=', thictionary)
    # print ('thcnkLen=', len(thictionary)
    # print '\n'


    #aligner(thictionary, naNames, berrs)
    #align2(thictionary, naNames, berrs)
    alignAll(thictionary, naNames, berrs)

    # for i in thictionary:
    #     print '\n'+str(i)

if __name__ == "__main__":
    main()