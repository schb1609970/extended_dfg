import os

#importer
from pm4py.objects.log.importer.xes import importer as xes_importer

#discovery
from pm4py.algo.discovery.dfg import algorithm as dfg_discovery

#visualization
from pm4py.visualization.dfg import visualizer as dfg_vis

#extended dfg package
from dfg_extended_discovery.algo import algorithm as dfg_imp_dep
from dfg_extended_discovery.visualization.dfg import visualizer as dfg_imp_dep_vis

#add path for graphviz
os.environ["PATH"] += os.pathsep + 'venv/Library/bin'

#parse log
example1 = "data/implicit_dependency1.xes"
example2 = "data/implicit_dependency2.xes"
example3 = "data/implicit_dependency3.xes"
example4 = "data/implicit_dependency4.xes"
example5 = "data/implicit_dependency5.xes"
example6 = "data/implicit_dependency6.xes"
example7 = "data/implicit_dependency7.xes"
example8 = "data/implicit_dependency8.xes"
log = xes_importer.apply(example1) #Change parameter to look at a different example log

#create standard dfg
dfg = dfg_discovery.apply(log)

#create improved dfg
threshold = 0.98
dfg2 = dfg_imp_dep.apply(dfg, log, threshold)

#improved visualization
gviz = dfg_imp_dep_vis.apply(dfg2, log=log)
dfg_imp_dep_vis.view(gviz)

#standard visualization
#gviz2 = dfg_vis.apply(dfg, log=log)
#dfg_vis.view(gviz2)