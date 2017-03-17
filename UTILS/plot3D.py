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

path ="batch_kass_re1"
files = "analysis_PRMS_Glu_sumOpen.txt"

# valeurs de ref PRMS / output
refX = 10.0
refY = 0.486434368805

# range PRMS et GLU utilse pour faire les simu
xi = np.logspace(-3,4,200) #np.linspace(x.min(), x.max(), 200)
yi = np.logspace(-3,3,200) #np.linspace(y.min(), y.max(),  200)

# X and Y labels
xAxisLabel = "PRMS"
yAxisLabel = "[Glu] (mM)"
zAxisLabel = "sumOpen"

###############################################################################################################


outName = files[:-4]

graphTitle ="" #"with [ACh] = 10 mM"

x, y , z = np.loadtxt(path + os.sep +  files,unpack=True)

###############################################################################################################
# contour
###

"""
# range PRMS et GLU utilse pour faire les simu
xi = np.logspace(-3,3,200) #np.linspace(x.min(), x.max(), 200)
yi = np.logspace(-3,2,200) #np.linspace(y.min(), y.max(),  200)
"""

#Through the unstructured data get the structured data by interpolation
zi = griddata(x, y, z, xi,yi, interp='linear') #interp='nn')


fig = plt.figure()
ax = fig.gca()

plt.suptitle(graphTitle)


CS = plt.contour(xi,yi,zi,10,linewidths=1,colors='black')
CS = plt.contourf(xi,yi,zi,10,cmap=plt.cm.jet,  vmax=abs(zi).max(), vmin=-abs(zi).max()) 

plt.plot(refX, refY, marker = 'x', markersize =20, markeredgewidth = 5,  color = 'red', label= "Initial value " + str(refX))

cbar = plt.colorbar(CS)


#CS.set_clim(0, 1.0)

drop_spines(plt.gca())




ax.set_xlabel(xAxisLabel) 
ax.set_ylabel(yAxisLabel)
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



