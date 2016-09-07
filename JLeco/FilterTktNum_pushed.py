import os
import glob
import re

def get_pos_message(str_MSG, contents):
	MSG_start = []
	MSG_end = []
	for m in re.finditer(str_MSG, contents):
		MSG_start.append(m.end())
		MSG_end.append(m.start())
	MSG_end = MSG_end[1:]+[len(contents)]
	# print(MSG_start)
	# print(MSG_end)
	return MSG_start, MSG_end

def get_AL(MSG_start,MSG_end,contents,pat_TKT_CPN):
	# get primary ticket number and the insertion schema
	m = pat_TKT_CPN.search(contents,MSG_start, MSG_end)
	if m == None:
		print ('Error! Input TKTREQ message is wrong')	
	TktNum = m.group(1)
	nalc = TktNum[0:3] 
	AL = [m.group(2)]		
	# print('TktNum is : ', TktNum, '\nAL is : ', AL)
	
	## if 2rd view exists, get 2rd view insertion schema
	if contents[m.end():m.end()+3] == 'CPN':  # 2 View 
		# print('found 2nd view')
		n = pat_CPN_2rdView.search(contents,m.end())
		if n == None:
			print('Error! Input TKTREQ message of {} is wrong: insertion schema in CPN for 2nd view is not found'.format(TktNum))
		AL += [n.group(1)]
		# print('TktNum is : ', TktNum, '\nAL is : ', AL)
	return TktNum, nalc, AL


if __name__ == '__main__':

	OutputFileName_JL = 'PushedTktNum_JL.md'
	OutputFileName_JC = 'PushedTktNum_JC.md'
	OutputFileName_NU = 'PushedTktNum_NU.md'

	TktNum_JL = set()
	TktNum_JC = set()
	TktNum_NU = set()

	str_MSG = r'MSGMIG' # match this string in order to count the number of TKTREQ message pushed in all files
	# match TKT segment and following CPN segment in order to find primary TktNum and 1st insertion schema
	str_TKT_CPN = r'TKT([0-9]{13}).*?.*?3CPN.*?99(JL|JC|NU).*?' 
	str_CPN_2rdView = r'CPN.*?99(JL|JC|NU).*?' # match 1st CPN segment (whole line) in order to find if the next line is still CPN (2Views)
	pat_TKT_CPN = re.compile(str_TKT_CPN) 
	pat_CPN_2rdView = re.compile(str_CPN_2rdView)

	for filename in glob.glob(os.path.join('c_TST.TKT.JLTT*')):
	# for filename in glob.glob(os.path.join('c_TST.TKT.JLTT001.20160826.1438')):  
		with open (filename, 'rt') as in_file:
			contents = in_file.read()
			## to define roughly the position of each TKTREQ message
			MSG_start, MSG_end = get_pos_message(str_MSG, contents)
		
			for i in range(len(MSG_start)):
				## get airline schema for the TKTREQ message
				TktNum, nalc, AL_list = get_AL(MSG_start[i],MSG_end[i],contents,pat_TKT_CPN)
				
				## add ticket number to corresponding airline schema
				if 'JL' in AL_list:
					TktNum_JL.add(TktNum)
				if 'JC' in AL_list:
					TktNum_JC.add(TktNum)
				if 'NU' in AL_list:
					TktNum_NU.add(TktNum)

	# write ticket numbers to 3 files				
	with open(OutputFileName_JL, 'w') as f:
		for wordline in TktNum_JL:
			f.write(wordline+'\n')

	with open(OutputFileName_JC, 'w') as f:
		for wordline in TktNum_JC:
			f.write(wordline+'\n')

	with open(OutputFileName_NU, 'w') as f:
		for wordline in TktNum_NU:
			f.write(wordline+'\n')

	print("Number of ticket in '{}' is : '{}'".format(OutputFileName_JL,len(TktNum_JL)))
	print("Number of ticket in '{}' is : '{}'".format(OutputFileName_JC,len(TktNum_JC)))
	print("Number of ticket in '{}' is : '{}'".format(OutputFileName_NU,len(TktNum_NU)))


