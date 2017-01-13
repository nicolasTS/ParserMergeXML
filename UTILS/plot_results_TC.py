import numpy as np  
import matplotlib.pyplot as plt
from scipy.optimize import *
import os
import sys
from pylab import *
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

from prms_utils import *

setup_plot_prms()

plt.close("all")


###############################################################################
p = "./Results-2017-01-13_14H48M40S/"
tag = "Ga_GTP"

# titre 
graphTitle = "m1AChR with [ACh] = 1mM during 1sec" #

# label
labelTitle = ""

# X and Y labels
xAxisLabel ="Time (sec)"
yAxisLabel = r'G$\alpha$qGTP $\mu$m$^2$'


##################################################################################

path = p + os.sep + tag + os.sep
nameOfFiles = "Sim0.txt"


# nom du graph de sortie
outName = tag #nameOfFiles[:-4]

#read data
dataX, dataY = np.loadtxt(path + nameOfFiles ,unpack=True)

Fig = plt.figure(num=None)

# titre du graph
plt.suptitle(graphTitle)


plt.plot(dataX*1e-3, dataY, color = 'black', label = labelTitle)


# label X
plt.xlabel(xAxisLabel)


# label pour axe Y
plt.ylabel(yAxisLabel)


drop_spines(plt.gca())



# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")


plt.show()

