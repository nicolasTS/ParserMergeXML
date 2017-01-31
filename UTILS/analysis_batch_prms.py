#!/usr/bin/python
import os
import sys
import time
import datetime
import glob
import operator
import numpy as np

#################################################


namePRMS = sys.argv[1] #"kf_G1"
#Yfile="IP3"
Yfile=sys.argv[2] #"Ga_GTP"

path = "./batch_"+namePRMS +"/"

Xfile="Cstes_CHO.txt"

#################################################

listDir = []
valueXfile = []
valueYfile = []


# recuperation du prm cinetiq
for nameX in glob.glob(path +"/*/" + Xfile.rstrip(".txt")+"*"):
	listDir.append(os.path.dirname(nameX))
	for i, line in enumerate(file(nameX, 'r' )):
		(a,b)=line.split(' = ')
		if (a == " " +namePRMS):
			valueXfile.append(b[:-1])



# recuperation du max pour valeur output
for nameY in listDir:
	n = glob.glob(nameY + "/*/" + Yfile +"/Sim0.txt")
	X, Y = np.loadtxt(n[0],unpack=True)
	valueYfile.append(max(Y))

data = zip(valueXfile, valueYfile)



# sort result file
numberR={}
for i in range(len(data)):
	numberR[i]= [float(data[i][0]),  float(data[i][1])]
# sort according 
lsrt= sorted(numberR.iteritems(), key=operator.itemgetter(1))


#ecrire dans un fichier txt

sortFile = file(path + "/analysis" + namePRMS + "_" + Yfile + ".txt", 'a')
print>>sortFile, "#  " + str(namePRMS) + "   " +str(Yfile)
for ivalue in lsrt: 
	print>>sortFile, str(ivalue[1][0]) + " " +str(ivalue[1][1])


 
