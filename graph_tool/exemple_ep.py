##
import os
from graph_tool.all import *
import numpy as npr
import numpy.random as npr
from numpy.linalg import norm
from pylab import *
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib
##


from numpy.random import randint

g = Graph()
g.add_vertex(100)

# insert some random links
for s,t in zip(randint(0, 100, 100), randint(0, 100, 100)):
    g.add_edge(g.vertex(s), g.vertex(t))

vprop_double = g.new_vertex_property("double")            # Double-precision floating point
v = g.vertex(10)
vprop_double[v] = 3.1416

vprop_vint = g.new_vertex_property("vector<int>")         # Vector of ints
v = g.vertex(40)
vprop_vint[v] = [1, 3, 42, 54]

eprop_dict = g.new_edge_property("object")                # Arbitrary Python object.
e = g.edges().next()
eprop_dict[e] = {"foo": "bar", "gnu": 42}                 # In this case, a dict.

gprop_bool = g.new_graph_property("bool")                 # Boolean
gprop_bool[g] = True
##

g
##
eprop_float = g.new_edge_property("float")  # Arbitrary Python object.
eprop_float[e] = 14.1  

##
g.ep.dist = eprop_float
##
e
##
g.properties

##
