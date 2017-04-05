import numpy as np  
import matplotlib.pyplot as plt
from scipy.optimize import *
import glob
from pylab import *
import os
import sys
import operator

from itertools import islice

from prms_utils import *

setup_plot_prms()

#####################################################################################################################
# nom du fichier a analyser
nameOfFiles = "analysis_PRMS_ACh_IP3.txt"
#EC50 d origine
refY =  1.385e-3
# seuil reglage de error pour le fit EC50
threshold=0.1
###############################################################################################################################


tag = str(sys.argv[1]) #"k_reconst" #"k_PLC" #"kon_ACh" #"k_PLCassoc"

path = "batch_"+tag

tagX = tag #"PRMS"
tagY = "$EC_{50}$"

# PRMS d origine et EC50 d orgine
refX = float(sys.argv[2]) #0.001 #0.0255  #3.02 #0.001 #0.0255 #3.02

# nom du graph de sortie
outName = nameOfFiles[:-4]
# titre 
graphTitle = "" #Dose Response Curve with 1mM ACh" 

# X and Y labels
xAxisLabel =tagX +" ()"

yAxisLabel = '['+ tagY+'] '


EC50s = []
EC50s2 = []
EC50s3 = []
prms2 = []
prms =[]

x, y , z , z2, z3= np.loadtxt(path + os.sep +  nameOfFiles,unpack=True)


# pour enlever les doublons dans X
newX = set(x)

minPrm =min(newX)
maxPrm = max(newX)

print "#"*40
print "Nbre prms = " + str(len(newX))
print "Nbre de points = " + str(len(x))
print "Min value = " + str(minPrm)
print "Max value = " + str(maxPrm)
print "slice = " + str(len(x)/len(newX))
print "#"*40




NbPrmsUsed = len(x)/len(newX)





for iPrm in newX:
	a=[]
	b=[]
	c=[]

	for line in zip (x,y,z):
		if (iPrm == line[0]):
			a.append(line[1])
			b.append(line[2])
			c.append(line[0])

	#for val in zip(a,b, c):
	#	print val
	#print "\n"
	if (max(b) == min(b)):
		print "\t Pas de variation por PRM " + str(iPrm)
		EC50s.append(0)
		prms.append(iPrm)
		pass
	else:

		bNorm = (b - min(b) )/ max(b - min(b))


		try:
			plsqAA, stderAA = EC50(a, bNorm)
			#print "EC50 = " +str(plsqAA[1]) + " nH = " + str(plsqAA[2])+  str(stderAA[1]) + " PRM= " + str(iPrm)

			
			if (stderAA[1] < (plsqAA[1]*threshold)):
				#print str(plsqAA[1]) + "  STDR=  "+ str(stderAA[1]) + " PRM= " + str(iPrm)
				EC50s.append(plsqAA[1])
				prms.append(iPrm)
			else:
				plsqA, stderA= Bi_EC50(a, bNorm)
				
				# check si bon fit ou pas avec les stdr
			
				if (plsqA[4] < plsqA[1]):
					if (stderA[4] < (plsqA[4]*threshold)):
						EC50s2.append(plsqA[4])
						EC50s3.append(plsqA[1])
					else: 
						EC50s2.append(0)
						EC50s3.append(0)
				else:
					if (stderA[1] < (plsqA[1]*threshold)):
						EC50s2.append(plsqA[1])
						EC50s3.append(plsqA[4])	
					else: 
						EC50s2.append(0)
						EC50s3.append(0)

				prms2.append(iPrm)

		except:
			print "pb with "+ str(iPrm)		
			pass
	
	
"""	
print "resultat"

print len(prms)
print len(EC50s)
print len(EC50s2)
"""

	

def sortedData(X, Y):

	data = zip(X,Y)

	numberR={}
	for i in range(len(data)):
		numberR[i]= [float(data[i][0]),  float(data[i][1])]
	# sort according 
	lsrt= sorted(numberR.iteritems(), key=operator.itemgetter(1))


	X_sorted = []
	Y_sorted = []

	#print 'value PRMS and EC50 sorted' 
	for j in range(len(lsrt)):
		#print lsrt[j][1]
		X_sorted.append(lsrt[j][1][0])
		Y_sorted.append(lsrt[j][1][1])

	return X_sorted, Y_sorted

#fit mono
prms_sorted, EC50s_sorted = sortedData(prms, EC50s)
# fit bi 
prms_sorted2, EC50s_sorted2 = sortedData(prms2, EC50s2)
prms_sorted3, EC50s_sorted3 = sortedData(prms2, EC50s3)




Fig = plt.figure(num=None)



# titre du graph
plt.suptitle(graphTitle)

"""
plt.plot(prms, EC50s, '-o', color = 'black')

plt.plot(refX, refY, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))
"""

plt.plot(EC50s_sorted,prms_sorted,  '-o', color = 'black' , label = tagY + ' Fit with S curves')
plt.plot(EC50s_sorted2,prms_sorted2,  '-o', color = 'green', label = tagY + ' Fit with double S curved')
plt.plot(EC50s_sorted3,prms_sorted3,  '-o', color = 'green') #, label = 'Fit with double S curved')


plt.plot(refY, refX, marker = 'x', markersize =15, markeredgewidth = 3,  color = 'red', label= "Initial value " + str(refX))

plt.ylim([maxPrm,minPrm])
plt.semilogx()
plt.semilogy()


plt.legend(loc = "upper left")

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
