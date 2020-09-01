from scipy.spatial import distance_matrix
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from collections import OrderedDict
import sys

def distance(lista, listb):
    return sum((b - a) ** 2 for a,b in zip(lista, listb)) ** .5

def get_data(line, num):
    try:
        x = float(line.split(',')[num].strip())
        #print('gd_x=', x)
        return x
    except:
        return 0


def nameClean(names):

    name2 = []
    for n in names:
        print('n=', n)
        if str(n).endswith('.cdf"'):
            # print('yes')
            na = n.strip('.cdf"')

            # na2 = na.replace("_", ".")
            na3 = na.replace("-", ".")
            # na4 = na3.split('_')[1:]
            # na4 = na3.split('_')[1]
            print('name3=', na3)
            # print('na3=', na3)
            # print('na='+na)
            name2.append(str(na3))
        else:
            print('no')

    return name2

file = sys.argv[1]

#with open('/home/cocopalacelove/tmp/sb_out/beta1_area.csv', 'r') as f:
with open(file, 'r') as f:
    i = 0
    species_dict = OrderedDict()
    list_o_species = []
    total = 0
    for line in f:
        # print('line=', line)
        num = line.count('\t')
        num2 = line.count(',')

        # print('num=', line.count('\t'))
        # print('num2=', line.count(','))

        if num > 0:
            total = num + 1
            print('total=' + str(total))
        print('i1=', i)

        if i != 0:
            count = 0
            for j in range(num2):
                y =  get_data(line, j)
                #print('y='+str(y))
                #count += 1
                #print('c='+str(count))
                # print('d=', str(len(species_dict)))
                # print('l=', str(len(list_o_species)))
                # print('jx=', get_data(line, j))
                species_dict[list_o_species[j]].append(get_data(line, j+1))
                #print('j='+str(j)+ '\n')
        else:
            for i in range(num2):
                print('rang_n2', range(num2))
                print('i0=', i)
                j = i+1

                species_dict[line.split(',')[j].strip()] = []
                u = line.split(',')[j].strip()
                print('u='+str(u)+'\n')
                x = line.split(',')[j].strip()
                list_o_species.append(x)
            #print('len='+ str(len(list_o_species)))
        i = 1
        #print( 'total='+str(total))
    print(species_dict)

# for i in species_dict:
#     print(i.items())


dm_list =[]
names = []
name2 = []

x =0
for l in species_dict:
    if x == 0:
        print(l)
        x += 1
    else:
        print(l, species_dict[l])
        dm_list.append(species_dict[l])
        names.append(l)
        #print(l)
        # if l.endswith('1.cdf'):
        #     print('yes')
        # else:
        #     print('no')
print('names=', names)




for n in names:
    print('n=', n)
    if str(n).endswith('.cdf"'):
        print('yes')
        na = n.strip('.cdf"')

        na2 = na.replace("_", ".")
        na3 = na2.replace("-", ".")
        print('na3=', na3)
        #print('na='+na)
        name2.append(na3)
    else:
        print('no')




#print('dmL len', len(dm_list))
#print('dm_list', dm_list)
print('name2', name2)

# print('dm5', dm_list[5])

#
d = distance_matrix(dm_list, dm_list)
#print(d)

linked = linkage(d, 'ward')

# labelList = range(1, 25)

plt.figure(figsize=(10,10))
dendrogram(linked,
            orientation='top',
            labels=name2,
            distance_sort='descending',
            show_leaf_counts=True)


            


plt.savefig('rasp2018_87c.svg', format="svg")
plt.show()