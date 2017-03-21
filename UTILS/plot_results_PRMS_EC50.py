import numpy as np  
import matplotlib.pyplot as plt
from scipy.optimize import *
import glob
from pylab import *
import os
import sys

from itertools import islice

from prms_utils import *

setup_plot_prms()

#####################################################################################################################

plt.close("all")

path = "batch_kass_re1"
nameOfFiles = "analysis_PRMS_Glu_sumOpen.txt"
tagX = "PRMS"
tagY = "EC50"

NbPrmsUsed = 40
#lire ligne 2 et compter le nombre d occurence dans le fichier

# PRMS d origine et EC50 d orgine
refX = 10.0 #0.55 #10.0
refY = 3.53e-1

###############################################################################################################################

# nom du graph de sortie
outName = nameOfFiles[:-4]
# titre 
graphTitle = "" #Dose Response Curve with 1mM ACh" 

# X and Y labels
xAxisLabel ="["+tagX +"] ()"

yAxisLabel = '['+ tagY+'] '









EC50s = []
prms =[]
x, y , z , z2, z3= np.loadtxt(path + os.sep +  nameOfFiles,unpack=True)

for i in range(0,len(x), NbPrmsUsed):		
	a = []
	b = []
	for line in islice(zip(x,y,z), 0+i, NbPrmsUsed+i):
		#print line[2]
		a.append(line[1])
		b.append(line[2])

	try:
		plsq = EC50(a, b)
		#print "EC50 = " +str(plsq[1]) + " nH = " + str(plsq[2])
		EC50s.append(plsq[1])
		prms.append(x[i])
	except:
		pass

"""	
print len(prms)
print len(EC50s)

for value in zip(prms, EC50s):
	print value
"""

Fig = plt.figure(num=None)



# titre du graph
plt.suptitle(graphTitle)

"""
plt.plot(prms, EC50s, '-o', color = 'black')

plt.plot(refX, refY, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))
"""

plt.plot(EC50s,prms,  '-o', color = 'black')
plt.plot(refY, refX, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))

plt.semilogx()
plt.semilogy()


# label X
plt.xlabel(yAxisLabel)


# label pour axe Y
plt.ylabel(xAxisLabel)

drop_spines(plt.gca())


#plt.tight_layout()

# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")




plt.show()


#print set(x)
