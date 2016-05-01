The code is divided into three parts.  

1.	The code in the directory QMCalculation is used to assist quantum chemistry calculation, if users want to prediction the thermodynamic properties for some new species. More details can be found in the "QMCalculation/ReadMe.txt" file. If a user has his own script to help with quantum chemistry calculation, this package is not necessary.

2.	The code in the directory DatabaseGenerator is used to generate the database for training, test and prediction. More details can be found in the "DatabaseGenerator/ReadMe.txt" file.  

3.	The code in the directory TrainingTestPrediction is used for training and testing the network in the group contribution algorithm and for practical prediction. More details can be found in the "rainingTestPrediction/ReadMe.txt" file.  

Currently this database "Database/currentDatabase.xlsx", which is stored in the directory Database, has  925 alkanes ranging from C3 to C13, 634 alkenes ranging from C3 to C10, 871 alkyl radicals ranging from C3 to C10, and 1458 alkenyl radicals ranging from C3 to C9. This is the database used for training and test in the distance-based contribution method. More details can be found in the "Database/ReadMe.txt" file. 

The file "Database/conventionalGAGroups.xlsx" is used for the comparison between the distance-based group contribution method and the conventional GA method. The conventional GA groups and corrections are recorded in this file. More details can be found in the "Database/ReadMe.txt" file.    

To use the code, python is needed to run .py files, and MATLAB is needed to run .m files.  
A Python distribution, Anaconda, is recommended. Ref: https://www.continuum.io/downloads.  
Some packages are also needed to run the code, including xlrd, xlwt, xlutils, xlsxwriter, openpyxl.  
Ref:  
xlrd 	https://pypi.python.org/pypi/xlrd.  
xlwt 	https://pypi.python.org/pypi/xlwt.  
xlutils 	https://pypi.python.org/pypi/xlutils.  
xlsxwriter 	https://pypi.python.org/pypi/XlsxWriter.  
openpyxl	https://openpyxl.readthedocs.org/en/default/.  
MATLAB is a commercial software. Ref: http://www.mathworks.com/products/matlab/index.html?s_tid=gn_loc_drop.  

Some Useful Link: 
DBGC online demo  
http://dbgc.online  
RMG - Reaction Mechanism Generator   
http://rmg.sourceforge.net/  
NIST Structures and Properties  
http://webbook.nist.gov/chemistry/grp-add/ga-file.html  
NIST Chemistry WebBook  
http://webbook.nist.gov/chemistry/name-ser.html  
Burcat's Thermodynamic Data  
http://garfield.chem.elte.hu/Burcat/burcat.html  
 
Some Important Paper:  
S.W. Benson & J.H. Buss, Additivity Rules for the Estimation of Molecular Properties. Thermodynamic Properties, 1958  
http://scitation.aip.org/content/aip/journal/jcp/29/3/10.1063/1.1744539  
S.W. Benson et al., Additivity rules for the estimation of thermochemical properties, 1969  
http://pubs.acs.org/doi/abs/10.1021/cr60259a002  
S.W. Benson, Thermochemical kinetics, 1976  
http://onlinelibrary.wiley.com/doi/10.1002/aic.690230437/abstract  
http://onlinelibrary.wiley.com/doi/10.1002/aic.690230437/epdf  
E.R. Ritter, J.W. Bozzelli, THERM: Thermodynamic property estimation for gas phase radicals and molecules, 1991  
http://onlinelibrary.wiley.com/doi/10.1002/kin.550230903/abstract  
T.H. Lay, J.W. Bozzelli, A.M. Dean, E.R. Ritter, Hydrogen Atom Bond Increments for Calculation of Thermodynamic Properties of Hydrocarbon Radical Species, 1995  
http://pubs.acs.org/doi/abs/10.1021/j100039a045  

P.S. Files in the directory dos2unix-6.0.6-win64 is used for text file format conversion (dos to unix).