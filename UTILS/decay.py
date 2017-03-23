import sys, os
import math
import glob
import datetime
from pylab import *
import numpy as np

from scipy.optimize import leastsq
from scipy.optimize import curve_fit

import matplotlib.pyplot as plt

from prms_utils import *

setup_plot_prms()

plt.close("all")


#########################################################################################
fileName = sys.argv[1]

# X and Y labels
xAxisLabel ="Time (msec)"
yAxisLabel = "sumOpen" #"r'G$\alpha$qGTP $\mu$m$^2$'

#########################################################################################




path= os.path.dirname(fileName)
outName =  os.path.basename(fileName)[:-4]

dataX, dataY = np.loadtxt(fileName, unpack= True)


peak = max(dataY)
timeForPeak = np.argmax(dataY)

auc=np.trapz(dataY,dataX)


dataXcut=dataX[timeForPeak:]
dataYcut=dataY[timeForPeak:]

def func(x, a, b):
	return (a*exp(-x/b))

def func2(x, a,b,c,d):
	return (a*exp(-x/b) + c*exp(-x/d))

def expl(t,p):
	return(p[0]*exp(-t/p[1]))
	    
def residuals(p,data,t):
	err = data - expl(t,p)
	return err
	    
def dbexpl2(t,p):
	    return(p[0]*exp(-t/p[1]) + p[2]*exp(-t/p[3]))

def residuals2(p,data,t):
	    err = data - dbexpl2(t,p)
	    return err



popt, pcov = curve_fit(func, dataXcut, dataYcut, [peak,max(dataX)])
print "FIT MonoExp ", popt

popt2, pcov2 = curve_fit(func2, dataXcut, dataYcut, [peak,max(dataX), peak,max(dataX)], maxfev = 100000)
print "FIT2 BiExp", popt2


print 'AUC ',auc
print "Peak " , peak

graphTitle ="Decay time of  "+ str(round(popt2[1], 2)) + " fit with Bi exp \n AUC of " + str(round(auc, 2)) + "\nPeak " + str(round(peak,2))

Fig = plt.figure(num=None)

# titre du graph
plt.suptitle(graphTitle)

# plot data 
plt.plot(dataX, dataY, color = 'black', label = "data")

# plot fit
x=linspace(dataX[timeForPeak], max(dataX),len(dataX))
plt.plot(x,func(x,*popt),color = 'red', lw = 4, label ="fit Mono")
plt.plot(x,func2(x,*popt2),color = 'green', lw = 4, label ="fit Bi")



plt.ylim(0,max(dataY))

#plt.xlim(0,100)

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



