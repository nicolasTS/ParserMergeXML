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

outDirectory = "DRC_ACh"

if(os.path.isdir(outDirectory) != True):
		os.mkdir(outDirectory)

maxSimu = len(values)



paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")


# copy parameters files 
shutil.copyfile("SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore.py")
shutil.copyfile("ODESystems.py", outDirectory + os.sep+ "ODESystems.py")
shutil.copyfile("SaveData.py", outDirectory + os.sep+ "/SaveData.py")


#os.system("cd "+ outDirectory +os.sep)

 
for i, iconc in enumerate(values):


	simu_params['valuePulse'] = [iconc,0, 0, 0, 0, 0]

	#ecriture du fichier 
	fPRMS = paramfilepath + "_"+ str(i) + ".py"
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
	print "Simulation #"+ str(i) + " / " + str(maxSimu) + " launched"

sys.exit()



