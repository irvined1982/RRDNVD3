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

from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'rrdviewer.views.list_graphs', name="rrd_home"),
                       url(r'^graph/(?P<start_time>.+?)/(?P<end_time>.+?)(?P<path>/.+?\.rrd)$', 'rrdviewer.views.get_graph', name="get_graph"),
                       url(r'^info(?P<path>/.+?\.rrd)$', 'rrdviewer.views.get_info', name="get_info"),
                       url(r'^rrd(?P<path>/.+?\.rrd)$', 'rrdviewer.views.show_rrd', name="rrd_view"),
                       )


