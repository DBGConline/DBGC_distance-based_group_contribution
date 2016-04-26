#!/bin/bash

sh C6H14_2_r011_C13_3_SP_M06/C6H14_2_r011_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r012_C10_3_SP_M06/C6H14_2_r012_C10_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r013_C17_3_SP_M06/C6H14_2_r013_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r014_C1_3_SP_M06/C6H14_2_r014_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r001_C17_3_SP_M06/C6H14_3_r001_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r002_C5_3_SP_M06/C6H14_3_r002_C5_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r003_C17_3_SP_M06/C6H14_3_r003_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r004_C8_3_SP_M06/C6H14_3_r004_C8_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r005_C13_3_SP_M06/C6H14_3_r005_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r006_C10_3_SP_M06/C6H14_3_r006_C10_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r007_C13_3_SP_M06/C6H14_3_r007_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r008_C17_3_SP_M06/C6H14_3_r008_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
