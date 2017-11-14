from analysis import *
from musicitem import *
from math import ceil


def check_data(request):
    characters = [item in request for item in TimeDelta.PERCENTAGEDARGS]
    characters.extend([item in request for item in TimeDelta.NONPERCENTAGEDARGS])
    if characters.count(True) == 0:
        return False
    try:
        s, e = map(int, [request['start_year'], request['end_year']])
        assert(s < e and e <= 2017)
        t = request['time_type']
        assert(t in ['years', 'quarters'])
        if t == 'years':
            assert(s >= 1956)
        else:
            assert(s >= 2010)
            assert(int(request['quarters_special']) in [-1, 1, 2, 3, 4])
        assert(request['data_type'] in ['middle', 'top', 'min', 'max'])
        return True
    except:
        return False

def build_graphs(request, range_years, range_quarters):
    if not check_data(request):
        return []
    result = []
    s, e = map(int, (request['start_year'], request['end_year']))
    if [item in request for item in TimeDelta.PERCENTAGEDARGS].count(True) > 0:
        percentaged_graph = {}
        cols = [item for item in TimeDelta.PERCENTAGEDARGS
                                        if item in request]
        percentaged_graph['columns'] = cols
        rows = []
        if request['data_type'] in ['middle', 'top']:
            percentaged_graph['title'] = ("Dynamic of %s characteristics of %s songs in percents" %
                                          (request['time_type'],
                                           ["all", "the most popular"][request['data_type'] == 'top']))
            if request['time_type'] == 'years':
                for i in range(s - 1956, e - 1956 + 1):
                    temprow = [range_years._pieces[i]['name']]
                    if request['data_type'] == 'top':
                        tempfeature = range_years._pieces[i].create_middle_feature(150)
                    else:
                        tempfeature = range_years._pieces[i]._middle_feature
                    for item in cols:
                        temprow.append(tempfeature[item] * 100)
                    rows.append(temprow)

            else:
                sp = int(request['quarters_special'])
                sp = {-1: [0, 1, 2, 3], 1: [0], 2: [1], 3: [2], 4: [3]}[sp]
                for i in range(s - 2010, e - 2010 + 1):
                    for special in sp:
                        temprow = [range_quarters._pieces[i][special]['name'][:-8]]
                        if request['data_type'] == 'top':
                            tempfeature = range_quarters._pieces[i][special].create_middle_feature(150)
                        else:
                            tempfeature = range_quarters._pieces[i][special]._middle_feature
                        for item in cols:
                            temprow.append(tempfeature[item] * 100)
                        rows.append(temprow)
        else:
            percentaged_graph['title'] = ("Dynamic of %s %s characteristics of all songs" %
                                          (request['time_type'],
                                           ['maximal', 'minimal'][request['data_type'] == 'min']))
            if request['time_type'] == 'years':
                for i in range(s - 1956, e - 1956 + 1):
                    temprow = [range_years._pieces[i]['name']]
                    for item in cols:
                        temprow.append(range_years._pieces[i]['extreme_nums'][request['data_type']][item]['value'] * 100)
                    rows.append(temprow)
            else:
                sp = int(request['quarters_special'])
                sp = {-1: [0, 1, 2, 3], 1: [0], 2: [1], 3: [2], 4: [3]}[sp]
                for i in range(s - 2010, e - 2010 + 1):
                    for special in sp:
                        temprow = [range_quarters._pieces[i][special]['name'][:-8]]
                        for item in cols:
                            temprow.append(range_quarters._pieces[i][special]['extreme_nums'][request['data_type']][item]['value'] * 100)
        percentaged_graph['rows'] = rows
        percentaged_graph['max'] = 100
        percentaged_graph['min'] = 0
        result.append(percentaged_graph)
    if [item in request for item in TimeDelta.NONPERCENTAGEDARGS].count(True) > 0:
        cols = [item for item in TimeDelta.NONPERCENTAGEDARGS
                if item in request]
        for characteristic in cols:
            graph = {}
            rows = []
            graph['columns'] = [characteristic]
            temp_max, temp_min = -float('inf'), float('inf')
            if request['data_type'] in ['min', 'max']:
                graph['title'] = ("%s dynamic of \
                                        %s %s values" % (request['time_type'],
                                                         ['maximal', 'minimal'][request['data_type'] == 'min'],
                                                         characteristic))
            else:
                graph['title'] = ("Dynamic of %s %s values of %s" % (request['time_type'],
                                                                     characteristic,
                                                                     ["the most popular songs",
                                                                      "all songs"][request['data_type'] == 'middle']))
            if request['time_type'] == 'years':
                for i in range(s - 1956, e - 1956 + 1):
                    temprow = [range_years._pieces[i]['name']]
                    if request['data_type'] in ['min', 'max']:
                        value = range_years._pieces[i]['extreme_nums'][request['data_type']][characteristic]['value']
                    else:
                        if request['data_type'] == 'top':
                            tempfeature = range_years._pieces[i].create_middle_feature(150)
                        else:
                            tempfeature = range_years._pieces[i]['middle_feature']
                        value = tempfeature[characteristic]
                    temprow.append(value)
                    temp_max = max(value, temp_max)
                    temp_min = min(temp_min, value)
                    rows.append(temprow)
            else:
                sp = int(request['quarters_special'])
                sp = {-1: [0, 1, 2, 3], 1: [0], 2: [1], 3: [2], 4: [3]}[sp]
                for i in range(s - 2010, e - 2010 + 1):
                    for special in sp:
                        temprow = [range_quarters._pieces[i][special]['name']]
                        print(temprow)
                        if request['data_type'] in ['min', 'max']:
                            value = range_quarters._pieces[i][special]['extreme_nums'][request['data_type']][characteristic]['value']
                        else:
                            if request['data_type'] == 'middle':
                                temp = range_quarters._pieces[i][special]['middle_feature']
                            else:
                                temp = range_quarters._pieces[i][special].create_middle_feature(150)
                            value = temp[characteristic]
                        temprow.append(value)
                        temp_max = max(value, temp_max)
                        temp_min = min(temp_min, value)
                        rows.append(temprow)

            graph['rows'] = rows
            graph['min'] = temp_min
            graph['max'] = temp_max
            result.append(graph)
    return result