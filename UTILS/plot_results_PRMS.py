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

namePRMS = sys.argv[1] # "kf_G1"

out = "Ga_GTP"
out2 = "IP3"

refCsteFile="Cstes.txt"

path = "./batch_"+namePRMS +"/"
nameOfFiles = "analysis"+namePRMS+"_"+out+".txt"
nameOfFiles2 = "analysis"+namePRMS+"_"+out2+".txt"

yAxisLabel = 'Readout norm' #'['+out+'] norm.'


####################################################################################


for line in file(path+refCsteFile, 'r' ):
	(a,b)=line.split(' = ')
	if (a == " " +namePRMS):
			#print "gagne"
		refX = b[:-1]
		break

# nom du graph de sortie
outName = nameOfFiles[:-4]+"_NORM"
# titre 
graphTitle = "" #Dose Response Curve with 1mM ACh" 
# label
labelTitle = ""

# X and Y labels
xAxisLabel =namePRMS+"(unit)"



#yAxisLabel =  r'G$\alpha$qGTP norm.' #r'G$\alpha$qGTP $\mu$m$^2$'



"""
data = np.loadtxt(path + nameOfFiles )

dataX = data[:,0]
dataY = data[:,1] / max(data[:,1])
"""


dataX, dataY = np.loadtxt(path + nameOfFiles,unpack=True)

for i, ivalue in enumerate(dataX):
	if str(ivalue) == str(refX):
		refY = dataY[i] 
		break


dataX2, dataY2 = np.loadtxt(path + nameOfFiles2,unpack=True)

for i2, ivalue2 in enumerate(dataX2):
	if str(ivalue2) == str(refX):
		refY2 = dataY2[i2] 
		break


Fig = plt.figure(num=None)



# titre du graph
plt.suptitle(graphTitle)

"""
plt.plot(dataX, dataY/max(dataY), 'o-', color = 'black',  label = out)
plt.plot(refX, refY/max(dataY), marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))

plt.plot(dataX2, dataY2/max(dataY2), 'o-', color = 'green', label = out2)
plt.plot(refX, refY2/max(dataY2), marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red')
"""


plt.subplot(211)
plt.plot(dataX, dataY/refY, 'o-', color = 'black',  label = out)
plt.plot(refX, refY/refY, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))
plt.legend(loc = 'lower right')
plt.ylabel("Norm by init value")
drop_spines(plt.gca())

plt.subplot(212)
plt.plot(dataX2, dataY2/refY2, 'o-', color = 'green', label = out2)
plt.plot(refX, refY2/refY2, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red')

plt.legend(loc = 'lower right')
plt.ylabel("Norm by init value")
# label X
plt.xlabel(xAxisLabel)


# label pour axe Y
plt.ylabel("Norm by ref value")

drop_spines(plt.gca())


#plt.tight_layout()

# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")


plt.show()

