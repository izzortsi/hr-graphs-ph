##
import os
import graph_tool.all as gt
import numpy as npr
import numpy.random as npr
from numpy.linalg import norm
from pylab import *
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib


##
#importing data

mass,lum,mag= loadtxt('new_data.txt', usecols=(2,3,4), unpack=True, skiprows=2)
                                     #building the graph

g = gt.Graph(directed=False)

Lum  = g.new_vertex_property('float')
Mag = g.new_vertex_property('float')
Mass = g.new_vertex_property('float')

g.vp.lum = Lum
g.vp.mag = Mag
g.vp.mass=Mass

N=250
v = g.add_vertex(N)

mag =mag[0:N]
lum = lum[0:N]
mass = mass[0:N]

init_foot = 0.001
ibin =      0.001
fbin = 0.21

step = 0.1       # move step
K = 1.0

##

##
#minmax scaling
mag-=min(mag);mag/=max(mag)
lum -= min(lum); lum /= max(lum)
mass-=min(mass);mass/=max(mass)

for i, v in enumerate(g.get_vertices()):
    g.vp.lum[v]=lum[i]
    g.vp.mag[v]=mag[i]
    g.vp.mass[v]=mass[i]

#gtdraw = gt.graph_draw(g, pos=g.vp.pos, vertex_fill_color=g.vp.lum,vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2))
##
points = np.array(list(zip(g.vp.lum.a, g.vp.mag.a)))
pos = gt.sfdp_layout(g, K=K)
#gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, K=1.5)pos = gt.sfdp_layout(g, K=K)
##

##
gg, gpos = gt.geometric_graph(points, ibin)
##
ug = gt.graph_union(gg, g, intersection = g.vertex_index, internal_props=True)
##
pos = gt.sfdp_layout(ug, K=K)
##
win = gt.GraphWindow(ug, pos, geometry=(500, 400), vertex_fill_color=ug.vp.lum,vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2))
count = 0
##
def update_state():

    global ibin
    global count
    
    gg, gpos = gt.geometric_graph(points, ibin)

    #gt.graph_union(gu, gg, intersection=gu.vertex_index, internal_props=True, include=True)
    
    new_edges = []

    for e2 in gg.get_edges():
        if e2 not in ug.get_edges():
            new_edges.append(e2)

    print(len(new_edges))
    ug.add_edge_list(new_edges)
        
    gt.sfdp_layout(ug, pos=pos, K=K, init_step=step, max_iter=1)
    
    ibin += init_foot

    count += 1

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.regenerate_surface()
    win.graph.queue_draw()

    # We need to return True so that the main loop will call this function more
    # than once.
    return True


##

cid = GLib.idle_add(update_state)

# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()
##
##
