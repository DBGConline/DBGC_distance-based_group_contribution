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

The code in the directory QMCalculation is used to assist quantum chemistry calculation. If a user has his own 
script to help with quantum chemistry calculation, this package is not necessary.

The working flow of the code in this package is as follows.  
1.	Pre-optimize the initial molecular structure with PM6; 
2.	Find the first 50 (or other number) lowest-energy conformers with MMFF;
3.	Re-optimize the 50 (or other number) conformers with PM6, and find the first 10 (or other number) 
lowest-energy conformers;
4.	Re-optimize the 10 conformers with B3LYP/6-31G(d), and find the lowest-energy conformer; 
5.	Analyze vibrational frequencies with B3LYP/6-31G(d);
6.	Compute single-point energy with M06-2X/def2-TZVP;
 
To implement this whole process, the .py files _a_PM6FromInitialGjf.py, _b_gjfFromLog.py, 
_c_confSearchFromGjf.py, _d_PM6FromConfSearch.py, _e_B3YPFromPM6.py, _f_lowestEnergyFromB3LYP.py,
_g_SPEnergyFromOpt.py, _h_radicalFromOpt.py,_i_radicalSPEnergyFromOpt.py can be used accordingly to 
speed up the calculation.

-----------------------------
_a_PM6FromInitialGjf.py
-----------------------------
This file is used to generate scripts for PM6 calculation based on the initial geometry structure.

The input files should be put in the directory _a_initialGeomGjf. The input format is the 
Gaussian input format, namely, .gjf.
The ouput files will appear in the directory _b_PM6PreOptimization, every sub-directory 
named like CnH2n+2_#_1_opt_PM6 in _b_PM6PreOptimization is an independent computational case. 
The .job file in the directory CnH2n+2_#_1_opt_PM6 is used to control the behavior of the cluster/PC, 
the .gjf file is the input for the Gaussian program. To control the details of the output scripts, please 
modify the code in the method generateJobFromGjf() in cluter.py file.

-----------------------------
_b_gjfFromLog.py
-----------------------------
This file is used to extract the optimized geomentry at PM6 level of theory from the .log file. 

The input files is the completed case in the directory _b_initialGeomGjf. This .py file will read 
the .log files in the sub-directories in _b_initialGeomGjf and extract the optimized geometry. The
.log file is the output of Gaussian compuation. By default the standard orientation in the .log 
file will be used, if the key word like nosym used, the code tmp_m = pattern_standard.match(tmp_line) 
should be replaced with tmp_m = pattern_input.match(tmp_line).
The ouput files will appear in the directory _c_confSearch. They are the optimized geometry 
coordinates in .gjf format.

-----------------------------
_c_confSearchFromGjf.py
-----------------------------
This file is used to generate scripts for MMFF conformational analysis with the Frog2 code, 
based on the initially optimized structure. 

The input files are the .gjf files in the directory _c_confSearch. The .gjf files contains the 
initially optimized structures.
The ouput files will appear in the directory _c_confSearch_Frog. Every sub-directory named like 
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
Ref: N M O'Boyle, M Banck, C A James, C Morley, T Vandermeersch, and G R Hutchison. "Open Babel: 
An open chemical toolbox." J. Cheminf. (2011), 3, 33. DOI:10.1186/1758-2946-3-33
The Open Babel Package, version 2.3.1 http://openbabel.org

-----------------------------
_d_PM6FromConfSearch.py
-----------------------------
This file is used to generate scripts for PM6 optimization based on the conformational analysis with 
MMFF. The conformers with low energies can be found in the energy ranking of MMFF analysis. Then the 
geometry structures will be extracted and used for PM6 optimization.

The input files are the _minimized.mol2 files in the directory _c_confSearch_Frog. The _minimized.mol2 
files contains the energy ranking of conformers based on MMFF calculation. 
The ouput files will appear in the directory _d_conformerPM6Gjfs. Every sub-directory named like 
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

-----------------------------
_e_B3YPFromPM6.py
-----------------------------
This file is used to generate scripts for B3LYP optimization based on the optimized with PM6. The 
geometry structures optimized with PM6 with be extracted. An energy ranking will be given and the 
low-energy conformers will be used for B3LYP optimization.

The input files is the completed case in the directory _d_conformerPM6Gjfs. This .py file will read 
the .log files in the sub-directories in _d_conformerPM6Gjfs and extract the optimized geometry. By 
default the standard orientation in the .log file will be used, if the key word like nosym used, 
the code tmp_m = pattern_standard.match(tmp_line) should be replaced with tmp_m = pattern_input.match(tmp_line).

The ouput files will appear in the directory _e_conformerB3LYPGjfs. Firstly, an energy ranking will 
be concluded, and several conformers with relatively low energy will be used for the next B3LYP optimization.
For reference, the energy collection is saved as EnergyCollection.xlsx in the directory _d_conformerPM6Gjfs.
In the directory _e_conformerB3LYPGjfs, every sub-directory named like CnH2n+2_#_1_opt_B3L is an independent 
computational case. The .job file in the directory CnH2n+2_#_1_opt_B3L is used to control the behavior of 
the cluster/PC, the .gjf file is the input for the Gaussian program. To control the number of low-energy 
conformers to be optimized with B3LYP, please modify the code in _d_PM6FromConfSearch.py. The related code 
is as below.

	for tmp_file in sortedDict[0:10]:
	tmp_m = pattern_fileConf.match(tmp_file[0])
	if not tmp_m:
		print 'Error! Not structure from conformer searching!'
		continue

To control the details of the output scripts, please modify the code in the method genFrogInputFromGjf() 
in cluter.py file.

-----------------------------
_f_lowestEnergyFromB3LYP.py
-----------------------------
This file is used to generate scripts for B3LYP optimization and frequencies calculation on the 
lowest-energy conformer. The geometry structures optimized with B3LYP in _e_conformerB3LYPGjfs 
with be extracted. An energy ranking will be given and the lowest-energy conformers will be used 
for the final B3LYP optimization and frequencies calculation.

The input files is the completed case in the directory _e_conformerB3LYPGjfs. This .py file will read 
the .log files in the sub-directories in _e_conformerB3LYPGjfs and extract the optimized geometry. By 
default the standard orientation in the .log file will be used, if the key word like nosym used, 
the code tmp_m = pattern_standard.match(tmp_line) should be replaced with tmp_m = pattern_input.match(tmp_line).

The ouput files will appear in the directory _f_lowestEnergy. Firstly, an energy ranking will be concluded, 
and the conformer with the lowest energy will be used for the final B3LYP optimization and frequencies 
calculation. For reference, the energy collection is saved as EnergyCollection.xlsx in the directory 
_e_conformerB3LYPGjfs. In the directory _f_lowestEnergy, every sub-directory named like CnH2n+2_#_2_opt_B3L 
is an independent computational case. The .job file in the directory CnH2n+2_#_2_opt_B3L is used to control 
the behavior of the cluster/PC, the .gjf file is the input for the Gaussian program. To control the details 
of the output scripts, please modify the code in the method genFrogInputFromGjf() in cluter.py file.

-----------------------------
_g_SPEnergyFromOpt.py
-----------------------------
This file is used to generate scripts for M06 single point energy calculation based on the optimization 
with B3LYP and a smaller basis set. The geometry structures optimized with B3LYP with be extracted for 
the single point energy calculation.

The input files is the completed case in the directory _f_lowestEnergy. This .py file will read 
the .log files in the sub-directories in _f_lowestEnergy and extract the optimized geometry. By 
default the standard orientation in the .log file will be used, if the key word like nosym used, 
the code tmp_m = pattern_standard.match(tmp_line) should be replaced with tmp_m = pattern_input.match(tmp_line).

The ouput files will appear in the directory _g_SPEnergy. Every sub-directory named like CnH2n+2_#_3_SP_M06 
is an independent computational case. The .job file in the directory CnH2n+2_#_3_SP_M06 is used to control 
the behavior of the cluster/PC, the .gjf file is the input for the Gaussian program. To control the details 
of the output scripts, please modify the code in the method genFrogInputFromGjf() in cluter.py file. For 
reference, the energy collection is saved as EnergyCollection.xlsx in the directory _f_lowestEnergy.

-----------------------------
_h_radicalFromOpt.py
-----------------------------
This file is used to generate scripts for radical optimization based on the optimization with B3LYP. 
The initial geometry structures is obtained by removing one of the hydrogens of the parent molecule
in _f_lowestEnergy.

The input files is the completed case in the directory _f_lowestEnergy, this .py file will read 
the .log files in the sub-directories in _f_lowestEnergy and extract the optimized geometry. By 
default the standard orientation in the .log file will be used, if the key word like nosym used, 
the code tmp_m = pattern_standard.match(tmp_line) should be replaced with tmp_m = pattern_input.match(tmp_line).

The ouput files will appear in the directory _h_radicalGeneration. Every sub-directory named like 
CnH2n+2_#_r#_C#_2_opt_B3L is an independent computational case. The .job file in the directory 
CnH2n+2_#_2_opt_B3L is used to control the behavior of the cluster/PC, the .gjf file is the input for 
the Gaussian program. To control the details of the output scripts, please modify the code in the method 
genFrogInputFromGjf() in cluter.py file. For reference, the energy collection of the parent molecules 
is saved as EnergyCollection.xlsx in the directory _h_radicalGeneration.

-----------------------------
_i_radicalSPEnergyFromOpt.py
-----------------------------
This file is used to generate scripts for radical single energy calculation based on the optimization 
with B3LYP. 

The input files is the completed case in the directory _h_radicalGeneration, this .py file will read 
the .log files in the sub-directories in _h_radicalGeneration and extract the optimized geometry. By 
default the standard orientation in the .log file will be used, if the key word like nosym used, 
the code tmp_m = pattern_standard.match(tmp_line) should be replaced with tmp_m = pattern_input.match(tmp_line).

The ouput files will appear in the directory _h_radicalGeneration. Every sub-directory named like CnH2n+2_#_r#_C#_3_SP_M06 
is an independent computational case. The .job file in the directory CnH2n+2_#_3_SP_M06 is used to control 
the behavior of the cluster/PC, the .gjf file is the input for the Gaussian program. To control the details 
of the output scripts, please modify the code in the method genFrogInputFromGjf() in cluter.py file. For 
reference, the energy collection is saved as EnergyCollection.xlsx in the directory _h_radicalGeneration.

Tips:
There is an input area at the beginning of every .py script. This is used to control the working directory 
of the compuation in the cluster/PC.



