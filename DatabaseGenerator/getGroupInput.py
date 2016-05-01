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
This file is used to generate the database containing the standard enthalpy of formation (unit: kcal/mol) 
and group contribution vector at the M062X/def2TZVP//B3LYP/6-31G(d) level of theory. During the calculation 
of the standard enthalpy of formation, a virtual reaction xC(g)+y/2H2(g)+z/2O2(g)=CxHyOx(g) is constructed. 
The standard enthalpy of formation of CxHyOx can be calculated with 
Hf298(CxHyOz(g))-xHf298(C(g))-y/2Hf298(H2(g))-z/2Hf298(O2(g))=Hf298_DFT(CxHyOz)-xHf298_DFT(C(g))-y/2Hf298_DFT(H2(g))-z/2Hf298_DFT(O2(g)), 
namely, 
Hf298(CxHyOz(g))=Hf298_DFT(CxHyOz)-xHf298_DFT(C(g))-y/2Hf298_DFT(H2(g))-z/2Hf298_DFT(O2(g))+xHf298(C(g)), 
because Hf298(H2(g))=0, and Hf298(O2(g))=0. 
The standard enthalpy of formation of C(g) used is not the experimental value, but an average value calculated 
from 89 aliphatic species at the same level of quantum theory used in the construction of the database, thus 
bringing an effect of error cancellation.

The input file is database.xlsx. It can be generated with getGroupDataBaseFromLog.py, or be obtained based on 
one's own data source. 

The output file is inputFile.xlsx and inputFile_m.xlsx. In the inputFile.xlsx, the data is arranged with the 
order of names of species in the database. In the inputFile_m.xlsx, the species with the same group contribution 
vectors are combined into the same row. Therefore, all the conformers through internal rotation will be listed 
in the same row and ranked in the order of energy in inputFile_m.xlsx. This is an advantage for picking out the 
lowest-energy conformer. It should be acknowledged that in current stage the cis-tran isomers has the same group 
contribution vector, and can't be distinguished. In most of the situations, the tran structure for alkene has a 
lower energy than cis structure, thus ranking before the cis structure.

'''

import re
import os 
import time
import numpy as np
import xlsxwriter
import xlrd

import chem
import thermoDatabase

# get commands from .name file
__energy__ = 'b3lyp'
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[3].strip(' \n')
		if tmp_line == 'cbs':
			__energy__ = 'CBS-QB3'
			# note that if __energy__ == 'cbs', a cbs freq check would be used. 
			# Sometimes another opt and freq would be done before cbs. This check is used to skip reading the information of other methods. 
			print '\n-------------------------------------\ncbs freq and energy are used in this calculation\n-------------------------------------\n'
		elif re.match('b3lyp', (tmp_line.strip()).lower()) != None:
			__energy__ = tmp_line.strip()
			print '\n-------------------------------------\nb3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'cbsb3lyp':
			__energy__ = 'cbsb3lyp'
			print '\n-------------------------------------\ncbs verified and b3lyp freq and energy are used in this calculation\n-------------------------------------\n'
		elif tmp_line == 'M062X/def2TZVP//B3LYP/6-31G(d)':
			__energy__ = 'M062X/def2TZVP//B3LYP/6-31G(d)'
			print '\n-------------------------------------\nM062X energy and b3lyp geom are used in this calculation\n-------------------------------------\n'	
		elif tmp_line == 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)':
			__energy__ = 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)'
			print '\n-------------------------------------\nM062X energy and B3LYP-GD3BJ geom are used in this calculation\n-------------------------------------\n'	
		elif tmp_line == 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)':
			__energy__ = 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)'
			print '\n-------------------------------------\nM062X-GD3 energy and B3LYP-GD3BJ geom are used in this calculation\n-------------------------------------\n'	
		else:
			print '\n-------------------------------------\nWarning! CBS or b3lyp energy is not announced! CBS is used as default!\n-------------------------------------\n'
		fr.close()	

#####################################################################
# read data from the database excel file and generate input file
#####################################################################
wb=xlrd.open_workbook('database.xlsx')
sh=wb.sheet_by_name('speciesInfo')

# definition of variables
all_moles = []
all_groups = set()
groupIndex = {}

# definition of temporary variables
tmp_name = ''
tmp_energy = 0.0
tmp_geom = ''
num_rows = sh.nrows
num_cols = sh.ncols
tmp_groups = []

# read info from database
for tmp_row in xrange(1, num_rows):
	tmp_groups = []
	tmp_mole = chem.molecule()

	tmp_name = sh.cell_value(tmp_row, 0)
	tmp_formula = sh.cell_value(tmp_row, 2)
	tmp_energy = sh.cell_value(tmp_row, 9)
	tmp_geom = sh.cell_value(tmp_row, 12)
	tmp_geom = tmp_geom.strip()
	tmp_geom = tmp_geom.split('\n')
	tmp_mole.getGjfGeom(tmp_geom)
	tmp_mole.setLabel(tmp_name)
	tmp_mole.fulfillBonds()

	# update the energy as enthalpy of formation at 298.15 K
	tmp_mole.calcFormula()
	if tmp_formula != tmp_mole.formula:
		print 'Error! The formula in the database is difference from the geometry!'
	# note that the refEnthalpy0 used here is not real refEnthalpy0, but refEnthalpy298, thus H298mH0 = 0.0
	tmp_energy = thermoDatabase.getFormationH(formula = tmp_formula, refQMMethod = __energy__, refEnthalpy0 = tmp_energy, H298mH0 = 0.0)
	# tmp_energy = thermoDatabase.getEnthalpyDifference(formula = tmp_formula, refQMMethod = __energy__, refEnthalpy0 = tmp_energy, H298mH0 = 0.0)
	# tmp_energy = thermoDatabase.getAtomizationEnergy(formula = tmp_formula, refQMMethod = __energy__, refEnergy0 = tmp_energy)
	# note that this is not real ZPE, but reference energy 
	# currently tmp_energy is the entaly of formation at 298.15 K
	tmp_mole.setZPE(tmp_energy)

	tmp_groups = tmp_mole.get1stOrderGroup()
	all_moles.append(tmp_mole)
	all_groups = all_groups | set(tmp_groups)

# generate input file
localtime = time.asctime(time.localtime(time.time()))
print localtime
groupIndex = {}
all_groups = sorted(list(all_groups))
N = len(all_groups)
n = len(all_moles)

wb2 = xlsxwriter.Workbook('inputFile.xlsx')
sh2 = wb2.add_worksheet('inputVectors')
sh3 = wb2.add_worksheet('acyclic')
sh4 = wb2.add_worksheet('cyclic')

tmp2_row = 0
tmp2_col = 0
sh2.write(tmp2_row, tmp2_col, 'ID')
sh2.write(tmp2_row, tmp2_col+1, 'Name')
sh2.write(tmp2_row, tmp2_col+2, 'ReferenceEnergy')
sh2.write(tmp2_row, tmp2_col+3, 'TotalDimesionNumber')
sh2.write(tmp2_row, tmp2_col+5, 'DimentionIndex')

tmp2_row = 1
sh2.write(tmp2_row, tmp2_col+3, N*(N+3)/2)

tmp2_col = 5
for i in xrange(N*(N+3)/2):
	sh2.write(tmp2_row, tmp2_col+i, i+1)

tmp2_row = 2 
for i in xrange(N):
	sh2.write(tmp2_row, tmp2_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp2_col
	tmp2_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh2.write(tmp2_row, tmp2_col, tmp_text)
		groupIndex[tmp_text] = tmp2_col
		tmp2_col += 1

tmp3_row = 0
tmp3_col = 0
sh3.write(tmp3_row, tmp3_col, 'ID')
sh3.write(tmp3_row, tmp3_col+1, 'Name')
sh3.write(tmp3_row, tmp3_col+2, 'ReferenceEnergy')
sh3.write(tmp3_row, tmp3_col+3, 'TotalDimesionNumber')
sh3.write(tmp3_row, tmp3_col+5, 'DimentionIndex')

tmp3_row = 1
sh3.write(tmp3_row, tmp3_col+3, N*(N+3)/2)

tmp3_col = 5
for i in xrange(N*(N+3)/2):
	sh3.write(tmp3_row, tmp3_col+i, i+1)

tmp3_row = 2 
for i in xrange(N):
	sh3.write(tmp3_row, tmp3_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp3_col
	tmp3_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh3.write(tmp3_row, tmp3_col, tmp_text)
		groupIndex[tmp_text] = tmp3_col
		tmp3_col += 1

tmp4_row = 0
tmp4_col = 0
sh4.write(tmp4_row, tmp4_col, 'ID')
sh4.write(tmp4_row, tmp4_col+1, 'Name')
sh4.write(tmp4_row, tmp4_col+2, 'ReferenceEnergy')
sh4.write(tmp4_row, tmp4_col+3, 'TotalDimesionNumber')
sh4.write(tmp4_row, tmp4_col+5, 'DimentionIndex')

tmp4_row = 1
sh4.write(tmp4_row, tmp4_col+3, N*(N+3)/2)

tmp4_col = 5
for i in xrange(N*(N+3)/2+1):
	sh4.write(tmp4_row, tmp4_col+i, i+1)

tmp4_row = 2 
for i in xrange(N):
	sh4.write(tmp4_row, tmp4_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp4_col
	tmp4_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh4.write(tmp4_row, tmp4_col, tmp_text)
		groupIndex[tmp_text] = tmp4_col
		tmp4_col += 1
sh4.write(tmp4_row, tmp4_col, 'CycleSize')

tmp2_row = 3
tmp2_col = 5
tmp3_row = 3
tmp3_col = 0
tmp4_row = 3
tmp4_col = 0
for i in xrange(n):
	for j in xrange(N*(N+3)/2):
		sh2.write(tmp2_row+i, tmp2_col+j, 0.0)

tmp2_row = 3
tmp2_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	sh2.write(tmp2_row, tmp2_col, index+1)
	sh2.write(tmp2_row, tmp2_col+1, tmp_mole.label)
	sh2.write(tmp2_row, tmp2_col+2, tmp_mole.ZPE)

	tmp_groupVector = tmp_mole.getGroupVector()
	for tmp_vectorEle in tmp_groupVector.keys():
		sh2.write(tmp2_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

	if not tmp_mole.existRings():
		sh3.write(tmp3_row, tmp3_col, index+1)
		sh3.write(tmp3_row, tmp3_col+1, tmp_mole.label)
		sh3.write(tmp3_row, tmp3_col+2, tmp_mole.ZPE)
		for j in xrange(N*(N+3)/2):
			sh3.write(tmp3_row, tmp3_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh3.write(tmp3_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
		tmp3_row += 1
	else:
		sh4.write(tmp4_row, tmp4_col, index+1)
		sh4.write(tmp4_row, tmp4_col+1, tmp_mole.label)
		sh4.write(tmp4_row, tmp4_col+2, tmp_mole.ZPE)
		for j in xrange(N*(N+3)/2):
			sh4.write(tmp4_row, tmp4_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh4.write(tmp4_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
		sh4.write(tmp4_row, tmp4_col+5+N*(N+3)/2, tmp_mole.getRingSize())
		tmp4_row += 1
	
	tmp2_row += 1

wb2.close()

vectorGroups = []
vectorMole = []
acyclicVecIndex = []
cyclicVecIndex = []

wb3 = xlsxwriter.Workbook('inputFile_m.xlsx')
sh5 = wb3.add_worksheet('inputVectors')
sh6 = wb3.add_worksheet('acyclic')
sh7 = wb3.add_worksheet('cyclic')

tmp5_row = 0
tmp5_col = 0
sh5.write(tmp5_row, tmp5_col, 'ID')
sh5.write(tmp5_row, tmp5_col+3, 'TotalDimesionNumber')
sh5.write(tmp5_row, tmp5_col+5, 'DimentionIndex')

tmp5_row = 1
sh5.write(tmp5_row, tmp5_col+3, N*(N+3)/2)

tmp5_col = 5
for i in xrange(N*(N+3)/2):
	sh5.write(tmp5_row, tmp5_col+i, i+1)

tmp5_row = 2 
for i in xrange(N):
	sh5.write(tmp5_row, tmp5_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp5_col
	tmp5_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh5.write(tmp5_row, tmp5_col, tmp_text)
		groupIndex[tmp_text] = tmp5_col
		tmp5_col += 1

sh5.write(tmp5_row, tmp5_col+2, 'Name')
sh5.write(tmp5_row, tmp5_col+3, 'ReferenceEnergy')

tmp6_row = 0
tmp6_col = 0
sh6.write(tmp6_row, tmp6_col, 'ID')
sh6.write(tmp6_row, tmp6_col+3, 'TotalDimesionNumber')
sh6.write(tmp6_row, tmp6_col+5, 'DimentionIndex')

tmp6_row = 1
sh6.write(tmp6_row, tmp6_col+3, N*(N+3)/2)

tmp6_col = 5
for i in xrange(N*(N+3)/2):
	sh6.write(tmp6_row, tmp6_col+i, i+1)

tmp6_row = 2 
for i in xrange(N):
	sh6.write(tmp6_row, tmp6_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp6_col
	tmp6_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh6.write(tmp6_row, tmp6_col, tmp_text)
		groupIndex[tmp_text] = tmp6_col
		tmp6_col += 1

sh6.write(tmp6_row, tmp6_col+2, 'Name')
sh6.write(tmp6_row, tmp6_col+3, 'ReferenceEnergy')

tmp7_row = 0
tmp7_col = 0
sh7.write(tmp7_row, tmp7_col, 'ID')
sh7.write(tmp7_row, tmp7_col+3, 'TotalDimesionNumber')
sh7.write(tmp7_row, tmp7_col+5, 'DimentionIndex')

tmp7_row = 1
sh7.write(tmp7_row, tmp7_col+3, N*(N+3)/2)

tmp7_col = 5
for i in xrange(N*(N+3)/2+1):
	sh7.write(tmp7_row, tmp7_col+i, i+1)

tmp7_row = 2 
for i in xrange(N):
	sh7.write(tmp7_row, tmp7_col, all_groups[i])
	groupIndex[all_groups[i]] = tmp7_col
	tmp7_col += 1	

for i in xrange(N):
	for j in xrange(i, N):
		tmp_list = sorted([all_groups[i], all_groups[j]])
		tmp_text = tmp_list[0] + '-' + tmp_list[1]
		sh7.write(tmp7_row, tmp7_col, tmp_text)
		groupIndex[tmp_text] = tmp7_col
		tmp7_col += 1
sh7.write(tmp7_row, tmp7_col, 'CycleSize')
sh7.write(tmp7_row, tmp7_col+2, 'Name')
sh7.write(tmp7_row, tmp7_col+3, 'ReferenceEnergy')

tmp5_row = 3
tmp5_col = 0
tmp6_row = 3
tmp6_col = 0
tmp7_row = 3
tmp7_col = 0
for (index, tmp_mole) in enumerate(all_moles):
	tmp_groupVector = {}

	tmp_groupVector = tmp_mole.getGroupVector()
	
	flag_exsit = 0
	for (i, tmp_vector) in enumerate(reversed(vectorGroups)):
		if set(tmp_groupVector.keys()) == set(tmp_vector.keys()):
			tmp_diff = np.array([tmp_groupVector[x]-tmp_vector[x] for x in tmp_groupVector.keys()])
			if max(abs(tmp_diff)) < 1e-12:			
				vectorMole[len(vectorGroups)-i-1][tmp_mole.label] = tmp_mole.ZPE
				flag_exsit = 1
	if flag_exsit == 0:
		vectorGroups.append(tmp_groupVector)
		vectorMole.append({})
		vectorMole[-1][tmp_mole.label] = tmp_mole.ZPE
		sh5.write(tmp5_row, tmp5_col, len(vectorGroups))
		for j in xrange(N*(N+3)/2):
				sh5.write(tmp5_row, tmp5_col+5+j, 0.0)
		for tmp_vectorEle in tmp_groupVector.keys():
			sh5.write(tmp5_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])

		if not tmp_mole.existRings():
			sh6.write(tmp6_row, tmp6_col, len(vectorGroups))
			for j in xrange(N*(N+3)/2):
				sh6.write(tmp6_row, tmp6_col+5+j, 0.0)
			for tmp_vectorEle in tmp_groupVector.keys():
				sh6.write(tmp6_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
			acyclicVecIndex.append(len(vectorGroups))
			tmp6_row += 1
		else:
			sh7.write(tmp7_row, tmp7_col, len(vectorGroups))
			for j in xrange(N*(N+3)/2):
				sh7.write(tmp7_row, tmp7_col+5+j, 0.0)
			for tmp_vectorEle in tmp_groupVector.keys():
				sh7.write(tmp7_row, groupIndex[tmp_vectorEle], tmp_groupVector[tmp_vectorEle])
			sh7.write(tmp7_row, tmp7_col+5+N*(N+3)/2, tmp_mole.getRingSize())
			cyclicVecIndex.append(len(vectorGroups))
			tmp7_row += 1
		
		tmp5_row += 1

tmp5_row = 3
tmp6_row = 3
tmp7_row = 3
for i in xrange(len(vectorGroups)):
	tmp5_col = N*(N+3)/2 + 7
	tmp6_col = N*(N+3)/2 + 7
	tmp7_col = N*(N+3)/2 + 7

	tmp_list = sorted(vectorMole[i].items(), key = lambda d: d[1])
	for tmp_item in tmp_list:
		sh5.write(tmp5_row, tmp5_col, tmp_item[0])
		sh5.write(tmp5_row, tmp5_col+1, tmp_item[1])
		tmp5_col += 2
	if (i+1) in acyclicVecIndex:
		for tmp_item in tmp_list:
			sh6.write(tmp6_row, tmp6_col, tmp_item[0])
			sh6.write(tmp6_row, tmp6_col+1, tmp_item[1])
			tmp6_col += 2
		tmp6_row += 1
	elif (i+1) in cyclicVecIndex:
		for tmp_item in tmp_list:
			sh7.write(tmp7_row, tmp7_col, tmp_item[0])
			sh7.write(tmp7_row, tmp7_col+1, tmp_item[1])
			tmp7_col += 2
		tmp7_row += 1
	else:
		print 'Error! The molecules are neither acyclic nor cyclic!', tmp_list

	tmp5_row += 1

wb3.close()

