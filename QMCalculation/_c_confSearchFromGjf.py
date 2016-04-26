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
This file is used to generate scripts for MMFF conformational analysis with the Frog2 code, 
based on the initially optimized structure. 

The input files are the .gjf files in the directory _c_confSearch.  The .gjf files contains the 
initially optimized structures.
The ouput files will appear in the directory _c_confSearch_Frog, every sub-directory named like 
CnH2n+2_#_1_confSearch in _c_confSearch_Frog is an independent computational case. The .job file in 
the directory CnH2n+2_#_1_confSearch is used to control the behavior of the cluster/PC, the .sdf
file is the input for the Frog2 program. To control the details of the output scripts, please 
modify the code in the method genFrogInputFromGjf() in cluter.py file.

The Frog program can be download at https://github.com/tuffery/Frog2. 
Ref papers about Frog2: T.B. Leite et al., Acids Res. 35 (2007) W568-W572, 
and M.A. Miteva et al., Nucl. Acids Res. 38 (2010) 622-627.

The OpenBabel program is also used for file format conversion. 
Info about OpenBabel and downloading: http://openbabel.org/wiki/Main_Page. 
To change the environment path of OpenBabel, please modify the code in the method
genFrogInputFromGjf() in cluter.py file.

'''

from xlrd import *
from xlwt import *
from re import *
import re
import os
import shutil
import cluster
import chem


#input
# the path where the jobs would lie should be announced
clusterName = 'Tsinghua100'
clusterPath = '/home/newGroupAdditivityFrog2/CnH2n_5'

# symbol indicating the position
pattern_name = re.compile('^.*.*$')

# constants
cluster1 = cluster.cluster(clusterName, clusterPath)
cluster1.setJmolPath('jmol-14.2.15_2015.07.09')

# definetion of comparing pattern

#variables
gjfFiles = []

#flags

# temporary variables

# if os.path.exists('_c_confSearch_Balloon'):
# 	shutil.rmtree('_c_confSearch_Balloon')
# shutil.copytree('_c_confSearch', '_c_confSearch_Balloon')
# os.chdir('_c_confSearch_Balloon')
# pwd = os.getcwd()
# tmp_fileLists = os.listdir(pwd)

# for tmp_file in tmp_fileLists:
# 	if re.search('\.gjf', tmp_file):
# 		gjfFiles.append(tmp_file)
			
# cluster1.genBalloonInputFromGjf(gjfFiles)
# os.chdir('../')

if os.path.exists('_c_confSearch_Frog'):
	shutil.rmtree('_c_confSearch_Frog')
shutil.copytree('_c_confSearch', '_c_confSearch_Frog')
os.chdir('_c_confSearch_Frog')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)

for tmp_file in tmp_fileLists:
	if re.search('\.gjf', tmp_file):
		gjfFiles.append(tmp_file)
			
cluster1.genFrogInputFromGjf(gjfFiles)
os.chdir('../')

print 'Jobs generated successfully!'

# THE END


