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
Distance = g.new_edge_property('float')

g.vp.lum = Lum
g.vp.mag = Mag
g.vp.mass = Mass
g.ep.dist = Distance

N=400
v = g.add_vertex(N)

mag =mag[0:N]
lum = lum[0:N]
mass = mass[0:N]

init_foot = 0.0001
ibin =      0.0001
fbin = 0.21

step = 0.25       # move step
K = 2.0

##

##
#minmax scaling
mag-=min(mag);mag/=max(mag)
lum -= min(lum); lum /= max(lum)
mass-=min(mass);mass/=max(mass)

for i, v in enumerate(g.get_vertices()):
    g.vp.lum[v]=lum[i]
    g.vp.mag[v]=mag[i]
    g.vp.mass[v] = mass[i]

#gtdraw = gt.graph_draw(g, pos=g.vp.pos, vertex_fill_color=g.vp.lum,vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2))
##
points = np.array(list(zip(g.vp.lum.a, g.vp.mag.a)))
pos = gt.sfdp_layout(g, K=K)
#gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, K=1.5)pos = gt.sfdp_layout(g, K=K)
##

##
gg, gpos = gt.geometric_graph(points, fbin)
##
ug = gt.graph_union(gg, g, intersection = g.vertex_index, internal_props=True)
##
def set_distances(g):
    dists = []
    for e in ug.edges():
        s, t = e
        pos_s = np.array([g.vp.lum[s], g.vp.mag[s]])
        pos_t = np.array([g.vp.lum[t], g.vp.mag[t]])
        distance = norm(pos_s - pos_t)
        #print(distance)
        dists.append(distance)
        g.ep.dist[e] = distance
    return dists
        
##
distances = set_distances(ug)

edge_filter = ug.new_ep('bool')
edge_filter.a = ug.ep.dist.a < ibin
ug.set_edge_filter(edge_filter)
##
pos = gt.sfdp_layout(ug, K=K)

##


##
win = gt.GraphWindow(ug, pos, geometry=(500, 400), vertex_fill_color=ug.vp.lum,vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2))
count = 0
##
def update_state():

    global ibin
    global count

    edge_filter.a = ug.ep.dist.a < ibin
    ug.set_edge_filter(edge_filter)

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
