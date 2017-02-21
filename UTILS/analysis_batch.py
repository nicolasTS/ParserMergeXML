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
path = "DRC_ACh"
Xfile="ACh"
Yfile="Ga_GTP"

#################################################




valueXfile = []
valueYfile = []

def maxValue(fileNameX, fileNameY):
	""" calcule max value for a txt file """
	import numpy as np
	X1, Y1 = np.loadtxt(fileNameX,unpack=True)
	maxDataX = max(Y1)
	X2, Y2 = np.loadtxt(fileNameY,unpack=True)
	maxDataY = max(Y2)

	return maxDataX, maxDataY






ppservers=("*",)
#ncpus=84	, ppservers=ppservers,
job_server = pp.Server( ppservers=ppservers, secret='123')


ncpus=6
job_server.set_ncpus(ncpus)
print job_server.get_active_nodes()
print "Starting ", job_server.get_ncpus(), " workers"



jobs = []
start_time = time.time()


for base in glob.glob(path +"/*/" ):
	nameX = base + Xfile +"/Sim0.txt"
	nameY = base + Yfile +"/Sim0.txt"
	jobs.append(job_server.submit(maxValue,(nameX,nameY ) ))



for job in jobs:
	a, b = job()
	valueXfile.append(a)
	valueYfile.append(b)


print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()


data = zip(valueXfile, valueYfile)


# sort result file
numberR={}
for i in range(len(data)):
	numberR[i]= [float(data[i][0]),  float(data[i][1])]
# sort according 
lsrt= sorted(numberR.iteritems(), key=operator.itemgetter(1))


#ecrire dans un fichier txt

sortFile = file(path + "/analysis" + Xfile + "_" + Yfile + ".txt", 'a')
print>>sortFile, "#  " + str(Xfile) + "   " +str(Yfile)
for ivalue in lsrt: 
	print>>sortFile, str(ivalue[1][0]) + " " +str(ivalue[1][1])


 
