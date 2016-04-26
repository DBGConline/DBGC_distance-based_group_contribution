import re

# constants
elementDict={1:'H',6:'C',7:'N',8:'O',
'1':'H','6':'C','7':'N','8':'O'
}

def geometryExtractor(lines):
	geom = ''
	for tmp_line in lines:
		tmp_line = tmp_line.strip()
		tmp_line = tmp_line.split()
		geom += elementDict[tmp_line[1]] + '\t' + tmp_line[3] + '\t' + tmp_line[4] + '\t' + tmp_line[5] + '\n'
	return geom

def molproGeometryExtractor(lines):
	geom = ''
	for tmp_line in lines:
		tmp_line = tmp_line.strip()
		tmp_line = tmp_line.split()
		geom += elementDict[tmp_line[1]] + ',\t' + tmp_line[3] + ',\t' + tmp_line[4] + ',\t' + tmp_line[5] + '\n'
	return geom

def mominertGeometryExtractor(lines):
	geom = ''
	tmp_num = 0
	for tmp_line in lines:
		tmp_num += 1
		tmp_line = tmp_line.strip()
		tmp_line = tmp_line.split()
		geom += tmp_line[0] + '\t' + str(tmp_num) + '\t' + tmp_line[1] + '\t' + tmp_line[2] + '\t' + tmp_line[3] + '\n'
	return geom

def hessianExtractor(lines):
	pattern_hessian = re.compile('^.*NImag=[0-9+]\\\\\\\\([-0-9.,]+)\\\\\\\\.*$')
	hessian = []

	for i in range(len(lines)):
		lines[i] = lines[i][1:].strip('\n')
	tmp_line = ''.join(lines)

	tmp_m = pattern_hessian.match(tmp_line)
	if tmp_m:
		hessian = tmp_m.group(1).split(',')
	hessian = [float(x) for x in hessian]	
	return hessian

# extract float number form a data summary format
# e.g. '[23.345,234.034,234.234]'
def floatFromSummary(line):
	data = line.strip('[]')
	data = data.split(',')
	data = map(float, data)
	return data

