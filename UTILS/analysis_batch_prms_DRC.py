#!/usr/bin/python
import os
import sys
import time
import datetime
import glob
import operator
import numpy as np
import pp
import math, sys, md5, time




#################################################
tag =str(sys.argv[1]) #"k_reconst" #

path = "batch_"+tag
Xfile="ACh"
Yfile="IP3"
namePRMS = tag #"kass_re12"
cstesBase = "Cstes"
ncpus=int(18)
#################################################



valuePRMfile = []
valueXfile = []
valueYfile = []
valueYfileAUC = []
valueYfileDecay = []


def maxValue3D(fileCste, namePRMS, fileNameX, fileNameY):
	""" calcule max value for a txt file """
	import numpy as np
	from prms_utils import func, func2
	
	from scipy.optimize import curve_fit

	for line in file(fileCste, 'r' ):
		if not line.startswith('#'):
			(a,b)=line.split(' = ')
			if (a == " " +namePRMS):
				valuePrm = float(b[:-1])

	X1, Y1 = np.loadtxt(fileNameX,unpack=True)
	maxDataX = max(Y1)

	X2, Y2 = np.loadtxt(fileNameY,unpack=True)
	maxDataY = max(Y2)
	auc=np.trapz(Y2,X2)

	timeForPeak = np.argmax(Y2)
	dataXcut=X2[timeForPeak:]
	dataYcut=Y2[timeForPeak:]
	try: 
		popt, pcov = curve_fit(func, dataXcut, dataYcut, [maxDataY,max(X2)]) #, maxfev = 1000)
		#popt, pcov = curve_fit(func2, dataXcut, dataYcut, [maxDataY,max(X2), maxDataY,max(X2)], maxfev = 1000)
		stder = np.sqrt(np.diag(pcov))
		threshold = 0.1

		if (stder[1] < (popt[1]*threshold)):
			decay = popt[1]
			#print "Decay= " + str(popt[1]) + " STDR= " + str(stder[1]) + " PRMS= " + str(namePRMS) + "FILE CSTE = " + str(fileCste)
		else:
			popt, pcov = curve_fit(func2, dataXcut, dataYcut, [maxDataY,max(X2), maxDataY,max(X2)]) #, maxfev = 1000)

			stder2 = np.sqrt(np.diag(pcov))
			if (stder2[1] < (popt[1]*threshold)):
				decay = popt[1]
				#print "mauvais fit"+ " PRMS= " + str(namePRMS) + "FILE CSTE = " + str(fileCste)
			else:
				#print "pb"
				decay = 666
	except:
		print "no Fit with Mono exp and exp , check output to delete 666 for decay"
		decay = 666
	#p0 = [maxDataY,max(X2)] # initial guesses
	#pbest = leastsq(residuals,p0,args=(dataYcut,dataXcut),full_output=1)
	#print 'Decay time fit with mono exp ',pbest[0][1]
	#decay = pbest[0][1]
	

	return valuePrm, maxDataX, maxDataY, auc, decay






ppservers=("*",)
#ncpus=84	, ppservers=ppservers,
job_server = pp.Server( ppservers=ppservers, secret='123')



job_server.set_ncpus(ncpus)
print job_server.get_active_nodes()
print "Starting ", job_server.get_ncpus(), " workers"



jobs = []
start_time = time.time()


for base in glob.glob(path +os.sep + namePRMS +"_*/*/" ):
	nameX = glob.glob(base + "/*/" + Xfile +"/Sim0.txt")
	nameY = glob.glob(base + "/*/" + Yfile +"/Sim0.txt")
	fileCste = glob.glob(base + cstesBase + "*.txt")
	for item in zip(nameX, nameY):
		#print item[0]
		#print item[1]
		#print fileCste[0]
		#print "\n"
		#(a,b,c) = maxValue3D(fileCste[0], namePRMS, item[0], item[1])
		#print str(a) + " " + str(b) + " " + str(c)		
		jobs.append(job_server.submit(maxValue3D,(fileCste[0], namePRMS, item[0], item[1] ) ))
		

for job in jobs:
	#valuePrm, maxDataX, maxDataY, auc, decay
	(a, b, c, d, e) = job()
	valuePRMfile.append(a)
	valueXfile.append(b)
	valueYfile.append(c)
	valueYfileAUC.append(d)
	valueYfileDecay.append(e)

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()




data = zip(valuePRMfile, valueXfile, valueYfile, valueYfileAUC, valueYfileDecay)



# sort result file
numberR={}
for i in range(len(data)):
	numberR[i]= [float(data[i][0]),  float(data[i][1]),  float(data[i][2]), float(data[i][3]), float(data[i][4])]
# sort according 
lsrt= sorted(numberR.iteritems(), key=operator.itemgetter(1))


#ecrire dans un fichier txt

sortFile = file(path + "/analysis_PRMS_" + Xfile + "_" + Yfile + ".txt", 'a')
print>>sortFile, "#  "+str(namePRMS) + "  "+ str(Xfile) + "   " +str(Yfile) + "  " + str("AUC  Decay")
print>>sortFile, "# Warning 666 for decay = no good fit \n" 

for ivalue in lsrt:
	# pour enlever les cas ou pas possible de faire un fit
	#if (ivalue[1][4] != 666.0):
	print>>sortFile, str(ivalue[1][0]) + " " +str(ivalue[1][1])+ " " +str(ivalue[1][2])+" " +str(ivalue[1][3])+" " +str(ivalue[1][4])


 
