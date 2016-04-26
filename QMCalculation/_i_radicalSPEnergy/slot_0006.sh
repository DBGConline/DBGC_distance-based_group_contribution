#!/bin/bash

sh C6H14_5_r005_C1_3_SP_M06/C6H14_5_r005_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r006_C9_3_SP_M06/C6H14_5_r006_C9_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r007_C17_3_SP_M06/C6H14_5_r007_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r008_C1_3_SP_M06/C6H14_5_r008_C1_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r009_C13_3_SP_M06/C6H14_5_r009_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r010_C13_3_SP_M06/C6H14_5_r010_C13_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r011_C9_3_SP_M06/C6H14_5_r011_C9_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r012_C6_3_SP_M06/C6H14_5_r012_C6_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r013_C9_3_SP_M06/C6H14_5_r013_C9_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_r014_C17_3_SP_M06/C6H14_5_r014_C17_3_SP_M06.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
