#!/usr/bin/python
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.mlab import griddata
from matplotlib.colors import LogNorm
import matplotlib as M



import matplotlib.pyplot as plt
import numpy as np
import os
import sys

import pylab

from prms_utils import *

setup_plot_prms()

###############################################################################################################
tag = str(sys.argv[1]) #"k_reconst"
# valeurs de ref PRMS / output
refX = float(sys.argv[2]) #0.001 #3.02 #0.0255 #3.02 
# a = peak b = 	auc, c = decay
colDataToPlot = str(sys.argv[3])


path ="batch_" + tag 
files = "analysis_PRMS_ACh_IP3.txt"


step = 4


#listOption = ["peak", "auc", "decay"]
#if str(colDataToPlot) 

graphTitle ="" 
# X and Y labels
xAxisLabel = tag #"PRMS"
yAxisLabel = "[ACh] (mM)"
zAxisLabel = colDataToPlot + " [IP3] ()" #"Peak"

###############################################################################################################


outName = files[:-4] + '_' +colDataToPlot



x, y , a, b, c = np.loadtxt(path + os.sep +  files,unpack=True)


# range PRMS et GLU utilse pour faire les simu
tmp_interA= ('{:.2e}'.format(min(x))).split('e')[1]
tmp_interB= ('{:.2e}'.format(max(x))).split('e')[1]
xi = np.logspace(int(tmp_interA),int(tmp_interB),20*step) 

tmp_interAY= ('{:.2e}'.format(min(y))).split('e')[1]
tmp_interBY= ('{:.2e}'.format(max(y))).split('e')[1]
yi = np.logspace(int(tmp_interAY),int(tmp_interBY),20*step) 



if (colDataToPlot == "peak"):
	#print colDataToPlot
	z= a 
if (colDataToPlot == "auc"):
	z = b
if (colDataToPlot == "decay"):

	for idecay in range(len(c)):
		#if (c[idecay] == 666.0):
		print "pb fit decay"
		index = np.argwhere(c==666.0)
		c = np.delete(c, index)
		x = np.delete(x, index)
		y = np.delete(y, index)
		a = np.delete(a, index)
		b = np.delete(b, index)


			#sys.exit()
	z = c
	

###############################################################################################################
# contour
###

#Through the unstructured data get the structured data by interpolation
#zi = griddata(x, y, z, xi,yi) #, interp='cubic') #interp='nn') linear

zi = griddata(y, x, z, yi,xi, interp='linear') #interp='nn') linear




fig = plt.figure()
ax = fig.gca()

plt.suptitle(graphTitle)

"""
CS = plt.contour(xi,yi,zi,10,linewidths=1,colors='black')
CS = plt.contourf(xi,yi,zi,10,cmap=plt.cm.jet,  vmax=abs(zi).max(), vmin=-abs(zi).max()) 

plt.plot(refX, refY, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'black', label= "Initial value " + str(refX))
"""
CS = plt.contour(yi,xi,zi,10,linewidths=1,colors='black')
CS = plt.contourf(yi,xi,zi,10,cmap=plt.cm.jet,  vmax=abs(zi).max(), vmin=-abs(zi).max()) 


xaline = np.linspace(min(yi), max(yi), 10)
yaline = np.linspace(refX, refX, 10) 
plt.plot(xaline, yaline, lw = 5,  color = 'black')

#plt.plot(refY, refX, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'black', label= "Initial value " + str(refX))

cbar = plt.colorbar(CS)

#CS.set_clim(0, 0.1)


drop_spines(plt.gca())




ax.set_xlabel(yAxisLabel) 
ax.set_ylabel(xAxisLabel)
cbar.ax.set_ylabel(zAxisLabel)


ax.set_xscale('log')
ax.set_yscale('log')

# sauvegarde en differents formats
plt.savefig(path + "/1_"+ outName+".eps", format="eps")
plt.savefig(path + "/1_"+ outName+".png", format="png")
plt.savefig(path + "/1_"+ outName+".svg", format="svg")


plt.show()


"""
#Through the unstructured data get the structured data by interpolation
xi = np.linspace(x.min(), x.max(), 200)
yi = np.linspace(y.min(), y.max(),  200)
zi = griddata(x, y, z, xi,yi, interp='linear') #interp='nn')

fig = plt.figure()
ax = fig.gca(projection='3d')

xim, yim = np.meshgrid(xi, yi)
surf = ax.plot_surface(xim, yim, zi,  cmap=plt.cm.jet, cstride=1, rstride=1,linewidth=0,antialiased=False)

fig.colorbar(surf, shrink=0.5, aspect=5) 
ax.set_zlim(z.min(), z.max())

#ax.set_xlim3d([1, 3])




#ax.xaxis.set_major_locator(pylab.MultipleLocator(2))

ax.ticklabel_format(axis='x', style='sci', scilimits=(-6,1))


zticks = np.unique(x) 
print zticks
ax.set_xticklabels(zticks,  rotation=25)


#ax.xticks((1, 5, 9), ('start', 'middle', 'end'), rotation25)
#ax.xaxis.set_major_formatter(FormatStrFormatter().set_powerlimits(-5,5))

plt.show()
"""

























#Plot the contour mapping and edit the parameter setting according to your data (http://matplotlib.org/api/pyplot_api.html?highlight=contourf#matplotlib.pyplot.contourf)
#CS = plt.contourf(xi, yi, zi, 5,vmax=abs(zi).max(), vmin=-abs(zi).max())


#CS = plt.contourf(xi, yi, zi, 5, cmap=plt.cm.jet, norm=log_norm, levels=levels) #,  origin='lower')
#plt.pcolormesh(xi, yi, zi,  cmap = plt.get_cmap('jet')), 


"""
CS = plt.contourf(X, Y, Z, 5,cmap=plt.cm.jet, c) #,  origin='lower')

cbar = plt.colorbar(CS,shrink=0.9)
cbar.ax.set_ylabel('max GaGTP')



plt.xlabel('[ACh] (mM)')
plt.ylabel('[Ant] (mM)')

plt.clabel(CS, fmt='%0.5f', colors='black', fontsize=14)

plt.ylim(0, 10)
"""

#CS = plt.contour(xi, yi,zi, 5 , linestyles='dashed',linewidths = 1.0, colors = 'black', vmax=abs(zi).max(), vmin=-abs(zi).max(), extent=(-3,3,-3,3))

#plt.pcolormesh(xi, yi, zi,  cmap = plt.get_cmap('jet')), 
#plt.ylim(0, 10)

#plt.colorbar(orientation='vertical', shrink=0.8) 
#plt.clabel(CS, fmt='%0.5f', colors='black', fontsize=14)

#plt.scatter(x, y, marker = 'o', c = 'b', s = 10, zorder = 10)

"""
xi = np.linspace(min(x), max(x))
yi = np.linspace(min(y), max(y))

X, Y = np.meshgrid(xi, yi)
Z = griddata(x, y, z, xi, yi, interp='linear')


fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=5, cstride=5, cmap=cm.jet,
                       linewidth=1, antialiased=True)

ax.set_zlim3d(np.min(Z), np.max(Z))
fig.colorbar(surf)
"""

"""
X = np.linspace(1,len(data[:,0]),len(data[:,0])) # data[:,0]
Y =  np.linspace(1,len(data[:,1]),len(data[:,1]))


Z = data[:,2]



X, Y = np.meshgrid(X, Y)


Z = []
i = 0
for x in range(len(X)):
	Z.append([])
	for y in range(len(Y)):
		Z[-1].append(data[x,2])
		i+=1


#print Z

#sys.exit()


fig = plt.figure()
ax = fig.gca(projection='3d') #projection='3d'

#CS = plt.contourf(X, Y, Z, cmap=cm.jet)


surf = ax.plot_surface(X, Y, Z, cmap='rainbow',cstride=1, rstride=1,linewidth=0,antialiased=False)
#surf = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
#surf = ax.plot_wireframe(X, Y, Z)
#surf = ax.plot_trisurf(X, Y, Z, cmap=cm.jet, linewidth=0.2)

#fig.colorbar(surf)

#ax.set_xscale('log')
#ax.set_yscale('log')

#ax.semilogx()

#ax.xaxis.set_scale('log')
#ax.yaxis.set_scale('log')
"""

"""
CS = ax.plot_surface(X,Y,Z,  rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(0, 10e-4)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(CS, shrink=0.5, aspect=5)
"""
"""
ax.set_yscale('symlog')
#
ax.set_xscale('symlog')

plt.colorbar(CS) #, shrink=0.5, aspect=25,format='%1.2f')

"""

"""
enablelog = True

snr=15
fig = plt.figure(figsize=(12,12))
ax = fig.gca(projection='3d')

realsnr = 10**(snr/10)
B,T = np.mgrid[100e3:10e6:100e3, 1:60:1]
C = .55 / (np.sqrt(2) * B * np.sqrt(B * T * realsnr) )
if enablelog: C = np.log10(C)
surf = ax.plot_surface(
    B/1e6, T, C, cmap='rainbow',cstride=1,
    rstride=1,linewidth=0,antialiased=False)
ax.set_xlabel("Bandwidth MHz")
ax.set_ylabel("Integration Time")
ax.set_zlabel("Cramer-Rao Lower Bound")
if enablelog:zticks = [1e-13,1e-12,1e-11,1e-10,1e-9]
if enablelog:ax.set_zticks(np.log10(zticks))
if enablelog:ax.set_zticklabels(zticks)
plt.show()
"""



