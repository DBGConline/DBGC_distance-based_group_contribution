# This is a database for bath gas and usual molecules
# it should be write to a .xml file in the future if the database is much larger
import chem
import phys
import re

# constants
phys1 = phys.phys()

moleBase = {}

tmp_mole = chem.molecule()
tmp_mole.setLabel('C')
tmp_mole.setDescription('gas-phase Carbon atom, charge: 0, multiplicity: 3')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
# NIST DATA
# tmp_mole.setFormationH(171.2882409)
# Tanjin's CBS-QB3 empirical HO averaged data based on 89 alkanes, alkenes, cycloalkanes and oxygenated hydrocarbons, standard deviation 0.119052083
# tmp_mole.setFormationH(169.7035843)
# Tanjin's CBS-QB3 empirical HR averaged data based on 89 alkanes, alkenes, cycloalkanes and oxygenated hydrocarbons, standard deviation 0.134300929
# tmp_mole.setFormationH(169.5852139)
# Tanjin's M062X/def2TZVP//B3LYP/6-31G(d) empirical HO averaged data based on 89 alkanes, alkenes, cycloalkanes and oxygenated hydrocarbons, standard deviation 0.156821832
tmp_mole.setFormationH(172.0396822)
# Tanjin's M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d) empirical HO averaged data based on 89 alkanes, alkenes, cycloalkanes and oxygenated hydrocarbons, standard deviation 0.157905381
# tmp_mole.setFormationH(172.0489917)
# Tanjin's M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d) empirical HO averaged data based on 89 alkanes, alkenes, cycloalkanes and oxygenated hydrocarbons, standard deviation 0.157319398
# tmp_mole.setFormationH(172.0982219)
# Tanjin's B3LYP/6-31G(d) empirical HO averaged data based on 82 alkanes, alkenes, cycloalkanes, standard deviation 0.347106593
# tmp_mole.setFormationH(169.6972837)

# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -37.785377, 'B3LYP/6-31G(d)': -37.84628001, 'M062X/def2TZVP': -37.842511, 'M062X/def2TZVP//B3LYP/6-31G(d)': -37.84251051, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -37.842510898, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -37.842510898})
tmp_mole.setRefH298({'CBS-QB3': -37.783017, 'B3LYP/6-31G(d)': -37.84392001, 'M062X/def2TZVP': -37.840150, 'M062X/def2TZVP//B3LYP/6-31G(d)': -37.84015051, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -37.840150898, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -37.840150898})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('H2')
tmp_mole.setDescription('gas-phase H2, charge: 0, multiplicity: 1')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
tmp_mole.setFormationH(0)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -1.166083, 'B3LYP/6-31G(d)': -1.165570344, 'M062X/def2TZVP': -1.158161, 'M062X/def2TZVP//B3LYP/6-31G(d)': -1.158438045, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -1.158214884, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -1.158214884})
tmp_mole.setRefH298({'CBS-QB3': -1.162778, 'B3LYP/6-31G(d)': -1.162266344, 'M062X/def2TZVP': -1.154857, 'M062X/def2TZVP//B3LYP/6-31G(d)': -1.155134045, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -1.155143989, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -1.155143989})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('O2')
tmp_mole.setDescription('gas-phase O2, charge: 0, multiplicity: 3')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol
tmp_mole.setFormationH(0)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'CBS-QB3': -150.164604, 'B3LYP/6-31G(d)': -150.3163499, 'M062X/def2TZVP': -150.323158, 'M062X/def2TZVP//B3LYP/6-31G(d)': -150.3223863, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -150.322304033, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -150.322304033})
tmp_mole.setRefH298({'CBS-QB3': -150.161296, 'B3LYP/6-31G(d)': -150.3130429, 'M062X/def2TZVP': -150.319852, 'M062X/def2TZVP//B3LYP/6-31G(d)': -150.3190793, 'M062X/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -150.319083950, 'M062X-GD3/def2TZVP//B3LYP-GD3BJ/6-31G(d)': -150.319083950})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('H')
tmp_mole.setDescription('gas-phase H, charge: 0, multiplicity: 2')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol, from Cramer's Essential of Computational Chemistry, p369
tmp_mole.setFormationH(52.103)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'B3LYP/6-31G(d)': -0.500272995, 'M062X/def2TZVP//B3LYP/6-31G(d)': -0.498138695})
tmp_mole.setRefH298({'B3LYP/6-31G(d)': -0.497911995, 'M062X/def2TZVP//B3LYP/6-31G(d)': -0.495777695})
moleBase[tmp_mole.label] = tmp_mole

tmp_mole = chem.molecule()
tmp_mole.setLabel('O')
tmp_mole.setDescription('gas-phase O, charge: 0, multiplicity: 3')
# standard enthalpy of formation in 298.15 K, 1 atm, unit is kcal/mol, from Cramer's Essential of Computational Chemistry, p369
tmp_mole.setFormationH(59.553)
# computational reference energies at 0 K using ab initio, unit is a.u.
tmp_mole.setRefH0({'B3LYP/6-31G(d)': -75.060623, 'M062X/def2TZVP//B3LYP/6-31G(d)': -75.0661519})
tmp_mole.setRefH298({'B3LYP/6-31G(d)': -75.058263, 'M062X/def2TZVP//B3LYP/6-31G(d)': -75.0637919})
moleBase[tmp_mole.label] = tmp_mole


def useThermoData(species):
	if species not in moleBase.keys():
		print 'Error! The species to be used is not in the thermodynamic database!', species
		return None
	else:
		return moleBase[species]

# unit: refEnthalpy0: a.u.
#		H298mH0: cal/mol
#		formationH: kcal/mol
# assume the formula is CxHyOz
# return the standard enthalpy of formation at 298.15 K 
def getFormationH(formula, refQMMethod, refEnthalpy0, H298mH0):
	pattern_element = re.compile('([A-Z][a-z]?)([0-9]*)')
	x = 0
	y = 0
	z = 0

	allElements = pattern_element.findall(formula)
	for tmp_element in allElements:
		if tmp_element[0] == 'C':
			if tmp_element[1] != '':
				x = int(tmp_element[1])
			else:
				x = 1
		elif tmp_element[0] == 'H':
			if tmp_element[1] != '':
				y = int(tmp_element[1])
			else:
				y = 1
		elif tmp_element[0] == 'O':
			if tmp_element[1] != '':
				z = int(tmp_element[1])
			else:
				z = 1
		else:
			print 'Error! The elements are more than C H and O!'
	if x+y+z==0:
		print 'Error! x+y+z can not be 0!'
	formationH = phys1.hartreeTokcalmol(refEnthalpy0 - x*moleBase['C'].refH298[refQMMethod] - y/2.0*moleBase['H2'].refH298[refQMMethod] - z/2.0*moleBase['O2'].refH298[refQMMethod]) + H298mH0/1000.0 + x*moleBase['C'].formationH 
	return formationH

# unit: NIST data: [cal][mol][k]
#		formationH298: kcal/mol
# assume the formula is CxHyOz
def NSSAH298Correction(NASACoeff, formationH298):
	NASA_lines = NASACoeff.split('\n')
	tmp_num = float(NASA_lines[2][0:15]) + formationH298*1000.0/phys1.JoulTocal(phys1.R)
	tmp_num = '%.7e' % tmp_num
	tmp_num = ' '*(15-len(tmp_num)) + tmp_num
	NASA_lines[2] = tmp_num + NASA_lines[2][15:]

	tmp_num = float(NASA_lines[3][30:45]) + formationH298*1000.0/phys1.JoulTocal(phys1.R)
	tmp_num = '%.7e' % tmp_num
	tmp_num = ' '*(15-len(tmp_num)) + tmp_num

	NASA_lines[3] = ''.join([NASA_lines[3][0:30], tmp_num, NASA_lines[3][45:60], ' '*15, NASA_lines[3][75:]]) 
	NASACoeff = '\n'.join(NASA_lines)
	return NASACoeff

# unit: refEnthalpy0: a.u.
#		H298mH0: cal/mol
#		HDifference: kcal/mol
# assume the formula is CxHyOz
# return the difference enthalpy of formation at 298.15 K
# this is used to evaluate the performance of different ab initio methods 
def getEnthalpyDifference(formula, refQMMethod, refEnthalpy0, H298mH0):
	pattern_element = re.compile('([A-Z][a-z]?)([0-9]*)')
	x = 0
	y = 0
	z = 0

	allElements = pattern_element.findall(formula)
	for tmp_element in allElements:
		if tmp_element[0] == 'C':
			if tmp_element[1] != '':
				x = int(tmp_element[1])
			else:
				x = 1
		elif tmp_element[0] == 'H':
			if tmp_element[1] != '':
				y = int(tmp_element[1])
			else:
				y = 1
		elif tmp_element[0] == 'O':
			if tmp_element[1] != '':
				z = int(tmp_element[1])
			else:
				z = 1
		else:
			print 'Error! The elements are more than C H and O!'
	if x+y+z==0:
		print 'Error! x+y+z can not be 0!'
	HDifference = phys1.hartreeTokcalmol(refEnthalpy0 - x*moleBase['C'].refH298[refQMMethod] - y/2.0*moleBase['H2'].refH298[refQMMethod] - z/2.0*moleBase['O2'].refH298[refQMMethod]) + H298mH0/1000.0 
	return HDifference

# unit: refEnergy0: a.u.
#		atomizationEnergy: kcal/mol
# assume the formula is CxHyOz
# return the atomizationEnergy at 0 K with ZPE correction
# this is used to evaluate the performance of different ab initio methods 
def getAtomizationEnergy(formula, refQMMethod, refEnergy0):
	pattern_element = re.compile('([A-Z][a-z]?)([0-9]*)')
	x = 0
	y = 0
	z = 0

	allElements = pattern_element.findall(formula)
	for tmp_element in allElements:
		if tmp_element[0] == 'C':
			if tmp_element[1] != '':
				x = int(tmp_element[1])
			else:
				x = 1
		elif tmp_element[0] == 'H':
			if tmp_element[1] != '':
				y = int(tmp_element[1])
			else:
				y = 1
		elif tmp_element[0] == 'O':
			if tmp_element[1] != '':
				z = int(tmp_element[1])
			else:
				z = 1
		else:
			print 'Error! The elements are more than C H and O!'
	if x+y+z==0:
		print 'Error! x+y+z can not be 0!'
	atomizationEnergy = phys1.hartreeTokcalmol(x*moleBase['C'].refH0[refQMMethod] + y*moleBase['H'].refH0[refQMMethod] + z*moleBase['O'].refH0[refQMMethod] - refEnergy0) 
	return atomizationEnergy

