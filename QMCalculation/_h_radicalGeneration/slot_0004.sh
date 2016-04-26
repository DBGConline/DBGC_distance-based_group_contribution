#!/bin/bash

sh C6H14_3_r009_C1_2_opt_B3L/C6H14_3_r009_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r010_C13_2_opt_B3L/C6H14_3_r010_C13_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r011_C1_2_opt_B3L/C6H14_3_r011_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r012_C10_2_opt_B3L/C6H14_3_r012_C10_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r013_C5_2_opt_B3L/C6H14_3_r013_C5_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_r014_C1_2_opt_B3L/C6H14_3_r014_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r001_C17_2_opt_B3L/C6H14_4_r001_C17_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r002_C13_2_opt_B3L/C6H14_4_r002_C13_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r003_C1_2_opt_B3L/C6H14_4_r003_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r004_C13_2_opt_B3L/C6H14_4_r004_C13_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r005_C5_2_opt_B3L/C6H14_4_r005_C5_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_r006_C1_2_opt_B3L/C6H14_4_r006_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
