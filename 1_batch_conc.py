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

values = np.logspace(-6,0,20)

outDirectory = "DRC_ACh_v2"

if(os.path.isdir(outDirectory) != True):
		os.mkdir(outDirectory)

maxSimu = len(values)



paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")

basePath = simu_params['outDirectory'] + outDirectory


# copy parameters files 
shutil.copyfile("SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore.py")
shutil.copyfile("ODESystems.py", outDirectory + os.sep+ "ODESystems.py")
shutil.copyfile("SaveData.py", outDirectory + os.sep+ "SaveData.py")

shutil.copyfile(simu_params['inCsteFile'], outDirectory + os.sep+ simu_params['inCsteFile'])


starterBatch = open(outDirectory +os.sep + "start_All_launch.sh",'a')



# for cluster mode
fileLaunchBatch = open(outDirectory +os.sep + "launch_00.sh",'w')
fileLaunchBatch.write("#!/usr/bin/env bash \n#Job name \n#SBATCH -J ")
fileLaunchBatch.write("Jobs_00" + " \n")

fileLaunchBatch.write("#SBATCH --mem-per-cpu=5000 \n")
fileLaunchBatch.write("#SBATCH --ntasks 1 \n")
fileLaunchBatch.write("#SBATCH --ntasks-per-core=1 \n")

fileLaunchBatch.write("#SBATCH --exclusive \n")
fileLaunchBatch.write("#SBATCH --time=1 \n")
fileLaunchBatch.write("scontrol show jobid -dd ${SLURM_JOBID} \n")
fileLaunchBatch.write("srun sleep 10") 
fileLaunchBatch.close()

#for i in $(ls *.sh); do
#	echo item: $i
#done
starterBatch.write("sbatch "+ "launch_00.sh"+" \n")
starterBatch.write("sleep 5 \n")





for i, iconc in enumerate(values):



	simu_params['valuePulse'] = [iconc,0, 0, 0, 0, 0]

	simu_params['outDirectory'] = basePath

	#ecriture du fichier 
	fPRMS = paramfilepath + "_"+ str(i) + ".py"
	print fPRMS + " with value = " + str(iconc)
 	

	f = open(outDirectory +os.sep + fPRMS,'w')
	f.write("merge_params =" +str(merge_params))
	f.write("\n")
	f.write("simu_params = " +str(simu_params))
	f.close()
	
	print outDirectory

	shutil.copyfile(outDirectory + os.sep+ "SimulatoreCore.py", outDirectory + os.sep+ "SimulatoreCore_"+str(i)+".py")
	shutil.copyfile(outDirectory + os.sep+ "ODESystems.py", outDirectory + os.sep+ "ODESystems_"+str(i)+".py")
	shutil.copyfile(outDirectory + os.sep+ "SaveData.py", outDirectory + os.sep+ "SaveData_"+str(i)+".py")

#sed -i -e "s/ODESystems/ODESystems_1/g"

	os.system("sed -i -e 's/ODESystems/ODESystems_"+str(i)+"/g' "+ outDirectory + os.sep+ "SimulatoreCore_"+str(i)+".py")
	os.system("sed -i -e 's/SaveData/SaveData_"+str(i)+"/g' "+ outDirectory + os.sep+ "SimulatoreCore_"+str(i)+".py")


	sys.stdout.flush()
	
	# for cluster mode
	fileLaunchBatch = open(outDirectory +os.sep + "launch_"+str(i)+".sh",'w')
	fileLaunchBatch.write("#!/usr/bin/env bash \n#Job name \n#SBATCH -J ")
	fileLaunchBatch.write("Jobs_"+str(i) + " \n")
	fileLaunchBatch.write("#SBATCH --mem-per-cpu=5000 \n")
	fileLaunchBatch.write("#SBATCH --ntasks 1 \n")
#	fileLaunchBatch.write("#SBATCH --ntasks-per-core=1 \n")

#	fileLaunchBatch.write("#SBATCH --exclusive \n")
	fileLaunchBatch.write("#SBATCH --time=1 \n")

#SBATCH --qos=lowpri
#	fileLaunchBatch.write("#SBATCH --ntasks-per-core=1 \n")

	fileLaunchBatch.write("echo 'LOCALID = ' $SLURM_LOCALID \n")
	fileLaunchBatch.write("echo 'PROCID = ' $SLURM_PROCID \n")

#	fileLaunchBatch.write("#SBATCH --nodes=1 --ntasks-per-core=1 \n")
#	fileLaunchBatch.write("#SBATCH -o slurm." + str(i) + ".out \n")
#	fileLaunchBatch.write("#SBATCH -e slurm." + str(i) + ".err \n")

	fileLaunchBatch.write("scontrol show jobid -dd ${SLURM_JOBID} \n")
	fileLaunchBatch.write("srun python SimulatoreCore_"+str(i)+".py " + fPRMS) 
	fileLaunchBatch.close()

	os.system("cd "+ outDirectory +os.sep + "; sbatch launch_"+str(i)+".sh")
	time.sleep(2)

	starterBatch.write("sbatch "+ "launch_"+str(i)+".sh"+" \n")
	starterBatch.write("sleep 2 \n")


	#os.system("cd "+ outDirectory +os.sep + "; sbatch launch_"+str(i)+".sh") 
	
	# for single machine
	# os.system("cd "+ outDirectory +os.sep + "; python SimulatoreCore.py "+ fPRMS + " &") 

	#time.sleep(2)
	print "Simulation #"+ str(i) + " / " + str(maxSimu) + " launched"

sys.exit()



