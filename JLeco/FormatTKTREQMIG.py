import os
import glob

OutputFileName = 'FormattedTKTREQMIG.md'


nb_TKTREQ = 0
contents_all = ''

for filename in glob.glob(os.path.join('c_TST.TKT.JLTT*')):
# for filename in glob.glob(os.path.join('c_TST.TKT.JLTT001.20160826.1438')):  
	with open (filename, 'rt') as in_file:
		contents = in_file.read()		
		contents = contents.replace('','+')
		contents = contents.replace('',':')
		contents = contents.replace('','\n')
		contents = contents.replace('UNH+','\n\nUNH+')
		nb_TKTREQ += contents.count('UNH+')
		# I have tried to match 'UNH+1+TKTREQ:14:5:1A', the result is the same as that of matching 'UNH'
		# print(contents)
		contents_all += contents
with open(OutputFileName, 'w') as f:
	f.write(contents_all)


print('The total number of TKTREQ messages in the fold: ',nb_TKTREQ)