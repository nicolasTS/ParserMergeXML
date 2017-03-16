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
path = "batch_kass_re1"
Xfile="Glu"
Yfile="sumOpen"
namePRMS = "kass_re1"
cstesBase = "Cstes"
ncpus=int(4)
#################################################



valuePRMfile = []
valueXfile = []
valueYfile = []

def maxValue3D(fileCste, namePRMS, fileNameX, fileNameY):
	""" calcule max value for a txt file """
	import numpy as np
	for line in file(fileCste, 'r' ):
		if not line.startswith('#'):
			(a,b)=line.split(' = ')
			if (a == " " +namePRMS):
				valuePrm = float(b[:-1])

	X1, Y1 = np.loadtxt(fileNameX,unpack=True)
	maxDataX = max(Y1)
	X2, Y2 = np.loadtxt(fileNameY,unpack=True)
	maxDataY = max(Y2)

	return valuePrm, maxDataX, maxDataY






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
		jobs.append(job_server.submit(maxValue3D,(fileCste[0], namePRMS, item[0], item[1] ) ))
		#print str(a) + " " + str(b) + " " + str(c)


for job in jobs:
	(a, b, c) = job()
	valuePRMfile.append(a)
	valueXfile.append(b)
	valueYfile.append(c)


print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()




data = zip(valuePRMfile, valueXfile, valueYfile)


# sort result file
numberR={}
for i in range(len(data)):
	numberR[i]= [float(data[i][0]),  float(data[i][1]),  float(data[i][2])]
# sort according 
lsrt= sorted(numberR.iteritems(), key=operator.itemgetter(1))


#ecrire dans un fichier txt

sortFile = file(path + "/analysis_PRMS_" + Xfile + "_" + Yfile + ".txt", 'a')
print>>sortFile, "#  "+str(namePRMS) + " "+ str(Xfile) + "   " +str(Yfile)
for ivalue in lsrt: 
	print>>sortFile, str(ivalue[1][0]) + " " +str(ivalue[1][1])+ " " +str(ivalue[1][2])


 
