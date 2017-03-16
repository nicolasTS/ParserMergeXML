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

values = []

# variation du prm cinetique 

#tmpInter = np.linspace(valuePRMS/perCent,valuePRMS*perCent,nbPoints)
#tmpInter = np.linspace(1e-6,1e0, 40)
tmpInter = np.logspace(-4,4,40)

for ivalue in tmpInter:
	values.append(ivalue)

values.append(valuePRMS)

print values


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

	finalDirectory = dd+outDirectory+os.sep +namePRMS+"_"+ str(i)

	print finalDirectory

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
	simu_params['outDirectory'] = dd+outDirectory+os.sep +namePRMS+"_"+ str(i)
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
	time.sleep(3)
	shutil.move(outDirectory +os.sep +fCSTES, finalDirectory + os.sep+ fCSTES)
	shutil.move(outDirectory +os.sep +fPRMS, finalDirectory + os.sep+ fPRMS)
	
	
	print "Simulation #"+ str(i) + " / " + str(maxSimu) + " launched"

sys.exit()



