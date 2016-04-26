# this is a class of physics
# this could be used to get physical constants 
# also used for unit conversion
# m represent '-'
# p represent '+'
import os
import chem
import re

class Frog:
	# public constants
	pattern_mol2Energy = re.compile('^.*VDW energy = ([\.\-0-9]+).*$')
	pattern_mol2AtomStart = re.compile('^.*@<TRIPOS>ATOM.*$')
	pattern_mol2Atom = re.compile('^ *[0-9]+ +([a-zA-Z]+)[0-9]+ +([\-\.0-9]+) +([\-\.0-9]+) +([\-\.0-9]+).*$')

	def __init__(self):
		pass

	def readConformers(self, fileName, path=''):
		# varibles
		molecules = []

		# flags
		energy_done = 0
		atomStart_done = 0

		# temporary variables
		tmp_energy = 0.0
		tmp_geom = []
		tmp_coordinate = ''
		atomStartLine = 0

		fr = file(os.path.join(path, fileName), 'r')
		tmp_lines = fr.readlines()
		for (index, tmp_line) in enumerate(tmp_lines):
			if energy_done != 1:
				tmp_m = Frog.pattern_mol2Energy.match(tmp_line)
				if tmp_m:
					tmp_energy = float(tmp_m.group(1))
					energy_done = 1
			elif atomStart_done != 1:
				tmp_m = Frog.pattern_mol2AtomStart.match(tmp_line)
				if tmp_m:
					atomStartLine = index + 1
					atomStart_done = 1
			else:
				tmp_m = Frog.pattern_mol2Atom.match(tmp_line)
				if tmp_m:
					tmp_coordinate = ''.join([tmp_m.group(1), '    ', tmp_m.group(2), '    ', tmp_m.group(3), '    ', tmp_m.group(4)])
					tmp_geom.append(tmp_coordinate)
				else:
					tmp_molecule = chem.molecule()
					tmp_molecule.getGjfGeom(tmp_geom)
					tmp_molecule.setZPE(tmp_energy)
					molecules.append(tmp_molecule)					
					energy_done = 0
					atomStart_done = 0

					tmp_energy = 0.0
					tmp_geom = []
					tmp_coordinate = ''
					atomStartLine = 0
					
		fr.close()
		return molecules	


