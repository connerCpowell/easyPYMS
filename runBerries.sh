#!/bin/bash

for i in $(cat $1)
do
 echo $i
 python preppeaks_GCMS.py -f /workdir2/shared_folder/cpowell/rasp_2018_sl/all/$i -n /$i/ -p 140 -s 25 -t 3 -i 3 -c /workdir2/shared_folder/cpowell/rasp_2018_sl/tmp2/ -e /workdir2/shared_folder/cpowell/rasp_2018_sl/tmp2/ 
done


