import os
import glob

OutputFileName = 'FormattedTEDFRSMIG.md'


nb_TKTREQ = 0
contents_all = ''

# for filename in glob.glob(os.path.join('UAT.TKT.ECO.BATCH.*')):
for filename in glob.glob(os.path.join('UAT.TKT.ECO.BATCH.D160826.T160048.DATA')):  
	with open (filename, 'rt') as in_file:
		contents = in_file.read()		
		contents = contents.replace('','+')
		contents = contents.replace('',':')
		contents = contents.replace('','\n')
		nb_TKTREQ += contents.count('UNH+')
		contents_all += contents
with open(OutputFileName, 'w') as f:
	f.write(contents)


print('The total number of TKTREQ messages in the fold: ',nb_TKTREQ)