import numpy as np  
import matplotlib.pyplot as plt
from scipy.optimize import *
import glob
from pylab import *
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

from prms_utils import *

setup_plot_prms()

#####################################################################################################################

plt.close("all")

path = sys.argv[1] #"./DRC_Glu_Ref/"
tagX = "ACh"
tagY = "IP3"
nameOfFiles = "analysis"+tagX+"_"+tagY+".txt"
#nameOfFiles = "analysisACh_Ga_GTP.txt"

ECICtag = "EC"


# nom du graph de sortie
outName = nameOfFiles[:-4]+"_NORM"
# titre 
graphTitle = "" #Dose Response Curve with 1mM ACh" 
# label
labelTitle = ""

# X and Y labels
xAxisLabel ="["+tagX +"] (mM)"

yAxisLabel = '['+ tagY+'] norm.'

#yAxisLabel =  r'G$\alpha$qGTP norm.' #r'G$\alpha$qGTP $\mu$m$^2$'

#yAxisLabel =  r'R-ACh binding norm.'



data = np.loadtxt(path + nameOfFiles )

dataX = data[:,0]
dataY = (data[:,1] - min(data[:,1]) )/ max(data[:,1] - min(data[:,1]) )

#dataY = (data[:,1]/ max(data[:,1] ))



Fig = plt.figure(num=None)



# titre du graph
plt.suptitle(graphTitle)


plt.plot(dataX, dataY, 'o-', color = 'black', label = labelTitle)


# fit with simple S curve
plsq, sucess = EC50(dataX, dataY )
#print "EC50 = " +str(plsq[1]) + " nH = " + str(plsq[2])

y = plsq[0] /(1.0+(plsq[1]/dataX)**plsq[2])
plt.plot(dataX,y, '-o', color = "red", label = "S-curved")

if (sucess == 1):
	shift_tag = (plsq[1]*10)/100
	plt.gca().annotate(ECICtag+"$_{50}= $ " + str('{:.2e}'.format(plsq[1])) + " mM", xy=(plsq[1]+shift_tag, min(dataY) + (max(dataY)-min(dataY))/2))

	xaline = np.linspace(min(dataX), plsq[1], 10)
	yaline = np.linspace(min(dataY) + (max(dataY)-min(dataY))/2, min(dataY) + (max(dataY)-min(dataY))/2, 10)
	plt.plot(xaline, yaline, '--', color = "black")

	xbline = np.linspace(plsq[1], plsq[1], 10)
	ybline = np.linspace(min(dataY), min(dataY) + (max(dataY)-min(dataY))/2, 10)
	plt.plot(xbline, ybline, '--', color = "black")

	

# si arrive pas avec simple S curve alors double S curve
else:
	plsqA, sucessA= Bi_EC50(dataX, dataY)
	print plsqA

	shift_tag1 = (plsqA[1]*10)/100
	plt.gca().annotate(ECICtag+"$_{50}= $ " + str('{:.2e}'.format(plsqA[1])) + " mM", xy=(plsqA[1]+shift_tag1, plsqA[0] + (min(dataY) + (plsqA[3]-min(dataY))/2) ))

	xaline = np.linspace(min(dataX), plsqA[1], 10)
	yaline = np.linspace(plsqA[0] + (min(dataY) + (plsqA[3]-min(dataY))/2) , plsqA[0] + (min(dataY) + (plsqA[3]-min(dataY))/2), 10)
	plt.plot(xaline, yaline, '--', color = "black")

	xbline = np.linspace(plsqA[1], plsqA[1], 10)
	ybline = np.linspace(min(dataY), plsqA[0] + (min(dataY) + (plsqA[3]-min(dataY))/2), 10)
	plt.plot(xbline, ybline, '--', color = "black")

	shift_tag2 = (plsqA[4]*10)/100
	plt.gca().annotate(ECICtag+"$_{50}= $ " + str('{:.2e}'.format(plsqA[4])) + " mM", xy=(plsqA[4]+shift_tag2, min(dataY) + (plsqA[3]-min(dataY))/2))
		
	xaline = np.linspace(min(dataX), plsqA[4], 10)
	yaline = np.linspace(min(dataY) + (plsqA[3]-min(dataY))/2, min(dataY) + (plsqA[3]-min(dataY))/2, 10)
	plt.plot(xaline, yaline, '--', color = "black")

	xbline = np.linspace(plsqA[4], plsqA[4], 10)
	ybline = np.linspace(min(dataY), min(dataY) + (plsqA[3]-min(dataY))/2, 10)
	plt.plot(xbline, ybline, '--', color = "black")


	f = (plsqA[0] / (1.0 + ((plsqA[1]/dataX)**plsqA[2])) + (plsqA[3] / (1.0 + (plsqA[4]/dataX)**plsqA[5])))
	plt.plot(dataX,f, '-o', color = "green", label = "Double S-curved")



plt.semilogx()

# label X
plt.xlabel(xAxisLabel)

plt.legend(loc = "upper left")

# label pour axe Y
plt.ylabel(yAxisLabel)

drop_spines(plt.gca())


#plt.tight_layout()

# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")


plt.show()

