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
This file is used to generate scripts for PM6 calculation based on the initial geometry structure.

The input files should be put in the directory _a_initialGeomGjf, the input format is the 
Gaussian input format, namely, .gjf.
The output files will appear in the directory _b_PM6PreOptimization, every sub-directory 
named like CnH2n+2_#_1_opt_PM6 in _b_PM6PreOptimization is an independent computational case. 
The .job file in the directory CnH2n+2_#_1_opt_PM6 is used to control the behavior of the cluster/PC, 
the .gjf file is the input for the Gaussian program. To control the details of the output scripts, please 
modify the code in the method generateJobFromGjf() in cluster.py file.
'''

import re
import os
import shutil
import cluster
import time

#input
# the path where the jobs would lie should be announced
clusterName = 'Tsinghua100'
clusterPath = '/home/newGroupAdditivityFrog2/CnH2n+2_5'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)
cluster1.setG09D01(True)	
# definetion of comparing pattern

#variables

#flags

# temporary variables

if os.path.exists('_b_PM6PreOptimization'):
	shutil.rmtree('_b_PM6PreOptimization')
os.mkdir('_b_PM6PreOptimization')

tmp_fileList = os.listdir('_a_initialGeomGjf')
for tmp_file in tmp_fileList:
	shutil.copy(os.path.join('_a_initialGeomGjf', tmp_file), os.path.join('_b_PM6PreOptimization', tmp_file))
time.sleep(10)

os.chdir('_b_PM6PreOptimization')
pwd = os.getcwd()
tmp_fileList = os.listdir(pwd)

for tmp_file in tmp_fileList:
	if re.search('\.gjf', tmp_file):
		if re.search('[Tt][sS]', tmp_file):
			cluster1.setTS(True)
		else:
			cluster1.setTS(False)
		cluster1.generateJobFromGjf(tmp_file, method='PM6', freq=False)

print 'Jobs generated successfully!'

# THE END


