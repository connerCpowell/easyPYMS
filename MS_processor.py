import sys
import csv
import heapq


def main():

    ratio_set = []
    acRatio = []
    bigOnes = []


    inny = sys.argv[1]
    #print (inny)
    n = inny.split('_data/')
    name = n[1]
    print(name)

    # reader = csv.reader(inny)
    with open(inny, 'r') as f:
        next(f)
        for line in f:
            sline = line.split(',')
            #print(sline)
            ratios = []
            maxi = max(map(float, sline))
            loc = sline.index(str(maxi))

            print(maxi, loc)

            c = 0
            for i in sline:
                c += 1
                loc2 = sline.index(str(i))
                #print('l=', loc2)
                r = float(i) / float(maxi)
                ratios.append([float(i), loc2])
                #print(loc2, i, c)   0.0 always refers to first 0.0 occurance.

            ratio_set.append(ratios)

        #print(ratio_set)
        larges = []
        for ratios in ratio_set:
            l = heapq.nlargest(10, ratios[0])
            print(l)
            #larges.append(l)

        #print(larges)
        bigOnes.append(larges)
    # print(bigOnes)


            # for i in range(1, 10):
            #     max1 = 0
            #     for j in range(len(ratios)):
            #         if ratios[j] > max1:
            #             max1 = ratios[j]
            #
            #         ratios.remove(max1)
            #         bigOnes.append(max1)
            #
            # print(bigOnes)



        #print(ratio_set)




if __name__ == "__main__":
    main()