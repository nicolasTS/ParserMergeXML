#!/usr/bin/python
import os
import sys
import time
import datetime

import operator
import numpy as np
#from pylab import *


import re
import shutil



paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")

# PRMS name 

namePRMS = sys.argv[2] #"kf_G1"
valuePRMS = float(sys.argv[3]) #2.7e-07

perCent = 100
nbPoints = 10
values = []

"""
for a in range(100,0,-step):
	values.append(valuePRMS - valuePRMS*(a/100.0))

for b in range(0,100,step):
	values.append(valuePRMS + valuePRMS*(b/100.0))
"""

#print values
tmpInter = np.linspace(valuePRMS/perCent,valuePRMS*perCent,nbPoints)

for ivalue in tmpInter:
	values.append(ivalue)

values.append(valuePRMS)

#print values


#sys.exit()

outDirectory = "batch_"+namePRMS

if(os.path.isdir(outDirectory) != True):
		os.mkdir(outDirectory)

maxSimu = len(values)



# copy parameters files 
shutil.copyfile("SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore.py")
shutil.copyfile("ODESystems.py", outDirectory + os.sep+ "ODESystems.py")
shutil.copyfile("SaveData.py", outDirectory + os.sep+ "SaveData.py")
shutil.copyfile(simu_params['inCsteFile'], outDirectory + os.sep+ simu_params['inCsteFile'])

ff = simu_params['inCsteFile']
dd = simu_params['outDirectory'] 


for i, iconc in enumerate(values):

	finalDirectory = outDirectory +os.sep +dd+namePRMS+"_"+ str(i)

	fCSTES = ff[:-4] + "_"+ str(i) + ".txt"

	f = open(outDirectory +os.sep + fCSTES,'w')

	#changement du prm cinetique
	for line in file(ff, 'r' ):
		(a,b)=line.split(' = ')
		if (a == " " +namePRMS):
			#print "gagne"
			b = str(iconc) + "\n"
		f.write(str(a) +" = " + str(b))

	simu_params['inCsteFile'] = fCSTES
	simu_params['outDirectory'] = dd+namePRMS+"_"+ str(i)
	os.mkdir(finalDirectory )

	#ecriture du fichier 
	fPRMS = paramfilepath + "_"+ str(i) + ".py"

	f = open(outDirectory +os.sep + fPRMS,'w')
	f.write("merge_params =" +str(merge_params))
	f.write("\n")
	f.write("simu_params = " +str(simu_params))
	f.close()
	

	sys.stdout.flush()
	

	#print "python SimulatoreCore.py "+ str(fPRMS) 
	os.system("cd "+ outDirectory +os.sep + "; python SimulatoreCore.py "+ fPRMS + " &") 
	time.sleep(5)
	shutil.move(outDirectory +os.sep +fCSTES, finalDirectory + os.sep+ fCSTES)
	shutil.move(outDirectory +os.sep +fPRMS, finalDirectory + os.sep+ fPRMS)

	print "Simulation #"+ str(i) + " / " + str(maxSimu) + " launched"

sys.exit()



