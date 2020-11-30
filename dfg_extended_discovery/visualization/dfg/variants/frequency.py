import tempfile
from copy import copy

from graphviz import Digraph

from pm4py.statistics.attributes.log import get as attr_get
from pm4py.objects.dfg.utils import dfg_utils
from pm4py.util import xes_constants as xes
from pm4py.visualization.common.utils import *
from pm4py.util import exec_utils
from pm4py.visualization.dfg.parameters import Parameters

def get_min_max_value(dfg):
    """
    Gets min and max value assigned to edges
    in DFG graph

    Parameters
    -----------
    dfg
        Directly follows graph

    Returns
    -----------
    min_value
        Minimum value in directly follows graph
    max_value
        Maximum value in directly follows graph
    """
    min_value = 9999999999
    max_value = -1

    for edge in dfg:
        if dfg[edge] < min_value:
            min_value = dfg[edge]
        if dfg[edge] > max_value:
            max_value = dfg[edge]

    return min_value, max_value


def assign_penwidth_edges(dfg):
    """
    Assign penwidth to edges in directly-follows graph

    Parameters
    -----------
    dfg
        Direcly follows graph

    Returns
    -----------
    penwidth
        Graph penwidth that edges should have in the direcly follows graph
    """
    penwidth = {}
    min_value, max_value = get_min_max_value(dfg)
    for edge in dfg:
        v0 = dfg[edge]
        v1 = get_arc_penwidth(v0, min_value, max_value)
        penwidth[edge] = str(v1)

    return penwidth


def get_activities_color(activities_count):
    """
    Get frequency color for attributes

    Parameters
    -----------
    activities_count
        Count of attributes in the log

    Returns
    -----------
    activities_color
        Color assigned to attributes in the graph
    """
    activities_color = {}

    min_value, max_value = get_min_max_value(activities_count)

    for ac in activities_count:
        v0 = activities_count[ac]
        """transBaseColor = int(
            255 - 100 * (v0 - min_value) / (max_value - min_value + 0.00001))
        transBaseColorHex = str(hex(transBaseColor))[2:].upper()
        v1 = "#" + transBaseColorHex + transBaseColorHex + "FF"""

        v1 = get_trans_freq_color(v0, min_value, max_value)

        activities_color[ac] = v1

    return activities_color


#def graphviz_visualization(activities_count, dfg, image_format="png", measure="frequency",
#                           max_no_of_edges_in_diagram=170, start_activities=None, end_activities=None):
    """
    Do GraphViz visualization of a DFG graph

    Parameters
    -----------
    activities_count
        Count of attributes in the log (may include attributes that are not in the DFG graph)
    dfg
        DFG graph
    image_format
        GraphViz should be represented in this format
    measure
        Describes which measure is assigned to edges in direcly follows graph (frequency/performance)
    max_no_of_edges_in_diagram
        Maximum number of edges in the diagram allowed for visualization

    Returns
    -----------
    viz
        Digraph object
    """
#    if start_activities is None:
#        start_activities = []
#    if end_activities is None:
#        end_activities = []

#    filename = tempfile.NamedTemporaryFile(suffix='.gv') #F8
#    viz = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': 'transparent'})

    # first, remove edges in diagram that exceeds the maximum number of edges in the diagram
#    dfg_key_value_list = []
#    for edge in dfg:
#        dfg_key_value_list.append([edge, dfg[edge]])
    # more fine grained sorting to avoid that edges that are below the threshold are
    # undeterministically removed
#    dfg_key_value_list = sorted(dfg_key_value_list, key=lambda x: (x[1], x[0][0], x[0][1]), reverse=True)
#    dfg_key_value_list = dfg_key_value_list[0:min(len(dfg_key_value_list), max_no_of_edges_in_diagram)]
#    dfg_allowed_keys = [x[0] for x in dfg_key_value_list]
#    dfg_keys = list(dfg.keys())
#    for edge in dfg_keys:
#        if edge not in dfg_allowed_keys:
#            del dfg[edge]

    # calculate edges penwidth
#    penwidth = assign_penwidth_edges(dfg)
#    activities_in_dfg = set()
#    activities_count_int = copy(activities_count)

#    for edge in dfg:
#        activities_in_dfg.add(edge[0])
#        activities_in_dfg.add(edge[1])

    # assign attributes color
#    activities_color = get_activities_color(activities_count_int)
#
    # represent nodes
#    viz.attr('node', shape='box')
#
#    if len(activities_in_dfg) == 0:
#        activities_to_include = sorted(list(set(activities_count_int)))
#    else:
#        # take unique elements as a list not as a set (in this way, nodes are added in the same order to the graph)
#        activities_to_include = sorted(list(set(activities_in_dfg)))
#
#    activities_map = {}
#
#    for act in activities_to_include:
#        if "frequency" in measure and act in activities_count_int:
#            viz.node(str(hash(act)), act + " (" + str(activities_count_int[act]) + ")", style='filled',
#                     fillcolor=activities_color[act])
#            activities_map[act] = str(hash(act))
#        else:
#            viz.node(str(hash(act)), act)
#            activities_map[act] = str(hash(act))

    # make edges addition always in the same order
#    dfg_edges = sorted(list(dfg.keys()))

    # represent edges
#    for edge in dfg_edges:
#        if "frequency" in measure:
#            label = str(dfg[edge])
#        else:
#            label = human_readable_stat(dfg[edge])
#        viz.edge(str(hash(edge[0])), str(hash(edge[1])), label=label, penwidth=str(penwidth[edge]))
#
#    start_activities_to_include = [act for act in start_activities if act in activities_map]
#    end_activities_to_include = [act for act in end_activities if act in activities_map]
#
#    if start_activities_to_include:
#        viz.node("@@startnode", "@@S", style='filled', shape='circle', fillcolor="#32CD32", fontcolor="#32CD32")
#        for act in start_activities_to_include:
#            viz.edge("@@startnode", activities_map[act])
#
#    if end_activities_to_include:
#        viz.node("@@endnode", "@@E", style='filled', shape='circle', fillcolor="#FFA500", fontcolor="#FFA500")
#        for act in end_activities_to_include:
#            viz.edge(activities_map[act], "@@endnode")
#
#    viz.attr(overlap='false')
#    viz.attr(fontsize='11')
#
#    viz.format = image_format
#
#    return viz

# Added from here...
def graphviz_visualization(activities_count, dfg, image_format="png", measure="frequency",
                           max_no_of_edges_in_diagram=170, start_activities=None, end_activities=None):
    """
    Do GraphViz visualization of a DFG graph

    Parameters
    -----------
    activities_count
        Count of attributes in the log (may include attributes that are not in the DFG graph)
    dfg
        DFG graph
    image_format
        GraphViz should be represented in this format
    measure
        Describes which measure is assigned to edges in direcly follows graph (frequency/performance)
    max_no_of_edges_in_diagram
        Maximum number of edges in the diagram allowed for visualization

    Returns
    -----------
    viz
        Digraph object
    """
    if start_activities is None:
        start_activities = []
    if end_activities is None:
        end_activities = []

    filename = tempfile.NamedTemporaryFile(suffix='.gv')
    viz = Digraph("", filename=filename.name, engine='dot', graph_attr={'bgcolor': 'transparent'})

    # first, remove edges in diagram that exceeds the maximum number of edges in the diagram
    dfg_key_value_list = []
    for edge in dfg:
        dfg_key_value_list.append([edge, dfg[edge]])
    # more fine grained sorting to avoid that edges that are below the threshold are
    # undeterministically removed
    dfg_key_value_list = sorted(dfg_key_value_list, key=lambda x: (x[1], x[0][0], x[0][1]), reverse=True)
    dfg_key_value_list = dfg_key_value_list[0:min(len(dfg_key_value_list), max_no_of_edges_in_diagram)]
    dfg_allowed_keys = [x[0] for x in dfg_key_value_list]
    dfg_keys = list(dfg.keys())
    for edge in dfg_keys:
        if edge not in dfg_allowed_keys:
            del dfg[edge]

    # calculate edges penwidth
    penwidth = assign_penwidth_edges(dfg)
    activities_in_dfg = set()
    activities_count_int = copy(activities_count)


    for edge in dfg:
        activities_in_dfg.add(edge[0])
        activities_in_dfg.add(edge[1])


    activities_count_int, subevents, superevents = check_for_subevents(activities_count, dfg_key_value_list,activities_in_dfg)

    # assign attributes color
    activities_color = get_activities_color(activities_count_int)

    # represent nodes
    viz.attr('node', shape='box')
    viz.attr(compound="true")

    if len(activities_in_dfg) == 0:
        activities_to_include = sorted(list(set(activities_count_int)))
    else:
        # take unique elements as a list not as a set (in this way, nodes are added in the same order to the graph)
        activities_to_include = sorted(list(set(activities_in_dfg)))

    activities_map = {}

    # make edges addition always in the same order
    dfg_edges = sorted(list(dfg.keys()))


    for act in activities_to_include:
        if act.find('_SUBEVENT') > -1:
            node_desc = ''
        else:
            node_desc = act

        if activities_count_int[act] > 0:
            node_count = " (" + str(activities_count_int[act]) + ")"
        else:
            node_count = ''
        if "frequency" in measure and act in activities_count_int and act not in superevents and act not in subevents:
            viz.node(str(hash(act)), str(act) + " (" + str(activities_count_int[act]) + ")", style='filled',
                     fillcolor=activities_color[act])
            activities_map[act] = str(hash(act))
        elif act not in superevents and act not in subevents:
            viz.node(str(hash(act)), act)
            activities_map[act] = str(hash(act))
        elif act in superevents:
            for super in superevents:
                with viz.subgraph(name=super) as c:
                    super_label = super[8:len(super)]
                    c.attr(label=super_label)
                    activities_map[super] = str(super)
                    if activities_count_int[act] > 0:
                        c.node(str(hash(super)),"Placeholder",style='invis')
                    for sub in subevents:
                        if sub[0:sub.find('_SUBEVENT')] == super[8:len(super)]:
                            c.node(str(hash(sub)), "(" + str(activities_count_int[sub]) + ")", style='filled',
                                     fillcolor=activities_color[sub])
                            activities_map[sub] = str(hash(sub))

    # represent edges
    for edge in dfg_edges:
        if "frequency" in measure:
            label = str(dfg[edge])
        else:
            label = human_readable_stat(dfg[edge])
        if dfg[edge] >0:
            if edge[0] not in superevents and edge[1] not in superevents:
                viz.edge(str(hash(edge[0])), str(hash(edge[1])), label=label, penwidth=str(penwidth[edge]))
            elif edge[0] in superevents:
                viz.edge(str(hash(edge[0])),str(hash(edge[1])),label=label,penwidth=str(penwidth[edge]),ltail=edge[0])
            elif edge[1] in superevents:
                viz.edge(str(hash(edge[0])),str(hash(edge[1])),label=label,penwidth=str(penwidth[edge]), lhead=edge[1])

    start_activities_to_include = [act for act in start_activities if act in activities_map]
    end_activities_to_include = [act for act in end_activities if act in activities_map]

    if start_activities_to_include:
        viz.node("@@startnode", "@@S", style='filled', shape='circle', fillcolor="#32CD32", fontcolor="#32CD32")
        for act in start_activities_to_include:
            viz.edge("@@startnode", activities_map[act])

    if end_activities_to_include:
        viz.node("@@endnode", "@@E", style='filled', shape='circle', fillcolor="#FFA500", fontcolor="#FFA500")
        for act in end_activities_to_include:
            viz.edge(activities_map[act], "@@endnode")

    viz.attr(overlap='false')
    viz.attr(fontsize='11')

    viz.format = image_format

    return viz


def check_for_subevents(counted_in_log, dfg_keys, all_activities):
    subevents = set()
    superevents = set()

    #get a list of all subevents and superevents
    for entry in all_activities:
        at_index = entry.find('_SUBEVENT')
        if at_index > -1:
            subevents.add(entry)
            superevents.add("cluster_" + str(entry[0:at_index]))
            counted_in_log[[entry][0]] = 0

    #assess how many occurences there are for the subevents and superevents
    for entry in dfg_keys:
        if entry[0][0] in subevents:
            counted_in_log[entry[0][0]] += entry[1]
            counted_in_log[entry[0][0][0:entry[0][0].find('_SUBEVENT')]] = counted_in_log[entry[0][0][0:entry[0][0].find('_SUBEVENT')]] - entry[1]

    counted_in_log2 = counted_in_log.copy()
    for activity in counted_in_log:
        for super in superevents:
            if activity == super[8:len(super)]:
                counted_in_log2["cluster_" + str(activity)] = counted_in_log2[activity]
                counted_in_log2.pop(activity, None)

    return counted_in_log2, subevents, superevents


def apply(dfg, log=None, parameters=None, activities_count=None):
    if parameters is None:
        parameters = {}

    activity_key = exec_utils.get_param_value(Parameters.ACTIVITY_KEY, parameters, xes.DEFAULT_NAME_KEY)
    image_format = exec_utils.get_param_value(Parameters.FORMAT, parameters, "png")
    max_no_of_edges_in_diagram = exec_utils.get_param_value(Parameters.MAX_NO_EDGES_IN_DIAGRAM, parameters, 75)
    start_activities = exec_utils.get_param_value(Parameters.START_ACTIVITIES, parameters, [])
    end_activities = exec_utils.get_param_value(Parameters.END_ACTIVITIES, parameters, [])

    if activities_count is None:
        if log is not None:
            activities_count = attr_get.get_attribute_values(log, activity_key, parameters=parameters)
        else:
            activities = dfg_utils.get_activities_from_dfg(dfg)
            activities_count = {key: 1 for key in activities}

    return graphviz_visualization(activities_count, dfg, image_format=image_format, measure="frequency",
                                  max_no_of_edges_in_diagram=max_no_of_edges_in_diagram,
                                  start_activities=start_activities, end_activities=end_activities)
