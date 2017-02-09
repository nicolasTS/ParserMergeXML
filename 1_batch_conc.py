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

values = np.logspace(-6,1,50)

outDirectory = "TEST_QUEUE_toto"

if(os.path.isdir(outDirectory) != True):
		os.mkdir(outDirectory)

maxSimu = len(values)



paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")


# copy parameters files 
shutil.copyfile("SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore.py")
shutil.copyfile("ODESystems.py", outDirectory + os.sep+ "ODESystems.py")
shutil.copyfile("SaveData.py", outDirectory + os.sep+ "SaveData.py")

shutil.copyfile(simu_params['inCsteFile'], outDirectory + os.sep+ simu_params['inCsteFile'])


#'inCsteFile' : "./Cstes.txt",
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
	
	# for cluster mode
	fileLaunchBatch = open(outDirectory +os.sep + "launch.sh",'w')
	fileLaunchBatch.write("#!/usr/bin/env bash \n#Job name \n#SBATCH -J ")
	fileLaunchBatch.write("Jobs_"+str(i) + " \n")
#	fileLaunchBatch.write("#SBATCH --nodes=1 --ntasks-per-node=1 \n")
	fileLaunchBatch.write("#SBATCH --nodes=1 --ntasks-per-core=1 \n")
	fileLaunchBatch.write("time python SimulatoreCore.py " + fPRMS) 
	fileLaunchBatch.close()

	os.system("cd "+ outDirectory +os.sep + "; sbatch launch.sh") 
	
	# for single machine
	# os.system("cd "+ outDirectory +os.sep + "; python SimulatoreCore.py "+ fPRMS + " &") 

	time.sleep(2)
	print "Simulation #"+ str(i) + " / " + str(maxSimu) + " launched"

sys.exit()



