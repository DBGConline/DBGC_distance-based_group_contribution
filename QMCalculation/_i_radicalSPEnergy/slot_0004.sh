#!/bin/bash

sh C6H14_3_r009_C1_3_SP_M06/C6H14_3_r009_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r010_C13_3_SP_M06/C6H14_3_r010_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r011_C1_3_SP_M06/C6H14_3_r011_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r012_C10_3_SP_M06/C6H14_3_r012_C10_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r013_C5_3_SP_M06/C6H14_3_r013_C5_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r014_C1_3_SP_M06/C6H14_3_r014_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r001_C17_3_SP_M06/C6H14_4_r001_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r002_C13_3_SP_M06/C6H14_4_r002_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r003_C1_3_SP_M06/C6H14_4_r003_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r004_C13_3_SP_M06/C6H14_4_r004_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r005_C5_3_SP_M06/C6H14_4_r005_C5_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r006_C1_3_SP_M06/C6H14_4_r006_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
