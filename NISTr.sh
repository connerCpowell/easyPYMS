#!/bin/bash

for f in $(cat $1)
do
	echo $f
	v='C:\MYMSDS\DATA\NIST_rdy/'$f
	#cat $v
        echo $v APPEND > /mnt/c/MYMSDS/FilespecA.FIL 	
	#echo 'C:\MYMSDS\DATA\NIST_rdy\'$f APPEND > /mnt/c/MYMSDS/FilespecA.FIL
	#cat 'C:\MYMSDS\DATA\NIST_rdy\'$f
	/mnt/c/NIST14/MSSEARCH/nistms\$.exe /INSTRUMENT /PAR=10
	sleep 5m
	cp /mnt/c/NIST14/MSSEARCH/SRCRESLT.txt  /mnt/c/MYMSDS/DATA/NIST_out2/${f}_SRCHRESLT.txt
        rm /mnt/c/NIST14/MSSEARCH/*.HLM	
done
