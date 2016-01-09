This is the 0th edition for github test.

Currently only the database is available.  
The source code will be published once a more friendly UI is completed in the future.

The code is divided into three parts.  
1.	QMCalculation is used to assist quantum chemistry calculation, if users want to prediction the thermodynamic properties for some new species. More details can be found in the online "ReadMe.txt" file. If user are familiar with quantum chemistry calculation, this package is not necessary.  
2.	DatabaseGenerator is used to generate the "database.xlsx" and "inputVector.xlsx" file. For training or test set construction, the code will use the Gaussian output files in directories "freq" and "energy". For practical prediction, the code will use the geometry files in directory "Gjfs". More details can be found in the online "ReadMe.txt" file.  
3.	TrainingTestPrediction is used for training, test and practical prediction. More details can be found in the online "ReadMe.txt" file.  

Some Useful Link:  
Google  
https://www.google.com/
keinsci forum  
http://bbs.keinsci.com/forum.php
RMG - Reaction Mechanism Generator   
http://rmg.sourceforge.net/  
 
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

