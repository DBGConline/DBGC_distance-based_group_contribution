# this is a class of MomInert 
# it can be used for file format transformation and MomInert running
import re
import os
import shutil
import textExtractor
import chem

# definetion of comparing pattern
pattern_multi = re.compile('^.*spinMultiplicity: *([0-9]+).*$')
pattern_atom = re.compile('^.*[A-Z] *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+) *(-?[0-9]+\.[0-9]+).*$')
pattern_rotation = re.compile('^ *([0-9]+) +([0-9]+) +([0-9]+) +([0-9]+).*$')
pattern_fixBond = re.compile('^ *([0-9]+) ([0-9]+).*$')

pattern_gjfCommand = re.compile('^.*#p?.*$')
pattern_gjfMulti = re.compile('^.*([0-9]+) +([0-9]+).*$')
pattern_blankLine = re.compile('^ *$')

pattern_logMulti = re.compile('^.*Multiplicity = ([0-9]+).*$')
pattern_logFreqCom = re.compile('^.*#[PN]? Geom=AllCheck Guess=TCheck SCRF=Check.*Freq.*$')
pattern_logStandard = re.compile('^.*Standard orientation:.*$') 
pattern_logInput = re.compile('^.*Input orientation:.*$') 
pattern_logEndline = re.compile('^.*---------------------------------------------------------------------.*$')


class cluster:
	name = ''
	jobLocation = ''
	JmolPath = ''

	_g09D01 = False
	_dispersionD3 = False
	_scratchStrategy = False
	_TS = False

	def __init__(self, name, clusterPath):
		self.name = name
		self.jobLocation = clusterPath
		self.JmolPath = ''

		self._g09D01 = False
		self._dispersionD3 = False
		self._scratchStrategy = False
		self._TS = False

	def setJobLocation(self, clusterPath):
		self.jobLocation = clusterPath

	def setJmolPath(self, JmolProgPath):
		self.JmolPath = JmolProgPath

	def setG09D01(self, useG09D01):
		self._g09D01 = useG09D01

	def setDispersionD3(self, useDispersionD3):
		self._dispersionD3 = useDispersionD3

	def setScratchStractegy(self, useScratchStrategy):
		self._scratchStrategy = useScratchStrategy		

	def setTS(self, isTS):
		self._TS = isTS		

	def generateJobFromGjf(self, fileName, path='', jobName='', method='', freq=True, command=''):
		QMmethod = 'B3LYP/6-31G(d)'

		gjfCommand_done = -1
		gjfMulti_done = -1
		geomDone = -1

		lineStart = 0
		lineEnd = 0

		if method != '':
			QMmethod = method

		if jobName == '':
			tmp_dir = fileName[0:-4] + '_1_opt_' + QMmethod[0:3]
		else:
			tmp_dir = jobName
		if path == '':			
			tmp_dir_path = tmp_dir
			fr = file(fileName, 'r')
		else:
			tmp_dir_path = os.path.join(path, tmp_dir)
			fr = file(os.path.join(path, fileName), 'r')

		tmp_lines = fr.readlines()
		for (lineNum, tmp_line) in  enumerate(tmp_lines):
			if gjfCommand_done != 1:
				tmp_m = pattern_gjfCommand.match(tmp_line)
				if tmp_m:
					gjfCommand_done = 1
			elif gjfMulti_done != 1:
				tmp_m = pattern_gjfMulti.match(tmp_line)
				if tmp_m:
					lineStart = lineNum
					multi = int(tmp_m.group(2))
					geomDone = 0
					gjfMulti_done = 1
			elif geomDone != 1:
				tmp_m = pattern_blankLine.match(tmp_line)
				if tmp_m:
					lineEnd = lineNum
					geomDone = 1

		if os.path.exists(tmp_dir):
			shutil.rmtree(tmp_dir)
		os.mkdir(tmp_dir)					

		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
		fw.write(
'''%mem=15GB
%nprocshared=6
''')
		if command == '':
			fw.write('#p ')
			if multi != 1:
				fw.write('u')
			fw.write(QMmethod)
			if self._TS == False:
				fw.write(' opt ')
				if freq == True:
					fw.write('freq')
			else:
				fw.write(' opt=(TS, calcfc) freq')
			if self._dispersionD3 == False:
				fw.write('\n')
			else:
				fw.write(' EmpiricalDispersion=GD3\n')
		else:
			fw.write(command+'\n')
		fw.write('''
using ''' + QMmethod + ''' to do opt and freq calc.

''')
		fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')
		
		fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
		
		fw.write(
'''#!/bin/bash

cd ''' + self.jobLocation + '/' + tmp_dir + '''
g09 ''' + tmp_dir + '''.gjf 


''')				
		fw.close()
		os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

	# this function is used to convert gjf to sdf format for conformer searching
	# the parameter path should be left as ''
	# the supporting for other directory is not important currently
	# if needed, only the path in jmol script should be adjusted according to the parameter path 
	# the parameter is used only when one gjf file is processed 
	def genFrogInputFromGjf(self, fileList, path='', jobName=''):
		for tmp_file in fileList:
			gjfCommand_done = -1
			gjfMulti_done = -1
			geomDone = -1

			lineStart = 0
			lineEnd = 0

			if re.search('[Tt][sS]', tmp_file):
				self.setTS(True)
			else:
				self.setTS(False)

			if jobName == '':
				tmp_dir = tmp_file[0:-4] + '_1_confSearch'
			else:
				tmp_dir = jobName
			if path == '':			
				tmp_dir_path = tmp_dir
				fr = file(tmp_file, 'r')
			else:
				tmp_dir_path = os.path.join(path, tmp_dir)
				fr = file(os.path.join(path, tmp_file), 'r')

			tmp_lines = fr.readlines()
			for (lineNum, tmp_line) in  enumerate(tmp_lines):
				if gjfCommand_done != 1:
					tmp_m = pattern_gjfCommand.match(tmp_line)
					if tmp_m:
						gjfCommand_done = 1
				elif gjfMulti_done != 1:
					tmp_m = pattern_gjfMulti.match(tmp_line)
					if tmp_m:
						lineStart = lineNum
						multi = int(tmp_m.group(2))
						geomDone = 0
						gjfMulti_done = 1
				elif geomDone != 1:
					tmp_m = pattern_blankLine.match(tmp_line)
					if tmp_m:
						lineEnd = lineNum
						geomDone = 1

			if os.path.exists(tmp_dir):
				shutil.rmtree(tmp_dir)
			os.mkdir(tmp_dir)					

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
			fw.write(
'''%mem=28GB
%nprocshared=12
''')
			if self._TS == False:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt freq')
			else:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt=(TS, calcfc) freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt=(TS, calcfc) freq')				
			if self._dispersionD3 == False:
				fw.write('\n')
			else:
				fw.write(' EmpiricalDispersion=GD3\n')
			fw.write('''
using ub3lyp/6-31G(d) to scan

''')
			fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.xyz'), 'w')
			fw.write(str(lineEnd - lineStart - 1) + '\n')
			fw.write(tmp_file[0:-4] + '\n')
			fw.write(''.join(tmp_lines[lineStart+1: lineEnd]) + '\n\n\n\n\n')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			os.system('E:\\softwares\\OpenBabel-2.3.72\\babel.exe -ixyz ' + os.path.join(tmp_dir_path, tmp_dir+'.xyz') + ' -osdf ' + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')
			
			openBabelWrong = False
			tmp_molecule = chem.molecule(geom=tmp_lines[lineStart+1: lineEnd])
			tmp_molecule.fulfillBonds()			
			if os.path.exists(os.path.join(tmp_dir_path, tmp_dir+'.sdf')):
				fr = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'r')
				tmp2_lines = fr.readlines()
				fr.close()
				tmp_num = map(int, tmp2_lines[3].split()[0:2])
				if tmp_num[1] < len(tmp_molecule.bonds):
					openBabelWrong = True
				elif tmp_num[1] > len(tmp_molecule.bonds):
					print 'Error! Open babel bond number > len(tmp_molecule.bonds)', tmp_dir	
			else:
				openBabelWrong = True

			if openBabelWrong:
				print 'Warning! Open babel transformation bug! Chem used to regenerate the bonds!', tmp_dir
				tmp_molecule.generateSDFFile(directory=tmp_dir_path, fileName=tmp_dir+'.sdf', moleculeLabel=tmp_file[0:-4])
 				# fw = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'w')
# 				tmp2_lines[3] = ''.join([' ', '%2d'%tmp_num[0], ' ', '%2d'%(len(tmp_molecule.bonds)), tmp2_lines[3][6:]])
# 				fw.writelines(tmp2_lines[0:3+tmp_num[0]+1]) 
# 				for tmp_bond in tmp_molecule.bonds:
# 					fw.write(''.join([' ', '%2d'%tmp_bond.atom1.label, ' ', '%2d'%tmp_bond.atom2.label, ' ', '%2d'%tmp_bond.bondOrder, '  0  0  0  0\n']))
# 				fw.write(
# '''M  END
# $$$$

# ''')
# 				fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
			fw.write(
# cce cluster
'''#!/bin/sh

cd ''' + self.jobLocation + '/' + tmp_dir + '''
python /home/apps/Frog2/www_iMolecule.py -osmi ''' + tmp_dir + '''.smiles -logFile ''' + tmp_dir + '''.log -ounsolved Unsolved.data -wrkPath . -eini 100.0 -mcsteps 100 -emax 50 -i3Dsdf ''' + tmp_dir + '''.sdf -osdf out_''' + tmp_dir + '''.sdf -unambiguate -mini -multi 250 &>> log_''' + tmp_dir + '''.txt


''')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

	# this function is used to convert gjf to sdf format for conformer searching
	# the parameter path should be left as ''
	# the supporting for other directory is not important currently
	# if needed, only the path in jmol script should be adjusted according to the parameter path 
	# the parameter is used only when one gjf file is processed 
	def genBalloonInputFromGjf(self, fileList, path='', jobName=''):
		for tmp_file in fileList:
			gjfCommand_done = -1
			gjfMulti_done = -1
			geomDone = -1

			lineStart = 0
			lineEnd = 0

			if re.search('[Tt][sS]', tmp_file):
				self.setTS(True)
			else:
				self.setTS(False)

			if jobName == '':
				tmp_dir = tmp_file[0:-4] + '_1_confSearch'
			else:
				tmp_dir = jobName
			if path == '':			
				tmp_dir_path = tmp_dir
				fr = file(tmp_file, 'r')
			else:
				tmp_dir_path = os.path.join(path, tmp_dir)
				fr = file(os.path.join(path, tmp_file), 'r')

			tmp_lines = fr.readlines()
			for (lineNum, tmp_line) in  enumerate(tmp_lines):
				if gjfCommand_done != 1:
					tmp_m = pattern_gjfCommand.match(tmp_line)
					if tmp_m:
						gjfCommand_done = 1
				elif gjfMulti_done != 1:
					tmp_m = pattern_gjfMulti.match(tmp_line)
					if tmp_m:
						lineStart = lineNum
						multi = int(tmp_m.group(2))
						geomDone = 0
						gjfMulti_done = 1
				elif geomDone != 1:
					tmp_m = pattern_blankLine.match(tmp_line)
					if tmp_m:
						lineEnd = lineNum
						geomDone = 1

			if os.path.exists(tmp_dir):
				shutil.rmtree(tmp_dir)
			os.mkdir(tmp_dir)					

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.gjf'), 'w')
			fw.write(
'''%mem=28GB
%nprocshared=12
''')
			if self._TS == False:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt freq')
			else:
				if multi != 1:
					fw.write('#p ub3lyp/cbsb7 opt=(TS, calcfc) freq')
				else:
					fw.write('#p b3lyp/cbsb7 opt=(TS, calcfc) freq')				
			if self._dispersionD3 == False:
				fw.write('\n')
			else:
				fw.write(' EmpiricalDispersion=GD3\n')
			fw.write('''
using ub3lyp/6-31G(d) to scan

''')
			fw.write(''.join(tmp_lines[lineStart: lineEnd]) + '\n\n\n\n\n')

			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.xyz'), 'w')
			fw.write(str(lineEnd - lineStart - 1) + '\n')
			fw.write(tmp_file[0:-4] + '\n')
			fw.write(''.join(tmp_lines[lineStart+1: lineEnd]) + '\n\n\n\n\n')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')

			os.system('E:\\softwares\\OpenBabel-2.3.72\\babel.exe -ixyz ' + os.path.join(tmp_dir_path, tmp_dir+'.xyz') + ' -osdf ' + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')
			
			fr = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'r')
			tmp2_lines = fr.readlines()
			fr.close()
			tmp_num = map(int, tmp2_lines[3].split()[0:2])
			tmp_molecule = chem.molecule(geom=tmp_lines[lineStart+1: lineEnd])
			tmp_molecule.fulfillBonds()
			if tmp_num[1] < len(tmp_molecule.bonds):
				print 'Warning! Open babel transformation bug! Chem used to regenerate the bonds!', tmp_dir
				fw = file(os.path.join(tmp_dir_path, tmp_dir+'.sdf'), 'w')
				tmp2_lines[3] = ''.join([' ', '%2d'%tmp_num[0], ' ', '%2d'%(len(tmp_molecule.bonds)), tmp2_lines[3][6:]])
				fw.writelines(tmp2_lines[0:3+tmp_num[0]+1]) 
				for tmp_bond in tmp_molecule.bonds:
					fw.write(''.join([' ', '%2d'%tmp_bond.atom1.label, ' ', '%2d'%tmp_bond.atom2.label, ' ', '%2d'%tmp_bond.bondOrder, '  0  0  0  0\n']))
				fw.write(
'''M  END
$$$$

''')
				fw.close()
			elif tmp_num[1] > len(tmp_molecule.bonds):
				print 'Error! Open babel bond number > len(tmp_molecule.bonds)', tmp_dir
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + os.path.join(tmp_dir_path, tmp_dir+'.sdf') + ' > log_dos2unix.txt 2>&1')

			fw = file(os.path.join(tmp_dir_path, tmp_dir+'.job'), 'w')
			fw.write(
# linux bash
'''#!/bin/sh

cd ''' + self.jobLocation + '/' + tmp_dir + '''
/home/apps/balloon/balloon -f /home/hetanjin/apps/balloon/MMFF94.mff --nconfs 300 --stereo --addConformerNumberToName ''' + tmp_dir + '''.sdf out_''' + tmp_dir + '''.sdf &>> log_''' + tmp_dir + '''.txt


''')
			fw.close()
			os.system("..\\dos2unix-6.0.6-win64\\bin\\dos2unix.exe " + fw.name + ' > log_dos2unix.txt 2>&1')


