# -*- coding: utf-8 -*-
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import sys
import time
import os
import os.path
from libsbml import *
import pickle
#from function import *


# les prms cinetiques doivent etre different
# connections avec les etats qui sont identiques



##########################################################verifier si prm est cst ou pas !!


#get all assig
# recuperation en 1ier pour apres trier la liste des parametres cinetiques cad constant[] et assignement[]
def getAllAssig(listeModels):
	listeNamesAssig = []
	listeValuesAssig = []

	for iModels in listeModels:
		for i in range(iModels.getNumRules()):

			# necessaire a cause des ( et ) afin d avoir un espace entre!
			a = iModels.getRule(i).getFormula()
			tmp = a.replace('(',' ( ')
			tmp2 = tmp.replace(')',' ) ')
		

			listeNamesAssig.append(" " + iModels.getRule(i).getVariable()+ " ")
			listeValuesAssig.append(" "+ tmp2 + " ")
		

	return listeNamesAssig, listeValuesAssig



# get all Kinetics Parameters
def getAllKineticsParameters(listeModels):
	listeNamesKineticsParameters=[]
	listeValuesKineticsParameters=[]
	# names et values des assign
	listeNamesAssig, listeValuesAssig = getAllAssig(listeModels)
	# names et values des kinetics parameters dans des listes
	for iModels in listeModels:
		for i in range(iModels.getNumParameters()):
			listeNamesKineticsParameters.append(" " + iModels.getParameter(i).getId()+ " ")
			listeValuesKineticsParameters.append(iModels.getParameter(i).getValue())

	# suppression des assign de la liste des prm cinetiques
	for nAssign in listeNamesAssig:
		for i, n in enumerate(listeNamesKineticsParameters):
			if (n == nAssign):
				#print "trouvé " + str(n) + " position " + str(i)
				del listeNamesKineticsParameters[i]
				del listeValuesKineticsParameters[i]
		
	return listeNamesKineticsParameters, listeValuesKineticsParameters


# get all Species
def getAllSpecies(listeModels):
    	dicoSpecies={}
	dicoBondaries = {}
	for iModels in listeModels:
		for i in range(iModels.getNumSpecies()):
			if not (iModels.getSpecies(i).getBoundaryCondition()):
				dicoSpecies[" " + iModels.getSpecies(i).getName()+ " "] = iModels.getSpecies(i).getInitialAmount()
			else:
				dicoBondaries[iModels.getSpecies(i).getName()] = iModels.getSpecies(i).getInitialAmount()
			
    	return dicoSpecies, dicoBondaries





# get All Reactions
def getAllReactions(listeModels):
	listeAllReactions = []
	for iModels in listeModels:
		for i in range(iModels.getNumReactions()):
			listeAllReactions.append(iModels.getReaction(i))

	return listeAllReactions


#get all asign indexed
def getAllAssignIndexed(listeNamesAssig, listeValuesAssig,dicoSpecies, listeKineticsParameters ):
	listeNamesAsignIndexed = []
	listeReactAsignIndexed = []

	for index, (iNameAssign,iReactAssign)  in enumerate(zip(listeNamesAssig, listeValuesAssig)):

		#print iReactAssign
		r = iReactAssign
		# indexation des prms cinetiques
		for i, iParameter in enumerate(listeKineticsParameters):
		    	try:
		        	while iParameter in r:
		        	    	indexParameterInReaction = r.index(iParameter)
		        	    	temp2=r[0:indexParameterInReaction]+" constants["+str(i)+"] "+r[indexParameterInReaction+len(iParameter):]
		        	    	r=temp2
		    	except:
		        	pass
		# indexation des species
		for i, iSpecie in enumerate(dicoSpecies):
			try:
		            while iSpecie in r:
		                indexSpeciesInReaction = r.index(iSpecie)
		                temp=r[0:indexSpeciesInReaction]+" X["+str(i)+"] "+r[indexSpeciesInReaction+len(iSpecie):]
				r=temp
				#print r

		        except:
		            pass
		
		#indexation des assign car un assign peut contenir un autre assign
		for i, tNameAssign in enumerate(listeNamesAssig):
			#print t + " " + str(len(tNameAssign))
		 
			try:
		            while tNameAssign in r:
		                indexSpeciesInReaction = r.index(tNameAssign)
		                temp=r[0:indexSpeciesInReaction]+" assignments["+str(i)+"] "+r[indexSpeciesInReaction+len(tNameAssign):]
				r=temp
				#print r

		        except:
		            pass
					

		listeReactAsignIndexed.append(r)
		listeNamesAsignIndexed.append(iNameAssign)

		

	return listeNamesAsignIndexed, listeReactAsignIndexed

# get all partial equzations
def getAllPartialEquationsIndexed(listeReactions, listeSpecies, listeKineticsParameters, listeAssignements): 
	listeR = []
	listeReactionsIndexer=[]
	for iReaction in listeReactions:
		r = " " + str(iReaction.getKineticLaw().getFormula()) + " "
		#print r
		listeR.append(r)
		# indexation des species
		for i, iSpecie in enumerate(listeSpecies):
			try:
		            while iSpecie in r:
		                indexSpeciesInReaction = r.index(iSpecie)
		                temp=r[0:indexSpeciesInReaction]+" X["+str(i)+"] "+r[indexSpeciesInReaction+len(iSpecie):]
				r=temp
				#print r

		        except:
		            pass

		# indexation des prms cinetiques
		for i, iParameter in enumerate(listeKineticsParameters):
		    	try:
		        	while iParameter in r:
		        	    	indexParameterInReaction = r.index(iParameter)
		        	    	temp2=r[0:indexParameterInReaction]+" constants["+str(i)+"] "+r[indexParameterInReaction+len(iParameter):]
		        	    	r=temp2
		    	except:
		        	pass
	

		for i , iAssign in enumerate(listeAssignements):
			#print iAssign
			try:
				while iAssign in r:
					indexAssignInReaction = r.index(iAssign)
					temp3 = r[0:indexAssignInReaction]+" assignments["+str(i)+"] "+r[indexAssignInReaction+len(iAssign):]
		        	    	r=temp3
					#print r
		    	except:
		        	pass

		listeReactionsIndexer.append(r)

	return listeR, listeReactionsIndexer

# get all Global Equations
def getGlobalEquations(listeReactions, listeSpecies):

	 # On Recupere les reactions Negatives 
	RES = ""
	RES3 = [] 
	RRES3 = [] 
	    
	RES2=""
	 # On Recupere les reactions positives 
	RRES = ""
	RRES3 = []    
	RRES2=""  


	for iSpecie in listeSpecies:
		for i, iReact in enumerate(listeReactions):

			for j in range(iReact.getNumReactants()):
				react = " " + iReact.getReactant(j).getSpecies() + " "
				#print react
				if (iSpecie in react):
					RES = " - R" + str(i)
					#print RES
					
			RES2=RES2+RES
		    	RES=""  

			for j in range(iReact.getNumProducts()):
		        	prod = " " + iReact.getProduct(j).getSpecies() + " "
		        	if (iSpecie in prod):
		          		RRES = " + R" + str(i)

			RRES2=RRES2+RRES
			RRES="" 
	   
		RRES3.append(str(RRES2))		
		RRES2=""   
		RES3.append(str(RES2))
		RES2="" 



	Rtot=[]
	for i in range(len(listeSpecies)):
		Rtot.append(RRES3[i]+RES3[i])
	 #       print("\tXdot["+str(i)+"] ="+Rtot[i]+" \t\t\t "+"# d"+str(listeSpecies[i][1:-1])+"\n")

	#print "GlobalEquations: "+str(Rtot)    

	
	return Rtot








# write ODE system
def writeODESystem(listeModels, merge_params, simu_params):

    writePythonFolder = merge_params['outDirectory']

    timePulse = simu_params['timePulse']
    valuePulse = simu_params['valuePulse']
    namePulse =simu_params['namePulse']


    listeNamesKineticsParameters, listeValuesKineticsParameters= getAllKineticsParameters(listeModels)
    listeNamesAssig, listeValuesAssig  = getAllAssig(listeModels)

    dicoSpecies, dicoBondaries = getAllSpecies(listeModels)
    print "BONDARIES "
    print dicoBondaries.keys()
    listeNamesAssignIndexer, listeReactAssignIndexer= getAllAssignIndexed(listeNamesAssig, listeValuesAssig,dicoSpecies.keys(), listeNamesKineticsParameters )
    listeReactions = getAllReactions(listeModels)
    listeR, listeReactionsIndexer = getAllPartialEquationsIndexed(listeReactions, dicoSpecies.keys(),listeNamesKineticsParameters,listeNamesAssig )
    globalEq = getGlobalEquations(listeReactions, dicoSpecies.keys())



    with open(writePythonFolder+os.sep + "ODESystems.py","w") as monFichier:
        monFichier.write("try:\n")
        monFichier.write("\tfrom pysundials import cvode\n")
        monFichier.write("except ImportError:\n")
        monFichier.write("\timport cvode\n\n")
        monFichier.write("import ctypes\n")
        monFichier.write("from numpy import *\n")
        monFichier.write("from scipy import *\n")
        monFichier.write("from pylab import *\n")
	monFichier.write("import os\n")
	monFichier.write("import sys\n")
        monFichier.write("import time\n\n\n\n")
        
  	monFichier.write("# import parameters file \n")
	monFichier.write("paramfilepath = sys.argv[1] \n")
	monFichier.write('exec("')
	monFichier.write('from "+paramfilepath.rstrip(".py")+" import *") \n\n')

	# nombre de prm cinetique
        monFichier.write("constants = cvode.NVector(zeros("+str(len(listeNamesKineticsParameters))+"))\n")
	# nombre de species
        monFichier.write("X = cvode.NVector(zeros("+str(len(dicoSpecies.keys()))+"))\n")

	if(len(listeNamesAssig) == 0):
		monFichier.write("assignments = cvode.NVector(zeros("+str(1) +"))\n")
	else :
	        monFichier.write("assignments = cvode.NVector(zeros("+str(len(listeNamesAssig)) +"))\n")
	# nombre d events = nombre de bondaries
        monFichier.write("events = cvode.NVector(zeros("+ str(len(dicoBondaries.keys())) +"))\n\n")
        monFichier.write("t = cvode.realtype(0.0)\n\n\n\n")
        
        monFichier.write("# BOUNDARY CONDITION\n")
        monFichier.write("########################################################\n\n")
	
	iEvent = 0
	for iName in namePulse:
		monFichier.write('events[' + str(iEvent) + '] = ' + str(dicoBondaries[iName]) + "  # " + str(iName) + "\n")
		iEvent+=1

	monFichier.write("\n\n\n# KINETICS PARAMETERS\n")
        monFichier.write("########################################################\n\n")
     
#	for i, (k, v) in enumerate(zip(listeNamesKineticsParameters, listeValuesKineticsParameters)):
#		monFichier.write('constants[' + str(i) + '] = ' + str(v) + "  # " + str(k) + "\n")
	
	f = open(merge_params['outCsteFile'],'w')
	for (k, v) in zip(listeNamesKineticsParameters, listeValuesKineticsParameters):
		f.write(str(k) + "= " + str(v) + "\n")

	monFichier.write("for i, line in enumerate(file(simu_params['inCsteFile'], 'r' )):\n")
	monFichier.write("\t(a,b)=line.split(' = ')\n")
	monFichier.write("\tconstants[i] = float(b)\n")


 	monFichier.write("\n\n\n# SPECIES: INITIAL CONDITION\n")
        monFichier.write("########################################################\n\n")
        
        i = 0
	for k, v in dicoSpecies.iteritems():
		monFichier.write('X[' + str(i) + '] = ' + str(v) + "  # " + str(k) + "\n")
		i+=1


	monFichier.write("\n\n\n# ASSIGNEMENTS\n")
	for i, (k, v) in enumerate(zip(listeNamesAssignIndexer, listeReactAssignIndexer)):
		monFichier.write('assignments[' + str(i) + '] = ' + str(v) + "  # " + str(k) + "\n")	


        monFichier.write("\n\n\n# GLOBAL EQUATIONS\n")
        monFichier.write("########################################################\n\n")
        monFichier.write("def f(t, X, Xdot, f_data):\n\n")



	iEvent = 0
	for iName in namePulse:
		monFichier.write('\t'+iName + ' = events['+str(iEvent)+ "]\n")
		iEvent+=1

	monFichier.write('\n')

	for i, iReact in enumerate(listeReactionsIndexer):
		monFichier.write('\t# R' + str(i) + ' = ' + str(listeR[i]) + "\n")
		monFichier.write('\tR' + str(i) + ' = ' + str(iReact) + "\n")

	for i, iGlobalEq in enumerate(globalEq):
		monFichier.write('\tXdot[' + str(i) +'] = ' + iGlobalEq + "\n")

 	monFichier.write("\treturn 0\n\n\n")
        
	monFichier.write("\n\n\n# EVENTS\n")
        monFichier.write("def update_assign(t):\n\n")

	for i, (k, v) in enumerate(zip(listeNamesAssignIndexer, listeReactAssignIndexer)):
		monFichier.write('\tassignments[' + str(i) + '] = ' + str(v) + "  # " + str(k) + "\n") 


	for i, iName in enumerate(namePulse):
		monFichier.write('\t#'+iName + ' = 0'+ "\n")
		monFichier.write('\tevents[' + str(i) + '] = 0'+ "\n")	
	monFichier.write("\treturn 0\n\n\n")

   	
	monFichier.write("def g(t, X, gout, g_data):\n\n")
	for i in range(len(timePulse)):
        	#monFichier.write("\tgout["+ str(i) + "] = (t  - (" + 10.0)) * (t  - ( 11.0))\n")
        	#monFichier.write("\tgout["+ str(i) + "] = (t  - (" + str(timePulse[i][0]) +")) * (t  - ("+ str(timePulse[i][1]) +"))\n")

        	monFichier.write("\tgout["+ str(i) + "] = (t  - (" + "simu_params['timePulse']["+str(i)+"][0])" +") * (t  - ("+"simu_params['timePulse'][" +str(i)+"][1])" +")\n")


        monFichier.write("\treturn 0\n\n\n")

        monFichier.write("def update_rootsfound(rootsfound,t,reltol,abstol,cvode_mem):\n\n")
	
	for i in range(len(valuePulse)):
		monFichier.write("\tif(rootsfound[" + str(i) +"] != 0):\n")
		#monFichier.write("\t\tevents[" + str(i) + "] = " +str(valuePulse[i]) + "\n")
		monFichier.write("\t\tevents[" + str(i) + "] = simu_params['valuePulse'][" +str(i) + "] \n")
		monFichier.write("\t\tcvode.CVodeReInit(cvode_mem, f,t.value, X, cvode.CV_SS, reltol, abstol)\n")
	monFichier.write("\treturn 0\n\n\n")

	
	monFichier.write("def update_events(t):\n\n")
	for i in range(len(timePulse)):
		monFichier.write("\tif(not(t.value < " +"simu_params['timePulse'][" +str(i)+"][0]"+ " or t.value > " + "simu_params['timePulse'][" +str(i)+"][1]" +")):\n")
		monFichier.write("\t\tevents[" + str(i) + "] = simu_params['valuePulse'][" +str(i) + "] \n")
		#monFichier.write("\t\tevents[" + str(i) + "] = "  +str(valuePulse[i]) + "\n")
	monFichier.write("\treturn 0\n\n\n")
	
    monFichier.close()
    return 0


# write Simulator COre

def writeSimulatorCore(listeModels, merge_params, simu_params):

    writePythonFolder = merge_params['outDirectory']

    simuDuration = simu_params['tstop']
    nameSaveY = simu_params['nameSaveY']
    nameSaveAssig = simu_params['nameSaveAssig']
    nameSaveEvents = simu_params['nameSaveEvents']
    namePulse =simu_params['namePulse']


    listeNamesKineticsParameters, listeValuesKineticsParameters= getAllKineticsParameters(listeModels)
    listeNamesAssig, listeValuesAssig = getAllAssig(listeModels)

    dicoSpecies, dicoBondaries = getAllSpecies(listeModels)
    listeNamesAssignIndexer, listeReactAssignIndexer= getAllAssignIndexed(listeNamesAssig, listeValuesAssig,dicoSpecies.keys(), listeNamesKineticsParameters )
  

    with open(writePythonFolder+os.sep + "SimulatoreCore.py","w") as monFichier:
        monFichier.write("try:\n")
        monFichier.write("\tfrom pysundials import cvode\n")
        monFichier.write("except ImportError:\n")
        monFichier.write("\timport cvode\n\n")
        monFichier.write("import ctypes\n")
	#evite les pbs avec matplotlibrc
	monFichier.write("import matplotlib\n")
	monFichier.write("matplotlib.use('agg') \n")
        monFichier.write("import numpy as np  # NumPy (multidimensional arrays, linear algebra, ...)\n")
        monFichier.write("import scipy as sp  # SciPy (signal and image processing library)\n")
        monFichier.write("import matplotlib.pyplot as plt  # Matplotlib's pyplot: MATLAB-like syntax\n")
        monFichier.write("import time\n")
        monFichier.write("import os\n")
        monFichier.write("import sys\n")
        monFichier.write("from ODESystems import *\n")
	monFichier.write("from SaveData import *\n\n")
	
        monFichier.write("# import parameters file \n")
	monFichier.write("paramfilepath = sys.argv[1] \n")
	monFichier.write('exec("')
	monFichier.write('from "+paramfilepath.rstrip(".py")+" import *") \n\n')

        
        monFichier.write("### DECLARATION ###\n\n")
        monFichier.write("abstol = cvode.realtype(1.0E-6)\n")
        monFichier.write("reltol = cvode.realtype(1.0E-6)\n\n")
        monFichier.write("cvode_mem = cvode.CVodeCreate(cvode.CV_BDF,cvode.CV_NEWTON)\n")
        monFichier.write("cvode.CVodeMalloc(cvode_mem,f,0.0,X,cvode.CV_SS,reltol,abstol)\n")

	monFichier.write("cvode.CVodeRootInit(cvode_mem," + str(len(dicoBondaries))+",g,None)\n")


        monFichier.write("cvode.CVDense(cvode_mem,"+str(len(dicoSpecies))+")\n\n")
 
#        monFichier.write("tf = "+ str(simuDuration) +"\n")
        monFichier.write("tf = simu_params['tstop'] \n")

        monFichier.write("iout = 0\n")
        monFichier.write("pourcent = 0\n")
        monFichier.write("t = cvode.realtype(0.0)\n\n\n")
        monFichier.write("### Creation de la liste des points a recuperer ###\n\n")

	# nombre de point a recuperer = 10 x la duree de la simu
        monFichier.write("toutTab = linspace(0.0,tf,"+ str(simuDuration*10) +")\n")

        monFichier.write("particular = []\n")
        monFichier.write("cptPart = 0\n\n")
        monFichier.write("toutList = []\n")
        monFichier.write("toutList.append(toutTab[0])\n")
        monFichier.write("for i in range(1,toutTab.shape[0]-1,1):\n")                                                                                                       
        monFichier.write("\ttout1 = toutTab[i]\n")
        monFichier.write("\ttout2 = toutTab[i+1]\n")
        monFichier.write("\ttoutList.append(tout1)\n")
        monFichier.write("\tif(cptPart < len(particular)):\n")
        monFichier.write("\t\tif(tout1 <= particular[cptPart] and particular[cptPart]<= tout2):\n")
        monFichier.write("\t\t\ttoutList.append(particular[cptPart])\n")
        monFichier.write("\t\t\tcptPart += 1\n\n")
        monFichier.write("toutList.append(toutTab[toutTab.shape[0]-1])\n\n\n")
	
	monFichier.write("### SAUVEGARDE DES CONDITIONS INITIALES ###\n\n")
        monFichier.write("tsave = []\n")
        monFichier.write("tsave.append(t.value)\n\n")

	listOfY = "[ "
	for i in range(len(nameSaveY)):
		listOfY+="ysave_"+str(i)+","
	        monFichier.write("ysave_"+str(i) +" = []\n")
		# pour avoir correspondance entre nameSaveY et listeSpecies car dans dictionnaire pas d indexation
		pos = dicoSpecies.keys().index(" "+ str(nameSaveY[i]) + " ")	
		monFichier.write("ysave_" + str(i) + ".append(X[" + str(pos) + "])\n\n")
	listOfY=listOfY[:-1]+"]"



	listOfAssig = "[ "
	for i in range(len(nameSaveAssig)):
		listOfAssig+="assigsave_"+str(i)+","
	        monFichier.write("assigsave_"+str(i) +" = []\n")
		#pos = dicoSpecies.keys().index(" "+ str(nameSaveY[i]) + " ")
		pos = listeNamesAssignIndexer.index(" "+ str(nameSaveAssig[i]) + " ")
		monFichier.write("assigsave_" + str(i) + ".append(assignments[" + str(pos) + "])\n\n")
	listOfAssig=listOfAssig[:-1]+"]"


	listOfEvents = "[ "
	for i in range(len(nameSaveEvents)):
		listOfEvents+="eventsave_"+str(i)+','	
	        monFichier.write("eventsave_"+str(i) +" = []\n")
		# pour avoir correspondance entre nameSaveY et listeSpecies car dans dictionnaire pas d indexation
		pos = namePulse.index(str(nameSaveEvents[i]))
        	monFichier.write("eventsave_" +str(i) + ".append(events[" + str(pos) +"])\n\n")
	listOfEvents=listOfEvents[:-1]+"]"
	
        monFichier.write("nameSaveY = " + str(nameSaveY) +"\n")
	monFichier.write("nameSaveAssig = " +str(nameSaveAssig) +"\n")
	monFichier.write("nameSaveEvents = " +str(nameSaveEvents) +"\n")


	monFichier.write("### CORE SIMULATOR ###\n\n")
        monFichier.write("time.clock()\n\n")
        monFichier.write("while (True) :\n")
	monFichier.write("\tlistOfY = " + str(listOfY) + "\n")
	monFichier.write("\tlistOfAssig = " + str(listOfAssig) +"\n")
	monFichier.write("\tlistOfEvents = " + str(listOfEvents) + "\n\n")


        monFichier.write("\ttout = toutList[iout]\n")
        monFichier.write("\tflag = cvode.CVode(cvode_mem,tout,X,ctypes.byref(t),cvode.CV_NORMAL)\n")
        monFichier.write("\tif flag == cvode.CV_ROOT_RETURN:\n")
        monFichier.write("\t\trootsfound = cvode.CVodeGetRootInfo(cvode_mem,"+ str(len(dicoBondaries))+")\n")
	monFichier.write("\t\tupdate_rootsfound(rootsfound,t,reltol,abstol,cvode_mem)\n\n")

        monFichier.write("\ttsave.append(t.value)\n\n")
	for i in range(len(nameSaveY)):
		pos = dicoSpecies.keys().index(" "+ str(nameSaveY[i]) + " ")	
		monFichier.write("\tysave_" + str(i) + ".append(X[" + str(pos) + "])\n\n")
	
	for i in range(len(nameSaveAssig)):
		pos = listeNamesAssignIndexer.index(" "+ str(nameSaveAssig[i]) + " ")
		monFichier.write("\tassigsave_" + str(i) + ".append(assignments[" + str(pos) + "])\n\n")


	for i in range(len(nameSaveEvents)):
		pos = namePulse.index(str(nameSaveEvents[i]))	
        	monFichier.write("\teventsave_" +str(i) + ".append(events[" + str(pos) +"])\n\n")
	

 	monFichier.write("\tupdate_assign(t)\n")
        monFichier.write("\tupdate_events(t)\n\n")
        monFichier.write("\tif(pourcent != int((tout/tf)*100)):\n")
        monFichier.write("\t\tpourcent = int((tout/tf)*100)\n")
       # monFichier.write("\t\tprint pourcent\n\n")
        monFichier.write("\tif flag == cvode.CV_SUCCESS:\n")
        monFichier.write("\t\tiout += 1\n\n")
        monFichier.write("\tif iout >= len(toutList):\n")
        monFichier.write("\t\tbreak\n\n")
        monFichier.write("time.sleep(1.0)\n\n\n")

        monFichier.write("### ECRITURE DES RESULTATS ###\n\n")
	monFichier.write("listOfY = " + str(listOfY) + "\n")
	monFichier.write("listOfAssig = " + str(listOfAssig) + "\n")
	monFichier.write("listOfEvents = " + str(listOfEvents) + "\n\n")

	monFichier.write("writeAllResults("+"simu_params['outDirectory']" +",tsave, nameSaveY  +nameSaveAssig+ nameSaveEvents, listOfY+ listOfAssig + listOfEvents, paramfilepath.rstrip('.py') )\n")



    monFichier.close()
    return 0


# write save data 
def writeSaveData(merge_params):

	writePythonFolder = merge_params['outDirectory']

	with open(writePythonFolder+os.sep + "SaveData.py","w") as monFichier:

		monFichier.write("import time \n")
		monFichier.write("import os \n \n")

		monFichier.write("def writeAllResults(path, tsave,listOfNameSaveY,listOfY, tag): \n")
#		monFichier.write("\t directory = os.sep + time.strftime('Results-%Y-%m-%d_%HH%MM%SS',time.localtime()) \n")
		monFichier.write("\t directory = os.sep + tag \n")

		monFichier.write("\t tempPath = path + directory \n")
		monFichier.write("\t os.mkdir(tempPath)	 \n")
		
		monFichier.write("\t for iName in range(len(listOfNameSaveY)): \n")
		
		monFichier.write("\t \t directory_file = tempPath+  os.sep + listOfNameSaveY[iName] \n")
		monFichier.write("\t \t os.mkdir(directory_file) \n")
		monFichier.write("\t \t file = open(directory_file+ os.sep + 'Sim0.txt','w') \n")
		monFichier.write('\t \t file.write("# Time "+ str(listOfNameSaveY[iName]) + "\\n") \n')
		
		monFichier.write("\t \t for i in range(len(tsave)): \n")
		monFichier.write("\t\t\tfile.write(str(tsave[i])) \n")
		monFichier.write('\t\t\tfile.write("\\t") \n')
		monFichier.write("\t\t\tfile.write(str(listOfY[iName][i])) \n")
		monFichier.write('\t\t\tfile.write("\\n") \n')
		monFichier.write("\t\t file.close() \n")
	
    	monFichier.close()
	return 0

#
#################################################################################################################

# pour recuperer le dictionnnaire  simu_params dans le fichier PRMS.py avec toutes les infos 

#exec("from PRMS import *")

paramfilepath = sys.argv[1]
print " paramfilepath = " + str(paramfilepath.rstrip(".py"))
exec("from "+paramfilepath.rstrip(".py")+" import *") 


# obliger de faire comme cela car boucle ne marche pas probleme de segmentation
listeModels = []


document1 = readSBML(merge_params['listXMLFiles'][0]);
listeModels.append(document1.getModel());

document2 = readSBML(merge_params['listXMLFiles'][1]);
listeModels.append(document2.getModel());


print "List of XML files: "
print listeModels


writeODESystem(listeModels, merge_params, simu_params)

writeSimulatorCore(listeModels, merge_params, simu_params)

writeSaveData(merge_params)


