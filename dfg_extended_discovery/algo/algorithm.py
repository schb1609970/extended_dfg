import pandas as pd
from pm4py.objects.conversion.log.versions import to_data_frame as log_conversion
import itertools

def apply(dfg, log, thresh=None):
    if thresh is None:
      thresh = 1
    threshold = thresh
    dfg_keys = dfg.keys()  #creates a dict_keys of all directly follows relationships
    rel_list = set(dfg_keys)  #change data type to set

    activities = set()
    for relationship in rel_list:  # create list of unique activities in the dfg
        activities.add(relationship[0])
        activities.add(relationship[1])

    count_incoming_act = {i: 0 for i in activities}  # count how many incoming arrows an activity has
    for x in rel_list:
        count_incoming_act[x[1]] += 1

    count_outgoing_act = {i: 0 for i in activities}  # count how many outgoing arrows an activity has
    for x in rel_list:
        count_outgoing_act[x[0]] += 1

    multiple_incoming = dict()  # extract the ones that have >1 incoming arrows and is not an end activity
    for x in count_incoming_act:
        if count_incoming_act[x] > 1 and count_outgoing_act[x] > 0:
            multiple_incoming[x] = count_incoming_act[x]

    multiple_outgoing = dict()  # extract the ones that have >1 outgoing arrows and is not a start activity
    for x in count_outgoing_act:
        if count_outgoing_act[x] > 1 and count_incoming_act[x] > 0:
            multiple_outgoing[x] = count_outgoing_act[x]

    if multiple_incoming is not None:
        # find the portion of trace where an implicit dependency could be
        possible_traces_list_of_lists = list()
        incoming_possible = dict()
        outgoing_possible = dict()
        for x in multiple_incoming:
            possible_traces = list()
            for y in rel_list:
                if y[1] == x:
                    possible_traces.append(list(y))
            currently_added_act = x
            currently_added_act_at_start = currently_added_act
            continue_splitting = "yes"
            while currently_added_act not in multiple_outgoing:
                currently_added_act_loop_begin = currently_added_act
                possible_traces2 = possible_traces.copy()
                for y in rel_list:
                    if y[0] == currently_added_act:
                        currently_added_act = y[1]
                        for all_traces in possible_traces2:
                            all_traces.append(y[1])
                        if(y[1] in multiple_outgoing):
                            possible_traces = possible_traces2.copy()
                            break
                if currently_added_act_loop_begin == currently_added_act:
                    currently_added_act = currently_added_act_at_start
                    continue_splitting = "no"
                    break
            if continue_splitting == "yes":
                to_be_added = list()
                for y in rel_list:
                    if y[0] == currently_added_act:
                        to_be_added.append(y[1])
                unique_possible_traces = list()
                for all_traces in possible_traces:
                    for i in range(len(to_be_added)):
                        new_trace = all_traces.copy()
                        new_trace.append(to_be_added[i])
                        unique_possible_traces.append(new_trace)
                append_possible_traces = "yes"
                for trace in unique_possible_traces:
                    if len(trace) != len(set(trace)):
                        append_possible_traces = "no"
                if append_possible_traces == "yes":
                    possible_traces_list_of_lists.append(unique_possible_traces)
                incoming_possible[x] = len(set(map(lambda o: o[0], unique_possible_traces)))
                outgoing_possible[x] = len(set(map(lambda o: o[-1], unique_possible_traces)))

    df = get_case_and_event_from_log(log)

    occurrences_total = list()
    occurrence_income_act_count = dict()
    for possible_dependency in possible_traces_list_of_lists:
        occurrences = dict()
        for trace in possible_dependency:
            occurrences[tuple(trace)] = 0
            if trace[0] not in occurrence_income_act_count.keys():
                occurrence_income_act_count[trace[0]] = 0
        for possible_trace in possible_dependency:
            joined_possible_trace = (''.join(possible_trace))
            for ind in df.index:
                if joined_possible_trace in df['Trace'][ind]:
                    occurrences[tuple(possible_trace)] += 1
                    occurrence_income_act_count[possible_trace[0]] += 1
        occurrences_total.append(occurrences)

    dfg2 = dfg.copy()
    if occurrences_total:
        for x in range(len(occurrences_total)):
            del_act = (list(occurrences_total[x].keys())[0])[1:-1]  # get all activities that need to be reapplied
            actually_del_act = set()
            before_del_act = list()
            after_del_act = list()
            for trace in occurrences_total[x]:
                limit = occurrence_income_act_count[trace[0]]*threshold     #calculate how many traces there have to be minimum
                if occurrences_total[x][trace] >= limit:
                    before_del_act.append(trace[0])
                    after_del_act.append(trace[-1])
                    for act in del_act:
                        actually_del_act.add(act)
                        if del_act.index(act) == 0:
                            dfg2[(str(trace[0]), str(act + "_SUBEVENT" + str(before_del_act.index(trace[0])+1)))] += occurrences_total[x][trace]
                            dfg2[(str(trace[0]), str(act))] -= occurrences_total[x][trace]
                        elif del_act.index(act) > 0:
                            dfg2[str(list(del_act)[del_act.index(act) - 1]) + '_SUBEVENT' + str(before_del_act.index(trace[0])+1), str(list(del_act)[del_act.index(act)]) + '_SUBEVENT' + str(before_del_act.index(trace[0])+1)] +=occurrences_total[x][trace]
                            dfg2[str(list(del_act)[del_act.index(act) - 1]), str(list(del_act)[del_act.index(act)])] -= occurrences_total[x][trace]
                        if del_act.index(act) == (len(del_act)-1):
                            dfg2[str(list(del_act)[del_act.index(act)]) + '_SUBEVENT' + str(before_del_act.index(trace[0])+1), trace[-1]] +=occurrences_total[x][trace]
                            dfg2[(str(act), str(trace[-1]))] -= occurrences_total[x][trace]
            dfg3 = dfg2.copy()

            for entry in dfg2:
                 if entry[0] in actually_del_act and entry[1] in actually_del_act:
                    dfg3["cluster_" + str(entry[0]), str("cluster_" + entry[1])] += dfg3[entry]
                 elif entry[0] in actually_del_act:
                    dfg3["cluster_" + str(entry[0]), str(entry[1])] += dfg3[entry]
                 elif entry[1] in actually_del_act:
                    dfg3[str(entry[0]), "cluster_" + str(entry[1])] += dfg3[entry]
                 if entry[0] in actually_del_act or entry[1] in actually_del_act:
                    dfg3.pop((str(entry[0]), str(entry[1])), None)
            dfg2 = dfg3.copy()
    return dfg2


def get_case_and_event_from_log(log):
    temp = {}
    for case_index, case in enumerate(log):
        trace = ''
        for event_index, event in enumerate(case):
            trace += event["concept:name"]
        temp[case_index] = trace
    data = {'Case_Index': temp.keys(),
            'Trace': temp.values()}
    df = pd.DataFrame(data, columns = ['Case_Index', 'Trace'])
    return df
