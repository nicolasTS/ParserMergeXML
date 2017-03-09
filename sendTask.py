from ClusterShell.Task import task_self, NodeSet
import os, time
import sys

 
source = "/media/nicolas/m1ACh_DT/ParserMergeXML"
dest = "/media/nicolas/DATA/TESTS/"
nodeset ="192.168.1.5"


 # get task associated with calling thread
task = task_self()


# copy file
task.copy(source + os.sep +"1_batch_conc.py", dest+ os.sep +"1_batch_conc.py", nodes=nodeset)
task.copy(source + os.sep +"PRMS_Thera.py", dest, nodes=nodeset)
task.copy(source + os.sep +"SimulatoreCore.py", dest, nodes=nodeset)
task.copy(source + os.sep +"Cstes_v2.txt", dest, nodes=nodeset)
task.copy(source + os.sep +"ODESystems.py", dest, nodes=nodeset)
task.copy(source + os.sep +"SaveData.py", dest, nodes=nodeset)
task.resume()

# run 
task.run("cd " + dest +"; python 1_batch_conc.py PRMS_Thera.py", nodes=nodeset)


print task.node_buffer(nodeset)

