merge_params = {
	'listXMLFiles' : ["../M1R_V2.1_Allosteric_site_NAM_v2.xml", "../20101123_Mcurrent_NAM_v11.xml"], 
	'outDirectory' : "./",
	'outCsteFile' : "./Cstes.txt",
}

simu_params = {
	'outDirectory' : "/media/nicolas/DATA/ParserMergeXML/",
	'inCsteFile' : "./Cstes.txt", 
	'tstop' : 30e3,
	'namePulse' :['ACh', 'Ant', 'L', 'Mod', 'GDP', 'GTP'],
	'timePulse' : [[3000,4000], [0,0], [0,0], [0,0], [0,0], [0,0]], 
	'valuePulse' : [1.0,0, 0, 0, 0, 0],
	'nameSaveY' : [ 'Ga_GTP' ], 
	'nameSaveAssig' : ['IP3'], 
	'nameSaveEvents' : ['ACh'],
}

