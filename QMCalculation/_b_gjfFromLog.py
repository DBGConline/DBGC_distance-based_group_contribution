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
This file is used to extract the optimized geometry at PM6 level of theory from the .log file. 

The input files is the completed case in the directory _b_initialGeomGjf, this .py file will read 
the .log files in the sub-directories in _b_initialGeomGjf and extract the optimized geometry. The
.log file is the output of Gaussian computation. By default the standard orientation in the .log 
file will be used, if the key word like nosym used, the code tmp_m = pattern_standard.match(tmp_line) 
should replaced with tmp_m = pattern_input.match(tmp_line).
The output files will appear in the directory _c_confSearch. They are the optimized geometry 
coordinates in .gjf format.
'''

import re
import os
import shutil
import cluster
import time
import textExtractor

#input
# the path where the jobs would lie should be announced
clusterName = 'Tsinghua100'
clusterPath = '/home/newGroupAdditivityFrog2/CnH2n+2_6'

# symbol indicating the position
pattern_name = re.compile('^(C[0-9]*H[0-9]*_[0-9]*)_.*$')
pattern_multi = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_optimized = re.compile('^.*Optimized Parameters.*$') 
pattern_standard = re.compile('^.*Standard orientation:.*$') 
pattern_input = re.compile('^.*Input orientation:.*$') 
pattern_endline = re.compile('^.*---------------------------------------------------------------------.*$')
pattern_end = re.compile('^.*Normal termination of Gaussian 09.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)

# definetion of comparing pattern

#variables
multi = 1

#flags
logExist = 0
multi_done = 0
optimized_done = 0
standard_done = 0
coordinate_done =0

#counters
error_file_num = 0

# temporary variables

if os.path.exists('_c_confSearch'):
	shutil.rmtree('_c_confSearch')
os.mkdir('_c_confSearch')

os.chdir('_b_PM6PreOptimization')
pwd = os.getcwd()
tmp_folderList = os.listdir(pwd)
for tmp_folder in tmp_folderList:
	if os.path.isfile(tmp_folder):
		continue
	tmp_m = pattern_name.match(tmp_folder)
	if tmp_m:
		tmp_name = tmp_m.group(1)
	else:
		print 'Error! Invalid folder name!'
		continue

	logExist = 0
	tmp_fileLists = os.listdir(tmp_folder)
	for tmp_file in tmp_fileLists:
		if re.search('\.log', tmp_file):
			logExist = 1

			multi_done = 0
			optimized_done = 0
			standard_done = 0
			coordinate_done =0

			fr = file(os.path.join(tmp_folder, tmp_file), 'r')
			tmp_lines = fr.readlines()
			tmp_m = pattern_end.match(tmp_lines[-1])
			if tmp_m:
				for (lineNum, tmp_line) in enumerate(tmp_lines):
					if multi_done != 1:
						tmp_m = pattern_multi.match(tmp_line)
						if tmp_m:
							multi = int(tmp_m.group(1))
							multi_done = 1
					elif optimized_done != 1:
						tmp_m = pattern_optimized.match(tmp_line)
						if tmp_m:
							optimized_done = 1
					elif standard_done != 1:
						tmp_m = pattern_standard.match(tmp_line)
						if tmp_m:
							tmp_num = lineNum + 5
							standard_done = 1
					elif coordinate_done != 1:
						tmp_m = pattern_endline.match(tmp_line)
						if tmp_m:
							if lineNum > tmp_num:
								tmp_geom = textExtractor.geometryExtractor(tmp_lines[tmp_num: lineNum])
								coordinate_done = 1
				fw = file(os.path.join('..', '_c_confSearch', tmp_name+'.gjf'), 'w')
				fw.write(
'''%mem=28GB
%nprocshared=12
%chk=''' + tmp_file[0:-4] + '''.chk
#p B3LYP/6-31G(d) opt freq

using B3LYP/6-31G(d) to do opt and freq calc.

0 '''+str(multi) + '\n' + tmp_geom + '\n\n\n\n\n\n')
				fw.close()
				# print tmp_file + '\tsuccess'
			else:
				print tmp_folder + '\terror'
				error_file_num += 1
	if logExist != 1:
		print tmp_folder + '\terror'
		error_file_num += 1

os.chdir('../')

print '\n Gjf extracted from log successfully!'
print 'error_file_num:\t' + str(error_file_num)
if error_file_num == 0:
	print 'All are successful log files!'

# THE END


