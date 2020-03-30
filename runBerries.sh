#!/bin/bash

for i in $(cat $1)
do
 python berryPipe.py /workdir2/shared_folder/cpowell/fielTmp/all/$i /2016_blueberry_gwas/ 140 25 3 3 /workdir2/shared_folder/cpowell/OPtmp/csv_2016/ /workdir2/shared_folder/cpowell/OPtmp/expr_2016/ &
done


