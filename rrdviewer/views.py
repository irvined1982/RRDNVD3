#!/usr/bin/env python
# Copyright 2014 David Irvine
#
# This file is part of RRD Viewer
#
# RRD Viewer is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# RRD Viewer is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RRD Viewer. If not, see <http://www.gnu.org/licenses/>.

import json
import os
import rrdtool
from django.http import Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


GRAPH_PATH = '/tmp'


def get_graph(request, start_time, end_time, path, CF="AVERAGE"):
    start_time = int(start_time)
    end_time = int(end_time)

    path = path.lstrip("/")
    path = path.split('/')

    filename = os.path.join(GRAPH_PATH, *path)
    if not os.path.exists(filename):
        raise Http404("RRD does not exist")
    args = []
    if start_time != 0:
        args.append("-s")
        args.append(str("%s" % start_time))

    if end_time != 0:
        args.append("-e")
        args.append(str("%s" % end_time))

    data = rrdtool.fetch(
        str(filename),
        str(CF),
        *args
    )

    header = data[0]
    time = header[0]
    step_time = header[2]


    serieses = []
    for series in data[1]:
        serieses.append({
            'key': series,
            'values': [],
        })

    # Broken for multiple serieses in same RRD, need to understand dataformat more.
    for row in data[2:][0]:
        for series_index in xrange(len(row)):
            serieses[series_index]['values'].append([time * 1000, row[series_index]])
        time += step_time

    return HttpResponse(json.dumps(serieses), content_type="application/json")


def get_graph_info_dict(path):
    info = {}
    info_file_path = "%s.info" % path[0:-4]
    if os.path.exists(info_file_path):
        info = json.load(open(info_file_path))

    info['rrd_absolute_path'] = path
    info['relative_path'] = info['rrd_absolute_path']
    if info['relative_path'].startswith(GRAPH_PATH):
        info['relative_path'] = info['relative_path'][len(GRAPH_PATH):]
    info['hourly_rrd_url'] = reverse('get_graph', args=[-60*60, 0, info['relative_path']])
    info['daily_rrd_url'] = reverse('get_graph', args=[-60*60*24, 0, info['relative_path']])
    info['weekly_rrd_url'] = reverse('get_graph', args=[-60*60*24*7, 0, info['relative_path']])
    info['monthly_rrd_url'] = reverse('get_graph', args=[-60*60*24*31, 0, info['relative_path']])
    info['yearly_rrd_url'] = reverse('get_graph', args=[-60*60*24*31*265, 0, info['relative_path']])
    info['info_url'] = reverse('get_info',args=[info['relative_path']])

    info['name'] = info['relative_path'][:-4]

    for k, v in rrdtool.info(info['rrd_absolute_path']).iteritems():
        components = k.split(".")
        if len(components) == 1:
            info[components[0]] = v
        else:
            key = components[0]
            key, t, index = key.partition("[")
            index = index.rstrip("]")
            if key not in info:
                info[key] = {}
            if index not in info[key]:
                info[key][index] = {}
            if len(components) == 2:
                info[key][index][components[1]] = v
            elif len(components) == 3:
                i = info[key][index]  # dict of third level entries
                tkey, t, tindex = components[1].partition("[")
                tindex = index.rstrip("]")
                if tkey not in i:
                    i[tkey] = {}
                if tindex not in i[tkey]:
                    i[tkey][tindex] = {}
                i[tkey][tindex][components[2]] = v
    return info


def get_info(request, path):
    filename = os.path.join(GRAPH_PATH, *path)
    if not os.path.exists(filename):
        raise Http404("RRD does not exist")

    return HttpResponse(json.dumps(get_graph_info_dict(filename)), content_type="application/json")


def show_rrd(request, path):
    pass


def list_graphs(request):
    id=0
    graphs = []
    for directory, subdirs, files in os.walk(GRAPH_PATH):
        for file in files:
            if file.endswith(".rrd"):
                id += 1
                if id > 10:
                    continue
                f=os.path.join(directory,file)
                info = get_graph_info_dict(f)
                info['graph_id'] = "graph_%s" % id
                graphs.append(info)
    paginator = Paginator(graphs, 10)
    page = request.GET.get('page')
    try:
        graphs = paginator.page(page)
    except PageNotAnInteger:
        graphs=paginator.page(1)
    except EmptyPage:
        graphs=paginator.num_pages

    return render_to_response("rrdviewer/graph_list.html", {'graphs': graphs, },
                              context_instance=RequestContext(request))
