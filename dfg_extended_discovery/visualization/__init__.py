from dfg_extended_discovery.visualization import common, dfg
import pkgutil

if pkgutil.find_loader("matplotlib"):
    # graphs require matplotlib. This is included in the default installation;
    # however, they may lead to problems in some platforms/deployments
    from pm4py.visualization import graphs
if pkgutil.find_loader("matplotlib") and pkgutil.find_loader("pyvis"):
    # SNA requires both packages matplotlib and pyvis. These are included in the default installation;
    # however, they may lead to problems in some platforms/deployments
    from pm4py.visualization import sna
if pkgutil.find_loader("pydotplus"):
    # heuristics net visualization requires pydotplus. This is included in the default installation;
    # however, they may lead to problems in some platforms/deployments
    from pm4py.visualization import heuristics_net
