#!/usr/bin/python
import os
import sys
import time
import datetime
import glob
import operator
import numpy as np
import pp

#################################################


namePRMS = sys.argv[1] #"kf_G1"
Yfile=sys.argv[2] #"Ga_GTP"
ncpus=int(sys.argv[3])

path = "./batch_"+namePRMS +"/"

Xfile="Cstes.txt"

#################################################

listDir = []
valueXfile = []
valueYfile = []


# recupere la valeur du prm cinetique ainsi que le max de l output demande
def prmMax(cstFile, namePRMS, Yfile):
	import numpy as np
	import glob
	import os
	for line in file(cstFile, 'r' ):
		if not line.startswith('#'):
			(a,b)=line.split(' = ')
			if (a == " " +namePRMS):
				valuePrm = float(b[:-1])

	n = glob.glob(os.path.dirname(cstFile) + "/*/" + Yfile +"/Sim0.txt")
	X, Y = np.loadtxt(n[0],unpack=True)
	maxValue = max(Y)

	return valuePrm, maxValue



ppservers=("*",)
job_server = pp.Server( ppservers=ppservers, secret='123')

job_server.set_ncpus(ncpus)
print job_server.get_active_nodes()
print "Starting ", job_server.get_ncpus(), " workers"


jobs = []
start_time = time.time()

for nameX in glob.glob(path +"/*/" + Xfile.rstrip(".txt")+"*"):
	#print prmMax(nameX, namePRMS, Yfile)
	jobs.append(job_server.submit(prmMax,(nameX,namePRMS, Yfile ) ))


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

sortFile = file(path + "/analysis" + namePRMS + "_" + Yfile + ".txt", 'a')
print>>sortFile, "#  " + str(namePRMS) + "   " +str(Yfile)
for ivalue in lsrt: 
	print>>sortFile, str(ivalue[1][0]) + " " +str(ivalue[1][1])


 
