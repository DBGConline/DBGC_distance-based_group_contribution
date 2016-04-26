#!/bin/bash

sh C6H14_1_r001_C14_2_opt_B3L/C6H14_1_r001_C14_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r002_C17_2_opt_B3L/C6H14_1_r002_C17_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r003_C11_2_opt_B3L/C6H14_1_r003_C11_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r004_C14_2_opt_B3L/C6H14_1_r004_C14_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r005_C11_2_opt_B3L/C6H14_1_r005_C11_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r006_C1_2_opt_B3L/C6H14_1_r006_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r007_C5_2_opt_B3L/C6H14_1_r007_C5_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r008_C1_2_opt_B3L/C6H14_1_r008_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r009_C1_2_opt_B3L/C6H14_1_r009_C1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r010_C5_2_opt_B3L/C6H14_1_r010_C5_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r011_C8_2_opt_B3L/C6H14_1_r011_C8_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_1_r012_C8_2_opt_B3L/C6H14_1_r012_C8_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
