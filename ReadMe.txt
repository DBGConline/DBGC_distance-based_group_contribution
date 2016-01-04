This is the 0th edition for github test.

Currently only the database is available.
The source code will be published once a more friendly UI is completed in the future.

The code is divided into three parts.
1.	QMCalculation is used to assist quantum chemistry calculation, if users want to prediction the thermodynamic properties for some new species. More details can be found in the online "ReadMe.txt" file. If user are familiar with quantum chemistry calculation, this package is not necessary.
2.	DatabaseGenerator is used to generate the "database.xls" and "inputVector.xlsx" file. For training or test set construction, the code will use the Gaussian output files in directories "freq" and "energy". For practical prediction, the code will use the geometry files in directory "Gjfs". More details can be found in the online "ReadMe.txt" file.
3.	TrainingTestPrediction is used for training, test and practical prediction. More details can be found in the online "ReadMe.txt" file.

Some Useful Link:
http://bbs.keinsci.com/forum.php
