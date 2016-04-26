# this is a class of physics
# this could be used to get physical constants 
# also used for unit conversion
# m represent '-'
# p represent '+'
import os
import chem
import re

class Balloon:
	# public constants
	pattern_sdfEnergyStart = re.compile('.*>  <energy>.*')
	pattern_sdfEnergy = re.compile('^.*([\.\-0-9]+).*$')
	pattern_sdfAtomStart = re.compile('^.*0999 V2000.*$')
	pattern_sdfAtom = re.compile('^ *([\-\.0-9]+) +([\-\.0-9]+) +([\-\.0-9]+) +([a-zA-Z]+).*$')

	def __init__(self):
		pass

	def readConformers(self, fileName, path=''):
		# varibles
		molecules = []

		# flags
		energyStart_done = 0
		energy_done = 0
		atomStart_done = 0
		coordinate_done = 0

		# temporary variables
		tmp_energy = 0.0
		tmp_geom = []
		tmp_coordinate = ''
		atomStartLine = 0

		fr = file(os.path.join(path, fileName), 'r')
		tmp_lines = fr.readlines()
		for (index, tmp_line) in enumerate(tmp_lines):
			if atomStart_done != 1:
				tmp_m = Balloon.pattern_sdfAtomStart.match(tmp_line)
				if tmp_m:
					atomStartLine = index + 1
					atomStart_done = 1
			elif coordinate_done != 1:
				tmp_m = Balloon.pattern_sdfAtom.match(tmp_line)
				if tmp_m:
					tmp_coordinate = ''.join([tmp_m.group(4), '    ', tmp_m.group(1), '    ', tmp_m.group(2), '    ', tmp_m.group(3)])
					tmp_geom.append(tmp_coordinate)
				else:
					coordinate_done = 1
			elif energyStart_done != 1:
				tmp_m = Balloon.pattern_sdfEnergyStart.match(tmp_line)
				if tmp_m: 
					energyStart_done = 1
			elif energy_done != 1:
				tmp_m = Balloon.pattern_sdfEnergy.match(tmp_line)
				if tmp_m:
					tmp_energy = float(tmp_m.group(1))
					tmp_molecule = chem.molecule()
					tmp_molecule.getGjfGeom(tmp_geom)
					tmp_molecule.setZPE(tmp_energy)
					molecules.append(tmp_molecule)					
					atomStart_done = 0
					coordinate_done = 0
					energyStart_done = 0
					tmp_energy = 0.0
					tmp_geom = []
					tmp_coordinate = ''
					
		fr.close()
		return molecules	


