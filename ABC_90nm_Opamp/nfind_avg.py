basename = 'nrun' 

FN = 10
FILE = [] 

FOUT = open(basename, 'w')

for i in range(1,FN+1) :
	FILE.append(open(str(basename + str(i)),'r')) ;


err = 0
gain = 0
ugb = 0
pm = 0
pc = 0 
psrr = 0
cmrr = 0
rsr  = 0 
fsr = 0        	

for i in range(0, FN) :
	while True :
		line = FILE[i].readline()
		lines = line.split()
		index = int(lines[0])
		#print index
		if(index ==5000) :
			err = err + float(lines[1]);
			gain = gain + float(lines[2]);
			pm = pm + float(lines[3]);
			ugb = ugb + float(lines[4]);
			psrr = psrr + float(lines[5]);
			cmrr = cmrr + float(lines[6]);
			pc = pc + float(lines[7]);
			rsr = rsr + float(lines[8]);
			fsr = fsr + float(lines[9]);	
			break

for i in range(0,FN) :
	FILE[i].close()

err = err/FN 
gain = gain/FN
pm = pm/FN
ugb = ugb/FN
psrr = psrr/FN
cmrr = cmrr/FN
pc = pc/FN
rsr = rsr/FN
fsr= fsr/FN

FOUT.write(str(err)+str('\t')+str(gain)+str('\t')+str(pm)+str('\t')+str(ugb)+str('\t')+str(psrr)+str('\t')+str(cmrr)+str('\t')+str(pc)+str('\t')+str(rsr)+str('\t')+str(fsr)+str('\n'))

FOUT.close()
