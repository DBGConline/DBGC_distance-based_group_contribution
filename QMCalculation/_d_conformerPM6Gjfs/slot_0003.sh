#!/bin/bash

sh C6H14_5_01_1_opt_PM6/C6H14_5_01_1_opt_PM6.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
sh C6H14_5_02_1_opt_PM6/C6H14_5_02_1_opt_PM6.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
wait
