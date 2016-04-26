#---------------------------------------------------------------------------------------------------
# This code is used for assist the use of distance-based group contribution (DBGC) method.
# The code is published under the MIT open source license.

# The MIT License (MIT)
# Copyright (c) 2016 by the DBGC Team (DBGConline@gmail.com)

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
# and associated documentation files (the "Software"), to deal in the Software without restriction, 
# including without limitation the rights to use, copy, modify, merge, publish, distribute, 
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or 
# substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING 
# BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#---------------------------------------------------------------------------------------------------

'''
This file is used to generate scripts for PM6 optimization based on the conformational analysis with 
MMFF. The conformers with low energies can be found in the energy ranking of MMFF analysis. Then the 
geometry structures will be extracted and used for PM6 optimization.

The input files are the _minimized.mol2 files in the directory _c_confSearch_Frog. The _minimized.mol2 
files contains the energy ranking of conformers based on MMFF calculation. 
The ouput files will appear in the directory _d_conformerPM6Gjfs, every sub-directory named like 
CnH2n+2_#_1_opt_PM6 in _d_conformerPM6Gjfs is an independent computational case. The .job file in the 
directory CnH2n+2_#_1_opt_PM6 is used to control the behavior of the cluster/PC, the .gjf file is the 
input for the Gaussian program. To control the number of low-energy conformers to be optimized with PM6, 
please modify the code in _d_PM6FromConfSearch.py. The related code is as below.

	moles = Frog1.readConformers(tmp_file, path=tmp_folder)
	# this code could be used to control the number of conformers selected for optimization
	# if len(moles) < 5:
	# 	tmp_num = len(moles)
	# else:
	# 	tmp_num = 5
	# 	for i in xrange(5, len(moles)):
	# 		if (moles[i].ZPE - moles[0].ZPE) > 10:
	# 			tmp_num = i
	# 			break
	print tmp_file
	tmp_num = len(moles)

To control the details of the output scripts, please modify the code in the method genFrogInputFromGjf() 
in cluter.py file.

'''

from xlrd import *
from xlwt import *
from xlutils.copy import copy

import re
import os
import shutil
import cluster
import chem
import Frog
import Balloon

#input
# the path where the jobs would lie should be announced
clusterName = 'Tsinghua100'
clusterPath = '/WORK/newGroupAdditivityFrog2/banana/validation_g_M06'
jobsPerSlot = 12

# symbol indicating the position
pattern_BalloonName = re.compile('^out_(C[0-9]*H[0-9]*_[0-9]*).*\.sdf$')
pattern_FrogName = re.compile('^(C[0-9]*H[0-9]*_[0-9]*)_minimized\.mol2$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)
cluster1._g09D01=True 
Frog1 = Frog.Frog()
Balloon1 = Balloon.Balloon()

# definetion of comparing pattern

#variables
moles = []
gjfFiles = []

#flags
BalloonOutExist = 0
FrogOutExist = 0

#counters
error_file_num = 0

# temporary variables
tmp_name = ''
tmp_num = 0
slot_num = 1

if os.path.exists('_d_conformerPM6Gjfs'):
	shutil.rmtree('_d_conformerPM6Gjfs')
os.mkdir('_d_conformerPM6Gjfs')

# if os.path.exists('_c_confSearch_Balloon'):
# 	os.chdir('_c_confSearch_Balloon')
# 	pwd = os.getcwd()
# 	tmp_folderList = os.listdir(pwd)
# 	for tmp_folder in tmp_folderList:
# 		if os.path.isfile(tmp_folder):
# 			continue
# 		BalloonOutExist = 0	
# 		tmp_fileList = os.listdir(tmp_folder)
# 		for tmp_file in tmp_fileList:
# 			tmp_m = pattern_BalloonName.match(tmp_file)
# 			if tmp_m:
# 				BalloonOutExist = 1
# 				tmp_name = tmp_m.group(1)
# 				moles = Balloon1.readConformers(tmp_file, path=tmp_folder)
# 				# this code could be used to control the number of conformers selected for optimization
# 				# if len(moles) < 5:
# 				# 	tmp_num = len(moles)
# 				# else:
# 				# 	tmp_num = 5
# 				# 	for i in xrange(5, len(moles)):
# 				# 		if (moles[i].ZPE - moles[0].ZPE) > 10:
# 				# 			tmp_num = i
# 				# 			break
# 				print tmp_file
# 				tmp_num = len(moles)
# 				if tmp_num > 99:
# 					print 'Warning! The number of comformers is more than 99!'
# 				for i in xrange(tmp_num):
# 					# _1xxx represent Balloon conformers
# 					fw = file(os.path.join('..', '_d_conformerPM6Gjfs', tmp_name + '_1' + '%03d' % i + '.gjf'), 'w')
# 					fw.write(
# '''#p b3lyp/6-31g(d) opt freq

# this is the .gjf file generated from Forg output which is used to save the coordinate of different coformers

# 0 1
# ''')
# 					for tmp_atom in moles[i].atoms:
# 						fw.write(tmp_atom.symbol + '    ' + str(tmp_atom.coordinate[0]) + '    ' + str(tmp_atom.coordinate[1]) + '    ' + str(tmp_atom.coordinate[2]) + '\n')
# 					fw.write('\n\n\n\n\n\n')
# 					fw.close()
# 		if BalloonOutExist != 1:
# 			error_file_num += 1
# 			print tmp_folder + '\tBalloon out error!'		
# 	os.chdir('../')

if os.path.exists('_c_confSearch_Frog'):
	os.chdir('_c_confSearch_Frog')
	pwd = os.getcwd()
	tmp_folderList = os.listdir(pwd)
	for tmp_folder in tmp_folderList:
		if os.path.isfile(tmp_folder):
			continue
		FrogOutExist = 0	
		tmp_fileList = os.listdir(tmp_folder)
		for tmp_file in tmp_fileList:
			tmp_m = pattern_FrogName.match(tmp_file)
			if tmp_m:
				FrogOutExist = 1
				tmp_name = tmp_m.group(1)
				moles = Frog1.readConformers(tmp_file, path=tmp_folder)
				# this code could be used to control the number of conformers selected for optimization
				# if len(moles) < 5:
				# 	tmp_num = len(moles)
				# else:
				# 	tmp_num = 5
				# 	for i in xrange(5, len(moles)):
				# 		if (moles[i].ZPE - moles[0].ZPE) > 10:
				# 			tmp_num = i
				# 			break
				print tmp_file
				tmp_num = len(moles)
				if tmp_num > 99:
					print 'Warning! The number of comformers is more than 99!'
				for i in xrange(tmp_num):
					# _2xxx represent Frog conformers
					fw = file(os.path.join('..', '_d_conformerPM6Gjfs', tmp_name + '_' + '%02d' % i + '.gjf'), 'w')
					fw.write(
'''#p b3lyp/6-31g(d) opt freq

this is the .gjf file generated from Forg output which is used to save the coordinate of different coformers

0 1
''')
					for tmp_atom in moles[i].atoms:
						fw.write(tmp_atom.symbol + '    ' + str(tmp_atom.coordinate[0]) + '    ' + str(tmp_atom.coordinate[1]) + '    ' + str(tmp_atom.coordinate[2]) + '\n')
					fw.write('\n\n\n\n\n\n')
					fw.close()
		if FrogOutExist != 1:
			error_file_num += 1
			print tmp_folder + '\tFrog out error!'		
	os.chdir('../')

# generate job directories
os.chdir('_d_conformerPM6Gjfs')
pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)
for tmp_file in tmp_fileList:
	if re.search('\.gjf', tmp_file):
		if re.search('[Tt][sS]', tmp_file):
			cluster1.setTS(True)
		else:
			cluster1.setTS(False)
		cluster1.generateJobFromGjf(tmp_file, method='PM6', freq=False)

# generate cluster script
tmp_num = 0
slot_num = 1
fw2 = file('submitFleet.sh', 'w')
fw2.write('''#!/bin/bash

source $HOME/.bash_profile

declare -i numJobs=0

''')


fw2.write('''numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done

''')

if jobsPerSlot > 1:
	tmp_fileList = os.listdir('.') 
	for tmp_file in tmp_fileList:
		if os.path.isdir(tmp_file):
			if tmp_num == 0:
				fw = file('slot_' + '%04d'%slot_num + '.sh', 'w')
				fw.write('#!/bin/bash\n\n')
			fw.write('sh ' + tmp_file + '/' + tmp_file + '''.job &
sleep 2
numJobs=`ps | grep g09 | wc -l`
while((numJobs>3))
do 
	sleep 120
	numJobs=`ps | grep g09 | wc -l`
done
''')
			tmp_num += 1
			if tmp_num >= jobsPerSlot:
				tmp_num = 0
				slot_num += 1
				fw.write('wait\n')
				fw.close()
				os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
	if tmp_num != 0:
		fw.write('wait\n')	
	fw.close()
	os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
	
	tmp_fileList = os.listdir('.')
	for tmp_file in tmp_fileList:
		if re.search('slot_.*sh', tmp_file):
			fw2.write('echo \'submit to Tsinghua100:\'\necho \'' + tmp_file + '\'\nyhbatch -N 1 ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep tsinghua_xqy | wc -l` 
while ((numJobs>63))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq |grep tsinghua_xqy | wc -l`  
done
''')

elif jobsPerSlot == 1:
	tmp_fileList = os.listdir('.')	
	for tmp_file in tmp_fileList:
		if os.path.isdir(tmp_file):
			fw2.write('sh submitTH.sh ' + tmp_file + '''
sleep 1
numJobs=`yhq |grep TH_NET | wc -l` 
while ((numJobs>28))
do
	echo $numJobs
	sleep 120
	numJobs=`yhq | grep TH_NET | wc -l`  
done
''')

fw2.close()
os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw2.name + ' > log_dos2unix.txt 2>&1')

os.chdir('../')

print '---------------------------------------\nLog of task 1\n'
print 'Gjf extracted from conformer searching output successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!' 
print '\nLog of task 2\n'
print 'PM6 opt jobs generated successfully!\n'

# THE END


