import matplotlib as mpl
import matplotlib.pyplot as plt
from pylab import *
import numpy as np  
from scipy.optimize import *




"""
plt.title(graphTitle, y=1.05) 
"""


######################################################################################
def setup_plot_prms(): 
	fsize = 28
	lwidth = 3
	legend_size = fsize/2

	
	mpl.rcParams['figure.dpi'] = 80.0
	mpl.rcParams['figure.figsize'] = [20,10]
	mpl.rcParams['figure.facecolor']= 'w'
	mpl.rcParams['figure.edgecolor']='k'

	mpl.rcParams['lines.linewidth'] = lwidth
	mpl.rcParams['font.size'] = fsize
	mpl.rcParams['axes.grid'] = 'False'

	
	# xticks
	mpl.rcParams['xtick.minor.visible'] = 'True'
	mpl.rcParams['xtick.minor.size'] = 4
	mpl.rcParams['xtick.minor.width'] = lwidth

	mpl.rcParams['xtick.major.width'] = lwidth
	mpl.rcParams['xtick.major.size'] = 7
	mpl.rcParams['xtick.labelsize'] = fsize
	#yticks
	mpl.rcParams['ytick.minor.visible'] = 'True'
	mpl.rcParams['ytick.minor.size'] = 4
	mpl.rcParams['ytick.minor.width'] = lwidth

	mpl.rcParams['ytick.major.width'] = lwidth
	mpl.rcParams['ytick.major.size'] = 7
	mpl.rcParams['ytick.labelsize'] = fsize

	mpl.rcParams['axes.linewidth'] =  lwidth
#	mpl.rcParams['axes.spines.top'] = 'False'
#	mpl.rcParams['axes.spines.right'] = 'False'
	mpl.rcParams['legend.fontsize'] = legend_size

	
	mpl.rcParams['legend.loc'] = 'upper right'
	mpl.rcParams['legend.fancybox'] = True
	#mpl.rcParams['legend.scatterpoints'] = 1
	mpl.rcParams['legend.frameon'] = False

	# ajuste automatiquement les espaces entre les axes dans la figure
	mpl.rcParams['figure.autolayout'] =  True

################################################################################################################
def drop_spines(ax) :
	for loc, spine in ax.spines.items():
		if loc in ['left','bottom']:
			spine.set_position(('outward',10)) # outward by 10 points
		elif loc in ['right','top']:
			spine.set_color('none') # don't draw spine
		else:
			raise ValueError('unknown spine location: %s'%loc)
	ax.xaxis.set_ticks_position('bottom')
	ax.yaxis.set_ticks_position('left')



######################################################################################################
def isSorted(x):
	if all(x[i] <= x[i+1] for i in range(len(x)-1)):return True
	else: return False

def NRMSD(x1,y1,x2,y2):
	# test if x's lists are creasing
	if(not isSorted(x1) or not isSorted(x2)):
		print "x lists must be creasing"
		return None
	# test if x's and y's have the same sizes
	if(len(x1)!=len(y1) or len(x2)!=len(y2)):
		print "x and y lists must have the same sizes"
		return -1
	# rename x's and y's, considering their sizes
	if(len(x1) < len(x2)):
		xp = x1
		yp = y1
		xg = x2
		yg = y2
	else:
		xp = x2
		yp = y2
		xg = x1
		yg = y1
	del(x1,y1,x2,y2)

	# xp[0] must be greater than xg[0]
	while xp[0]<xg[0]:
		xp = xp[1:]
		yp = yp[1:]
	# xp($) must be smaller than xg($)
	while xg[len(xg)-1]<xp[len(xp)-1]:
		xp = xp[0:len(xp)-2]
		yp = yp[0:len(yp)-2]

	# create interpolated values for the smallest y array
	ygi = zeros(len(xp), dtype = 'float64')
	if len(xp)!=len(xg):
#		print "vector length are different : interpolation"
#		sys.stdout.flush()
		for i in range(len(xp)):
			j = 0
			while xg[j]<xp[i] : j=j+1
			if xg[j]==xp[i]:
				ygi[i] = yg[j]
			else:
				ygi[i] = yg[j-1] + (yg[j]-yg[j-1])/(xg[j]-xg[j-1]) * (xp[i] - xg[j-1])
	else:
#		print "vector sizes are equal : no interpolation"
#		sys.stdout.flush()
		ygi = yg

	# compute the MSE
	MSE=0
	for i in range(len(xp)):
		MSE += (yp[i] - ygi[i])**2  / len(xp)
	RMSD = sqrt(MSE);
	NRMSD = RMSD / ( max(ygi) - min(ygi) );
	del(xp,yp,xg,yg,ygi)
	return NRMSD; 


########################################################################################################################################
def EC50(dataX, dataY):
	normMin = min(dataY)
	if(normMin >= 0):
		dataY = dataY - normMin
		normMax = max(dataY)
		dataY = dataY/normMax
	else:
		normMax = max(dataY)
		dataY = dataY - normMax
		normMin2 = min(dataY)
		dataY = dataY/normMin2

	### FIT + EC50

	peval1 = lambda p,x : p[0]/(1.0+(p[1]/x)**p[2])
	residu1 = lambda p,x,y : peval1(p,x) - y

	peval2 = lambda p,x : p[0]/(1.0+(x/p[1])**p[2])
	residu2 = lambda p,x,y : peval2(p,x) - y

	p0 = [1.0,1.0,1.0]

	if(dataY[0] > dataY[len(dataY)-1]):
		plsq,sucess = leastsq(residu2,p0,args=(array(dataX),array(dataY)),maxfev=5000)


	if(dataY[len(dataY)-1] > dataY[0]):
		plsq,sucess = leastsq(residu1,p0,args=(array(dataX),array(dataY)),maxfev=5000)
	
	return plsq


