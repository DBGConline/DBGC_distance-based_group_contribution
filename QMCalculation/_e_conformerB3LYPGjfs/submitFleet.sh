#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done

echo 'submit to Tsinghua100:'
echo 'slot_0001.sh'
yhbatch -N 1 slot_0001.sh
sleep 1
numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done
echo 'submit to Tsinghua100:'
echo 'slot_0002.sh'
yhbatch -N 1 slot_0002.sh
sleep 1
numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done
echo 'submit to Tsinghua100:'
echo 'slot_0003.sh'
yhbatch -N 1 slot_0003.sh
sleep 1
numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done
