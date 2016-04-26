#!/bin/bash

sh C6H14_1_2_opt_B3L/C6H14_1_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_2_2_opt_B3L/C6H14_2_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_3_2_opt_B3L/C6H14_3_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_4_2_opt_B3L/C6H14_4_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_2_opt_B3L/C6H14_5_2_opt_B3L.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
