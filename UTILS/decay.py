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
yAxisLabel = "sumOpen" #"r'G$\alpha$qGTP $\mu$m$^2$'

#########################################################################################




path= os.path.dirname(fileName)
outName =  os.path.basename(fileName)[:-4]

dataX, dataY = np.loadtxt(fileName, unpack= True)



from pylab import *
from scipy.optimize import curve_fit
"""
#x = np.array([399.75, 989.25, 1578.75, 2168.25, 2757.75, 3347.25, 3936.75, 4526.25, 5115.75, 5705.25])
#y = np.array([109,62,39,13,10,4,2,0,1,2])

def func(x, a, b):
	return a*exp(-x/b)
#   return a*np.exp(-c*(x-b))+d

peak = max(dataY)
timeForPeak = np.argmax(dataY)



dataXcut=dataX[timeForPeak:]
dataYcut=dataY[timeForPeak:]


popt, pcov = curve_fit(func, dataXcut, dataYcut, [peak,max(dataX)])
print popt

plot(dataXcut,dataYcut)
x=linspace(0,100,10)
plot(x,func(x,*popt), "-x")
xlim(0,100)
ylim(0,1)

show()


sys.exit()
"""
peak = max(dataY)
timeForPeak = np.argmax(dataY)

auc=np.trapz(dataY,dataX)


dataXcut=dataX[timeForPeak:]
dataYcut=dataY[timeForPeak:]

def func(x, a, b):
	return a*exp(-x/b)

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

"""   
p0 = [peak,max(dataX)] # initial guesses

pbest = leastsq(residuals,p0,args=(dataYcut,dataXcut),full_output=1)
print 'Decay time fit with mono exp ',pbest[0][1]


p02=[peak,10,10,10]
pbest2 = leastsq(residuals2,p02,args=(dataYcut,dataXcut),full_output=1)
print 'Best fit parameters with bi exp ', pbest2[0]
"""


popt, pcov = curve_fit(func, dataXcut, dataYcut, [peak,max(dataX)])
print popt

print 'AUC ',auc
print "Peak " , peak

graphTitle ="Decay time of  "+ str(round(popt[1], 2)) + " fit with mono exp \n AUC of " + str(round(auc, 2)) + "\nPeak " + str(round(peak,2))

Fig = plt.figure(num=None)

# titre du graph
plt.suptitle(graphTitle)

# plot data 
plt.plot(dataX, dataY, color = 'black', label = "data")

# plot fit
x=linspace(dataX[timeForPeak], max(dataX),len(dataX))
plt.plot(x,func(x,*popt),color = 'red', lw = 4, label ="fit")


plt.ylim(0,max(dataY))

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



