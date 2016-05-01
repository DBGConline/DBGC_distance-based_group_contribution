----------------------------------------------------------------
currentDatabase.xlsx
----------------------------------------------------------------
This is the database used for training and test in the distance-based contribution method. Currently this database, which is stored in the directory Database, has 925 alkanes ranging from C3 to C13, 634 alkenes ranging from C3 to C10, 871 alkyl radicals ranging from C3 to C10, and 1458 alkenyl radicals ranging from C3 to C9. The standard enthalpy of formation at M062X/def2TZVP//B3LYP/6-31G(d) level of theory, the optimized structure and frequencies at B3LYP/6-31G(d) level of theory, the group contribution vector, SMILES, connectivity, formula, atoms number and multiplicity are recorded in this database file.

Explanation for the columns.

ID
	This is the ID for species.
	
SMILES	
	"This is the SMILES for species.
	Hydrogen atom is omitted in the SMILES for molecule.
	The SMILES with hydrogen is used for radicals to indicate the site."
	
Formula	
	This is the formula for species.
	
Atoms Number	
	This is the number of all atoms.
	
SCF Energy in folder freq (unit: hartree)	
	This is the SCF energy without ZPE correction at the B3LYP/6-31G(d) level of theory.
	
ZPE (0 K) Energy in folder freq (unit: hartree)	
	This is the energy at 0 K with ZPE correction at the B3LYP/6-31G(d) level of theory. The scaling factor is not used here, but in the further calculation.
	
Enthalpy (298.15 K) in folder freq (unit: hartree)	
	This is the enthalpy at 298.15 K at the B3LYP/6-31G(d) level of theory. The scaling factor is not used here, but in the further calculation.
	
SP Energy in folder energy (unit: hartree)	
	This is the SCF energy without ZPE correction at the M062X/def2TZVP level of theory, based on the optimized geometry at B3LYP/6-31G(d) level of theory.
	
SP Energy (0 K) in folder energy corrected with freq scaling factor (unit: hartree)	
	This is the enegy at 0 K at M062X/def2TZVP level of theory, based on the optimized geometry and ZPE correction at the B3LYP/6-31G(d) level of theory. The ZPE scaling factor 0.977 is used here.
	
SP Enthalpy (298.15 K) in folder energy with ZPE and enthalpy correction (unit: hartree)	
	This is the enthalpy at 298.15 K at M062X/def2TZVP level of theory, based on the optimized geometry, ZPE correction and Hf298 - Hf0 at the B3LYP/6-31G(d) level of theory. The ZPE scaling factor 0.977 is used here. The scaling factor used to calculate the enthalpy difference is 1. Because it is usually very close to 1 at 295.15 K. (Ref: A. P. Scott, L. Radom, J. Phys. Chem, 100 (1996) 16502-16513.) Currently only HHRO approximation is used, because the huge cost of hindered rotation correction. 
	
Calculated standard formation of enthalpy at M062X/def2TZVP//B3LYP/6-31G(d) level of theory (unit: kcal/mol)	
	This is the calculated standard enthalpy of formation at the M062X/def2TZVP//B3LYP/6-31G(d) level of theory. During the calculation of the standard enthalpy of formation, a virtual reaction xC(g)+y/2H2(g)+z/2O2(g)=CxHyOx(g) is constructed. 
	The standard enthalpy of formation of CxHyOx can be calculated with 
	Hf298(CxHyOz(g))-xHf298(C(g))-y/2Hf298(H2(g))-z/2Hf298(O2(g))=Hf298_DFT(CxHyOz)-xHf298_DFT(C(g))-y/2Hf298_DFT(H2(g))-z/2Hf298_DFT(O2(g)), 
	namely, 
	Hf298(CxHyOz(g))=Hf298_DFT(CxHyOz)-xHf298_DFT(C(g))-y/2Hf298_DFT(H2(g))-z/2Hf298_DFT(O2(g))+xHf298(C(g)), 
	because Hf298(H2(g))=0, and Hf298(O2(g))=0. 
	The standard enthalpy of formation of C(g) used is not the experimental value, but an average value calculated from 89 aliphatic species at the same level of quantum theory used in the construction of the database, thus bringing an effect of error cancellation. More details about the 89 species and the calculation of standard enthalpy of formation can be found in the supplementary .docx file.
	
Multiplicity (2*S+1)	
	This is the multiplicity of the species, which in defined in the same way Gaussian, namely, 2*S+1.
	
Connectivity (.gjf format)	
	The is connetivity of atoms, which is defined in the same way as Gaussian. Every line consists of the atom label followed with several (label, bond order) pairs.
	
Geometry	
	This is the optimized geometry structure at the B3LYP/6-31G(d) level of theory. However, it should be noted that in pratical predition, a very accurate geometry is not needed. What is needed as input for the distance-based contribution method is the scratch, which is the sketch drawn that specifies the connectivity of atoms. 
	
Frequencies	
	This is frequencies at the B3LYP/6-31G(d) level of theory.
	
Group contribution vectors	
	This is the group contribution vector generated from the bonding information. This can be done with the code in the directory DatabaseGenerator.

	
