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
path = "TEST_QUEUE_CPU"
Xfile="ACh"
Yfile="IP3"

#################################################




valueXfile = []
valueYfile = []

def maxValue(fileName):
	""" calcule max value for a txt file """
	import numpy as np
	X, Y = np.loadtxt(fileName,unpack=True)
	maxData = max(Y)
	return maxData


job_server = pp.Server(secret='password')

print "Starting ", job_server.get_ncpus(), " workers"



for base in glob.glob(path +"/*/" ):

	nameX = base + Xfile +"/Sim0.txt"
	a= job_server.submit(maxValue,(nameX, ) )
	valueXfile.append(a())

	nameY = base + Yfile +"/Sim0.txt"
	b= job_server.submit(maxValue,(nameY, ) )
	valueYfile.append(b())

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


 
