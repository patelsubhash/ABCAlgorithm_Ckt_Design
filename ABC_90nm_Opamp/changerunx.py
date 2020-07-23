
import copy 



for fn in range(0, 10) :
	inbasename = 'run' + str(fn+1)
	outbasename = 'nrun'+ str(fn+1)
	FIN = open(inbasename, 'r')
	FOUT = open(outbasename, 'w')

	cntr = 0 ;
	first = True ;
	write = 'mmm'
	pline = []
	spltline = []
	while True :
		stop = True ;
		line = FIN.readline()
		if line :
			spltline = line.split()
			if not first :
				cntr = cntr + 1
				while(cntr < int(spltline[0])) : 
					write = str(cntr)
					for i in range(1, len(pline)) :
						write = write + '\t' + str(spltline[i])
					write = write + '\n'
					if (cntr <= 5000) :
						FOUT.write(write) ;
					cntr = cntr + 1

                	        FOUT.write(line)
				cntr = cntr+1
			
		else :
			stop = False
			while (cntr <= 5000) :
				write = str(cntr)
				for i in range(1, len(pline)) :
					write = write + '\t' + str(spltline[i])
				write = write + '\n'
				FOUT.write(write) ;
				cntr = cntr + 1	
			print cntr
		first = False 
		pline = copy.copy(spltline)
		if stop==False :
			break  
	

	FIN.close()
	FOUT.close()
