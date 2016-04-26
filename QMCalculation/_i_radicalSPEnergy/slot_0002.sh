#!/bin/bash

sh C6H14_1_r013_C17_3_SP_M06/C6H14_1_r013_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r014_C17_3_SP_M06/C6H14_1_r014_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r001_C7_3_SP_M06/C6H14_2_r001_C7_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r002_C7_3_SP_M06/C6H14_2_r002_C7_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r003_C5_3_SP_M06/C6H14_2_r003_C5_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r004_C17_3_SP_M06/C6H14_2_r004_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r005_C13_3_SP_M06/C6H14_2_r005_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r006_C17_3_SP_M06/C6H14_2_r006_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r007_C10_3_SP_M06/C6H14_2_r007_C10_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r008_C1_3_SP_M06/C6H14_2_r008_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r009_C13_3_SP_M06/C6H14_2_r009_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_r010_C1_3_SP_M06/C6H14_2_r010_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
