import sys, os
import math
import glob
import datetime
from pylab import *
import numpy as np

from scipy.optimize import leastsq
import matplotlib.pyplot as plt

from prms_utils import *

setup_plot_prms()

plt.close("all")


#########################################################################################
fileName = sys.argv[1]

# X and Y labels
xAxisLabel ="Time (msec)"
yAxisLabel = r'G$\alpha$qGTP $\mu$m$^2$'

#########################################################################################


path= os.path.dirname(fileName)
outName =  os.path.basename(fileName)[:-4]

dataX, dataY = np.loadtxt(fileName, unpack= True)

peak = max(dataY)
timeForPeak = np.argmax(dataY)


dataXcut=dataX[timeForPeak:]
dataYcut=dataY[timeForPeak:]

def expl(t,p):
	return(p[0]*exp(-t/p[1]))
	    
def residuals(p,data,t):
	err = data - expl(t,p)
	return err
	    
	    
p0 = [peak,max(dataX)] # initial guesses

pbest = leastsq(residuals,p0,args=(dataYcut,dataXcut),full_output=1)
print 'Decay time with mono exp ',pbest[0][1]

graphTitle ="Decay time of " + str(round(pbest[0][1], 2)) + "with mono exp"

Fig = plt.figure(num=None)

# titre du graph
plt.suptitle(graphTitle)

plt.plot(dataX, dataY, color = 'black', label = "data")


x = np.linspace(dataX[timeForPeak], max(dataX), 100)
f =  expl(x,pbest[0])

plt.plot(x, f ,color = 'red', lw = 4, label ="fit")

plt.legend()

# label X
plt.xlabel(xAxisLabel)

# label pour axe Y
plt.ylabel(yAxisLabel)

drop_spines(plt.gca())


# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+"_FIT.eps", format="eps")
plt.savefig(path + "/1_"+ outName+"_FIT.png", format="png")
plt.savefig(path + "/1_"+ outName+"_FIT.svg", format="svg")


plt.show()



