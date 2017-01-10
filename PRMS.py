
filenameSBML1 = "../M1R_V2.1_Allosteric_site_NAM.xml"; 
filenameSBML2 = "../20101123_Mcurrent_NAM_v11.xml"

path = "./"


merge_params = {
	'listXMLFiles' : [path + filenameSBML1, path + filenameSBML2], 
	'outDirectory' : path,
}

simu_params = {
	'outDirectory' : path,
	'tstop' : 20000,
	'namePulse' :['ACh', 'Ant', 'L', 'Mod', 'GDP', 'GTP'],
	'timePulse' : [[3000, 4000], [0,0], [0,0], [0,0], [0,0], [0,0]], 
	'valuePulse' : [1.0,0, 0, 0, 0, 0],
	'nameSaveY' : ['R','RL', 'RACh', 'RMod', 'RAnt', 'Ga_GTP', 'Ga_GTP_PLC' ,'PIP','PIP2', 'DAG', 'sIP', 'sIP3', 'sIP2', 'sPI'], 
	'nameSaveAssig' : ['readout_RL','IP', 'IP2', 'IP3'], 
	'nameSaveEvents' : ['ACh', 'L', 'Mod', 'Ant'],
}

