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


# Ligand

values = np.logspace(-6,1,20)
values2 = np.logspace(-6,1,20)

outDirectory = "DRC_ACh_L"

if(os.path.isdir(outDirectory) != True):
		os.mkdir(outDirectory)

maxSimu = len(values)*len(values2)



paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")


# copy parameters files 
shutil.copyfile("SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore.py")
shutil.copyfile("ODESystems.py", outDirectory + os.sep+ "ODESystems.py")
shutil.copyfile("SaveData.py", outDirectory + os.sep+ "SaveData.py")

shutil.copyfile(simu_params['inCsteFile'], outDirectory + os.sep+ simu_params['inCsteFile'])


#'inCsteFile' : "./Cstes.txt",
#os.system("cd "+ outDirectory +os.sep)

compteur = 0

for i, iconc in enumerate(values):
	for i2, iconc2 in enumerate(values2):

		compteur+=1

		simu_params['valuePulse'] = [iconc,0, iconc2, 0, 0, 0]

		#ecriture du fichier 
		fPRMS = paramfilepath + "_"+ str(compteur) + ".py"
		print fPRMS
	 	

		f = open(outDirectory +os.sep + fPRMS,'w')
		f.write("merge_params =" +str(merge_params))
		f.write("\n")
		f.write("simu_params = " +str(simu_params))
		f.close()
	

		sys.stdout.flush()
	

		#print "python SimulatoreCore.py "+ str(fPRMS) 
		os.system("cd "+ outDirectory +os.sep + "; python SimulatoreCore.py "+ fPRMS + " &") 
		time.sleep(5)
		print "Simulation #"+ str(compteur) + " / " + str(maxSimu) + " launched"

sys.exit()



