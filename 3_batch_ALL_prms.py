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

# fichier d'import ds prms
paramfilepath = sys.argv[1].rstrip(".py")
exec("from "+paramfilepath+" import *")


# fichier avec liste des prm a batcher
ff = sys.argv[2]
v = []
p = []
for line in file(ff, 'r' ):
	(a,b)=line.split(' = ')
	p.append(a[1:])
	v.append(b[:-1])	
 
	print "PRMS to batch = " + str(a[1:])
	#python batch_prms.py PRMS.py kf_G1 2.7e-7
	os.system("python 2_batch_prms.py " + sys.argv[1] + " "+ a[1:] + " " + b[:-1]) 
	time.sleep(5)


time.sleep(30)

# pour faire l analyse des donnees
for pi in p:
	os.system("python UTILS/analysis_batch_prms.py " + pi + " IP3" + " &") 
	os.system("python UTILS/analysis_batch_prms.py " + pi + " Ga_GTP" + " &") 


time.sleep(30)

# pour faire les plots
for pi in p:
	os.system("python UTILS/plot_results_PRMS.py " + pi " &") 

