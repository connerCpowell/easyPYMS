from scipy.spatial import distance_matrix
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
from collections import OrderedDict

def distance(lista, listb):
    return sum((b - a) ** 2 for a,b in zip(lista, listb)) ** .5

def get_data(line, num):
    try:
        return float(line.split('\t')[num].strip())
    except:
        return 0

with open('/home/juicebox/Desktop/Acinis/CDFdata/all_csv/all_9025pe2n3p233_area.csv', 'r') as f:
    i = 0
    species_dict = OrderedDict()
    list_o_species = []
    total = 0
    for line in f:
        #print(line)
        num = line.count('\t')
        print('num=' + str(num))
        if num > 0:
            total += num +1
            #print('total=' + str(total))
        if i != 0:
            count = 0
            for j in range(num-1):
                y =  get_data(line, j)
                print('y='+str(y))
                #count += 1
                #print('c='+str(count))
                print('d=', str(len(species_dict)))
                print('l=', str(len(list_o_species)))
                #print('jx=', get_data(line, j))
                species_dict[list_o_species[j]].append(get_data(line, j+1))
                print('j='+str(j)+ '\n')
        else:
            for i in range(num):
                print(i)
                j = i+1

                species_dict[line.split('\t')[j].strip()] = []
                u = line.split('\t')[j].strip()
                print('u='+str(u)+'\n')
                x = line.split('\t')[j].strip()
                list_o_species.append(x)
            #print('len='+ str(len(list_o_species)))
        i = 1
        #print( 'total='+str(total))
    #print( species_dict)


dm_list =[]
names = []
name2 = []

for l in species_dict:
    #print l, species_dict[l]
    print('line=', l)
    dm_list.append(species_dict[l])
    names.append(l)
    #print(l)
    # if l.endswith('1.cdf'):
    #     print('yes')
    # else:
    #     print('no')

for n in names:
    print('na=',n)

    if n.endswith('1.cdf'):
        print('yes')
        m = n.strip('-')
        #print('m='+m)
        na = m[3:-4]
        #print('na='+na)
    name2.append(na)

print(name2)

d = distance_matrix(dm_list, dm_list)
print(d)

linked = linkage(d, 'average')

labelList = range(1, 25)

plt.figure(figsize=(10,10))
dendrogram(linked,
            orientation='top',
            labels=name2,
            distance_sort='descending',
            show_leaf_counts=True)

#plt.savefig('blue_p120s30pe10n3_p34.png')
plt.show()