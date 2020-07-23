
import random
import copy
import math

import os

SPECTS =["Gain","PM",	"BW",	"PSRR", "CMRR", "PC",	"RSR",	"FSR"]
DVAL =  [80,	60,	100E6,	75,	80,	20E-6,	40,	40 ]
DVALLL=	[80,	60,	100E6,	75,	80,	0,	40,	40 ]
DVALUL=	[200,	80,	100E9,	1000,	1000,	20E-6,	80,	80]	
MUL   = [1,	1,	1E-6,	1,	1,	1E6,	1,	1]

CP   =  [0,	0,	0,	0,	0,	0,	0,	0]
BSP  =  [0,	0,	0,	0,	0,	0,	0,	0]
		

VNAME = [ 'w1',	'w2',	'w3',	'w4',	'w5',	'w6',	'w7',	'w8',	'w9',	'l1',	'l2',	'l3',	'l4',	'l5',	'i0',	'cc']
MIN = 	[5E-7, 	5E-7,	5E-7,	5E-7,	5E-7,	5E-7,	5E-7,	5E-7,	5E-7,	0.1e-6,	0.1e-6,	0.1e-6,	0.1e-6,	0.1e-6,	1e-6,	1e-13]
MAX = 	[8e-6, 	8e-6,	8e-6,	8E-6,	8e-6,	8E-6,	8e-6,	8e-6,	8e-6,	1e-6,	1e-6,	1e-6,	1e-6,	1E-6,	10e-6,	1e-15]
RES = 	[7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	7,	15]


D = len(VNAME) 




def writeVariable(TP) :
	FILE = open('variable', 'w')
	FILE.write('\n')
	for i in range(0, len(TP)) :
		FILE.write('.param '+ VNAME[i] + '=' + str(TP[i]) + '\n')
	FILE.close()
			

def costf(TP, PRN) :

	os.system('rm -rf *.data')
	
	writeVariable(TP)
	os.system('ngspice -b  -o simfile opamp.cir > simlog')

	if not os.path.isfile('acsim.data') :
		print "acsim.data error"
		return 100E6 
	if not os.path.isfile('opsim.data') :
		return 200E6
	if not os.path.isfile('transim.data') :
		return 300E6
	
	FILE = open('acsim.data', 'r')
	ln = FILE.readline().split()
	FILE.close()
	CP[0] = float(ln[1])
	CP[1] = float(ln[3])
	CP[2] = float(ln[5])
	CP[3] = float(ln[7])
	CP[4] = float(ln[9])

	FILE = open('opsim.data', 'r')
	ln = FILE.readline().split()
	FILE.close()
    	CP[5] = float(ln[1])
	FILE = open('transim.data', 'r')
	ln = FILE.readline().split()
	FILE.close()
	CP[6] = float(ln[1])
	CP[7] = float(ln[3])
	
	err1=0
	if(CP[1] < 45) :
		err1 = err1 + 100 

	for i in range(0, len(CP)) :
		if (DVALLL[i] <= CP[i] <= DVALUL[i]) :
			err1 = err1 
		else :
			err1 = err1 + ((CP[i]-DVAL[i])/(DVAL[i]))*((CP[i]-DVAL[i])/(DVAL[i]))
			if PRN :
				print SPECTS[i],((CP[i]-DVAL[i])/(DVAL[i]))*((CP[i]-DVAL[i])/(DVAL[i]))
	err1 = err1/float(len(CP))
	err1 = math.sqrt(err1)*100

	PRN = True
	if PRN :
		print "ERR ===> ", err1
		for i in range(0, len(CP)) :
			print SPECTS[i], ' --> ', CP[i]*MUL[i]
		print TP
	
	return err1 



class ABC :

	def __init__(self, dim, swarm, smin, smax, femax) :
 		self.D = dim
		self.SN = swarm
		self.xmin = copy.copy(smin) 
		self.xmax = copy.copy(smax) 
		self.FEMAX = femax 
		self.x = [] 
		self.fx = []
		self.fitx = []
		self.v = []  
		self.fv = 100E100
		self.fitv = 0
		self.gb = []
		self.fgb = 100E100
		self.fitgb = 0
		self.px = [] 
		self.FE = 0 
		self.T = []
		self.Tmax = 200
		



        def find_gb(self) :
		for i in range(0, self.SN) :
			if(self.fgb > self.fx[i]) :
				self.fgb = self.fx[i]
				self.gb = copy.copy(self.x[i]) 
				self.fitgb = self.fitx[i]

	def cal_fit(self, xf) :
		if (xf > 0) :
			return 1/(1+xf)
		else :
			return (1+math.fabs(xf))

	def init(self, index) :
		for j in range(0, self.D) :
			p = random.uniform(self.xmin[j], self.xmax[j])
			self.x[index][j] = round(p,RES[j])
		self.fx[index] = costf(self.x[index], False)
		self.fitx[index] = self.cal_fit(self.fx[index])
		self.T[index] = 0

	def init_all(self) :
		for i in range(0, self.SN) :
			self.T.append(0) 
			self.x.append([])
			for j in range(0,self.D) :
				self.x[i].append(0)
			self.px.append(0)
			self.fx.append(100E100)
			self.fitx.append(0)

		for j in range(0, self.D) :
			self.v.append(0)
			
	
		for i in range(0, self.SN) :
			self.init(i)
		self.FE = self.FE + self.SN
		self.gb = copy.copy(self.x[0])
		self.fgb = self.fx[0]
		for i in range(0, self.SN) :
			if(self.fgb > self.fx[i]) :
				self.fgb = self.fx[i]
				self.gb = copy.copy(self.x[i]) 
				self.fitgb = self.fitx[i]
			

	def find_prob(self) :
		for i in range(0, self.SN) :
			s = 0 
			for j in range(0, self.SN) :
				s = s + self.fitx[j]
			self.px[i] = self.fitx[i]/s 

	def employee(self) :
		for i in range(0, self.SN) :
			p2c = random.randint(0, self.D-1) 
			self.v = copy.copy(self.x[i])
			while True :
				N1 = random.randint(0, self.SN-1)
				if not (i==N1) :
					break 
			R = random.uniform(-1,1) ;
			
			self.v[p2c] = self.v[p2c]+R*(self.v[p2c]-self.x[N1][p2c])
			self.v[p2c] = round(self.v[p2c], RES[p2c])

			if self.v[p2c] > self.xmax[p2c] :
				self.v[p2c] = self.xmax[p2c] 
			if self.v[p2c] < self.xmin[p2c] :
				self.v[p2c] = self.xmin[p2c] 

			self.fv = costf(self.v, False)
			self.fitv = self.cal_fit(self.fv) 
			self.FE = self.FE + 1

			if(self.fitv > self.fitx[i]) :
				self.fitx[i] = self.fitv 
				self.fx[i] = self.fv
				self.x[i] = copy.copy(self.v)
				self.T[i] = 0
			else :
				self.T[i] = self.T[i] + 1 				 	
		

		
	def onlooker(self) :
		Tr = 0
		i = 0
		while Tr < self.SN :
			R = random.uniform(0,1)
			if(R < self.px[i]) :
				Tr = Tr + 1

				p2c = random.randint(0, self.D-1) 
				self.v = copy.copy(self.x[i])
				while True :
					N1 = random.randint(0, self.SN-1)
					if not (i==N1) :
						break 
				R = random.uniform(-1,1) ;
				self.v[p2c] = self.v[p2c]+R*(self.v[p2c]-self.x[N1][p2c])
				self.v[p2c] = round(self.v[p2c], RES[p2c])

				if self.v[p2c] > self.xmax[p2c] :
					self.v[p2c] = self.xmax[p2c] 
				if self.v[p2c] < self.xmin[p2c] :
					self.v[p2c] = self.xmin[p2c] 

				self.fv = costf(self.v, False)
				self.fitv = self.cal_fit(self.fv) 
				self.FE = self.FE + 1

				if(self.fitv > self.fitx[i]) :
					self.fitx[i] = self.fitv 
					self.fx[i] = self.fv
					self.x[i] = copy.copy(self.v)
					self.T[i] = 0
				else :
					self.T[i] = self.T[i] + 1 				 	
			i = i + 1
			if(i == self.SN) :
				i = 0	

	def scout(self) :
		for i in range(0, self.SN) :
			if (self.T[i] > self.Tmax) :
				self.init(i)
				break
		
	
	def startlog(self, LogN) :
		fname = "run" + str(LogN)
		self.log = open(fname, 'w')	

	def closelog(self, LogN) :
		print self.FE, '->', self.fgb
		self.log.close()
		vcp = "cp variable variable" + str(LogN)
		os.system(vcp)

	def solve(self, logn) :
		self.startlog(logn)
		self.init_all()
		while (self.FE < self.FEMAX) :
			
			self.employee()
			self.find_prob()
			self.onlooker()
			self.scout()
			self.find_gb()
			print self.FE, '------------------------------------------------>', self.fgb
			costf(self.gb, True)
			logstr = ''
			for i in range(0, len(CP)) :
				logstr = logstr + '\t' + str(CP[i]) 		
			self.log.write(str(str(self.FE) + '\t' + str(self.fgb) + logstr + '\n'))
			
			if(self.fgb <= 0) :
				break
		self.closelog(logn) 
		costf(self.gb, True)                
	

for i in range(0,10) : 
 	A = ABC(D, 20, MIN, MAX, 5E3);
	A.solve(i+1)
	print i




    	
		


