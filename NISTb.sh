#!/bin/bash

for f in $(cat $1)
do
	echo $f                                                  #Print MS_datafile.txt name
	v='C:\MYMSDS\nistTXT/'$f                                 #Store file name as V
        echo $v APPEND > /mnt/c/MYMSDS/FilespecA.FIL 	         #Write .fil pointing to V
	/mnt/c/NIST14/MSSEARCH/nistms\$.exe /INSTRUMENT /PAR=2   #Call NIST search/ run in backgroundi
	sleep 5m						 #Pause terminal	
							         #Copy & rename result file	
	cp /mnt/c/NIST14/MSSEARCH/SRCRESLT.txt  /mnt/c/MYMSDS/DATA/nist3/${f}_SRCHRESLT.txt 
        rm /mnt/c/NIST14/MSSEARCH/*.HLM	                         #Delete .HLM files 
done
