
filenameSBML2 = "20101123_Mcurrent_NAM_v5.xml"
#M1R_V2.1_Allosteric_site_NAM.xml"; 
path = "./"



merge_params = {
	'listXMLFiles' : [path + filenameSBML2], 
	'outDirectory' : path,
}

simu_params = {
	'outDirectory' : path,
	'tstop' : 5000,
	'namePulse' :['Ga_GTP_PLC'],
	'timePulse' : [[1000, 2000]], 
	'valuePulse' : [1], 
	'nameSaveY' : ['PIP','PIP2', 'DAG', 'sIP', 'sIP3'], 
	'nameSaveAssig' : ['IP', 'IP2', 'IP3'], 
	'nameSaveEvents' : ['Ga_GTP_PLC'],
}


