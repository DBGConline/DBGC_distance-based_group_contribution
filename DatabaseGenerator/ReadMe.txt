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

The code in the directory DatabaseGenerator is used to generate the database for training, test and prediction. 

For training or test set construction, the code getGroupDataBaseFromLog.py and getGroupInput.py will use the 
Gaussian output files in directories "freq" and "energy". The file database.xlsx containing the quantum 
chemistry results and the file inputFile.xlsx (or inputFile_m.xlsx) containing the group contribution vector 
and the thermodynamic data will be generated. It should be noted that the code to assist this process is not 
necessary. The user can construct a database based on his own data source. To get the group contribution vectors, 
only getGroupDataBaseFromGjf.py is enough.

For practical prediction, the code getGroupDataBaseFromGjf.py will use the geometry files in the directory "Gjfs". 
The file DBGCVectors.xlsx in the directory DBGCVectors, which contains the group contribution vectors for the species 
to be predict, will be generated.

To implement the whole process, the .py files getGroupDataBaseFromLog.py, getGroupInput.py and 
getGroupDataBaseFromGjf.py can be used accordingly to speed up the calculation.

-----------------------------
getGroupDataBaseFromLog.py
-----------------------------
This file is used to generate enthalpy at 298.15 K (unit: hartree) database for group contribution method 
at the M062X/def2TZVP//B3LYP/6-31G(d) level of theory. The enthalpy at 298.15 K is calculated as the the 
scf energy of M062X/def2TZVP + ZPE correction of B3LYP/6-31G(d) + enthalpy difference from 0 K to 298.15 K 
at the B3LYP/6-31G(d) level of theory. The scaling factor used to calculate the ZPE correction is 0.977. 
(Ref: I.M. Alecu, J. Zheng, Y. Zhao, D.G. Truhlar, J. Chem. Theory Comput. 6 (2010) 2872-2887.) The scaling 
factor used to calculate the enthalpy difference is 1. Because it is usually very close to 1 at 295.15 K. 
(Ref: A. P. Scott, L. Radom, J. Phys. Chem, 100 (1996) 16502-16513.) Currently only HHRO approximation is 
used, because the huge cost of hindered rotation correction. 

The input files should be put in the directories freq and energy. The directory freq is used to store the 
.log files from the optimization and frequencies calculation at the B3LYP/6-31G(d) level of theory. The 
directory energy is used to store the .log files from single point energy calculation at the M062X/def2TZVP 
level of theory. The freq file and the energy file for the same species is recognized through the names. 
For example, the freq file for C6H14_1 is called C6H14_1_2_opt_B3L, and the energy file is named as 
C6H14_1_3_opt_M06. To change the naming rule, please modify the code in getGroupDataBaseFromLog.py. The 
related code is as below.
	energyFile = file(os.path.join('energy', tmp_name+'_3_opt_M06.log'),'r')
To change the level of theory used, please modify the code accordingly in getGroupDataBaseFromLog.py. The 
related code is as below.
	pattern_optEnergy = re.compile('^.*SCF Done:  E\([RU]B3LYP\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
	pattern_optZPE = re.compile('^.*Sum of electronic and zero-point Energies= *(-?[0-9]+\.[0-9]+).*$')
	pattern_optEnthalpy = re.compile('^.*Sum of electronic and thermal Enthalpies= *(-?[0-9]+\.[0-9]+).*$')
	pattern_D3Energy = re.compile('^.*Grimme-D3 Dispersion energy= *(-?[0-9]+\.[0-9]+) *Hartrees.*$')
	pattern_SPEnergy = re.compile('^.*SCF Done:  E\([RU]M062X\) = *([\-\.0-9Ee]+) +A\.U\. after.*$')
The scaling factor in getGroupDataBaseFromLog.py should be also updated.
The standard enthalpy of formation of C(g) in thermoDatabase.py should be also updated with the new level 
of theory used.

The output file is database.xlsx, in which the name, formula, SCF energy, ZPE correction, enthalpy 
difference, and geometry is recorded. The enthalpy at 298.15 K and the M062X/def2TZVP//B3LYP/6-31G(d) 
level of theory is also calculated and recorded in the excel. Then this excel can be used to produce the 
standard enthalpy of formation and group contribution vector.

-----------------------------
getGroupInput.py
-----------------------------
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
bringing an effect of error cancellation. More details about the 89 species and the calculation of standard 
enthalpy of formation can be found in the supplementary .docx file.

The input file is database.xlsx. It can be generated with getGroupDataBaseFromLog.py, or be obtained based on 
one's own data source. 

The output file is inputFile.xlsx and inputFile_m.xlsx. In the inputFile.xlsx, the data is arraged with the 
order of names of species in the database. In the inputFile_m.xlsx, the species with the same group contribution 
vectors are combined into the same row. Therefore, all the conformers through internal rotation will be listed 
in the same row and ranked in the order of energy in inputFile_m.xlsx. This is an adavantage for picking out the 
lowest-energy conformer. It should be acknowledged that in current stage the cis-tran isomers has the same grouop 
contribution vector, and can't be distinguished. In most of the situations, the tran structure for alkene has a 
lower energy than cis structure, thus ranking before the cis stucture.


-----------------------------
getGroupDataBaseFromGjf.py
-----------------------------
This file is used to generate the group contribution veoctors for the species to be predicted.

By default the input file is stored in the directiry Gjfs. The input format is the Gaussian input 
format, namely, .gjf. Here is an example.

	-----------------example below--------------------------------
	# hf/3-21g 

	Title Card Required

	0 1
	 C                 -0.68027212   -0.34013605    0.00000000
	 H                 -0.32361770   -1.34894605    0.00000000
	 H                 -0.32359928    0.16426214   -0.87365150
	 H                 -1.75027212   -0.34012287    0.00000000
	 C                 -0.16692990    0.38582022    1.25740497
	 H                 -0.52198625    1.39519331    1.25642745
	 H                 -0.52519901   -0.11744821    2.13105486
	 C                  1.37306749    0.38336387    1.25881364
	 H                  1.73133598    0.88630575    0.38497547
	 H                  1.72974052    0.88808796    2.13227684
	 H                  1.72812373   -0.62600882    1.26016738



	 ------------------example above-------------------------------
The first line is the command line for Gaussian calculation, so it doesn't matter. The information 
needed to generate group contribution vector is the coordinates.

The output file is DBGCVectors.xlsx and DBGCVectors_noTemplate.xlsx in the directory DBGCVectors, which 
contains the group contribution vectors. In a system with finite groups, the dimension of the group 
contribution vector is a constant. A template file is used when the number of species is too small to 
cover all the groups. Currently, the template file used is groupTemplate.xlsx, containing all the groups 
in alkane, alkene (only one C=C double bond is considered), alkyl radical, and alkenyl radical system. If 
the types of groups are not determined, DBGCVectors_noTemplate.xlsx are used to record all the groups and 
group-group interactions in the new system, which consists of the .gjf files in the directory Gjfs.



