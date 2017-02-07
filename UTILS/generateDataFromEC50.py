import os
from prms_utils import *

setup_plot_prms()

maxAmp=1.0
EC50=2.90e-4
nH= 1.0

outFiles = "dataGeneratedFromExp.txt"
x = np.logspace(-6,1,30)

y = maxAmp/(1.0+(EC50/x)**nH)



plt.plot(x,y, '-o', color = "red", label = "Exp data")


plt.gca().annotate("$EC_{50}= $ " + str('{:.2e}'.format(EC50)) + " mM", xy=(EC50+1e-3, max(y)/2))

xaline = np.linspace(min(x), EC50, 10)
yaline = np.linspace(max(y)/2, max(y)/2, 10)
plt.plot(xaline, yaline, '--', color = "black")


xbline = np.linspace(EC50, EC50, 10)
ybline = np.linspace(min(y), max(y)/2, 10)
plt.plot(xbline, ybline, '--', color = "black")



plt.semilogx()

plt.xlabel("[Conc]")


plt.ylabel("Response")
plt.legend(loc='lower right')


drop_spines(plt.gca())

plt.show()


if (os.path.exists(outFiles)):
	os.remove(outFiles)
	print "old files deleted"

Results = file(outFiles, 'a')
print>>Results, "# EC50 = " + str(EC50) + " nH = " + str(nH) + " maxAmp = " + str(maxAmp)
for i in range(len(x)):
	print>>Results, x[i], y[i]




