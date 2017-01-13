#!/usr/bin/python
import os
import sys
import time
import datetime
import glob
import operator
import numpy as np

#################################################
path = "DRC_ACh"
Xfile="ACh"
Yfile="IP3"

#################################################

valueXfile = []
valueYfile = []


# recuperation du max pour concentration
for nameX in glob.glob(path +"/*/" + Xfile +"/Sim0.txt"):
	X, Y = np.loadtxt(nameX,unpack=True)
	valueXfile.append(max(Y))


# recuperation du max pour valeur output
for nameY in glob.glob(path +"/*/" + Yfile +"/Sim0.txt"):
	X, Y = np.loadtxt(nameY,unpack=True)
	valueYfile.append(max(Y))

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


 
