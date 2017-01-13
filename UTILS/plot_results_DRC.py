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

path = "./DRC_ACh/"
nameOfFiles = "analysisACh_IP3.txt"
ECICtag = "EC"


# nom du graph de sortie
outName = nameOfFiles[:-4]+"_NORM"
# titre 
graphTitle = "Dose Response Curve with 1mM ACh" 
# label
labelTitle = ""

# X and Y labels
xAxisLabel ="[ACh] (mM)"

yAxisLabel = '[IP3] norm.'

#yAxisLabel =  r'G$\alpha$qGTP norm.' #r'G$\alpha$qGTP $\mu$m$^2$'




data = np.loadtxt(path + nameOfFiles )

dataX = data[:,0]
dataY = data[:,1] / max(data[:,1])



Fig = plt.figure(num=None)



# titre du graph
plt.suptitle(graphTitle)


plt.plot(dataX, dataY, 'o-', color = 'black', label = labelTitle)



plsq = EC50(dataX, dataY)
print "EC50 = " +str(plsq[1]) + " nH = " + str(plsq[2])

plt.gca().annotate(ECICtag+"$_{50}= $ " + str('{:.2e}'.format(plsq[1])) + " mM", xy=(plsq[1], min(dataY) + (max(dataY)-min(dataY))/2))

xaline = np.linspace(min(dataX), plsq[1], 10)
yaline = np.linspace(min(dataY) + (max(dataY)-min(dataY))/2, min(dataY) + (max(dataY)-min(dataY))/2, 10)
plt.plot(xaline, yaline, '--', color = "black")


xbline = np.linspace(plsq[1], plsq[1], 10)
ybline = np.linspace(min(dataY), min(dataY) + (max(dataY)-min(dataY))/2, 10)

plt.plot(xbline, ybline, '--', color = "black")

plt.semilogx()

# label X
plt.xlabel(xAxisLabel)


# label pour axe Y
plt.ylabel(yAxisLabel)

drop_spines(plt.gca())


#plt.tight_layout()

# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")


plt.show()

