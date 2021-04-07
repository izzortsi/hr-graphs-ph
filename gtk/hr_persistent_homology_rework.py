##
import os
##
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

Mass = g.new_vertex_property('float')
Lum  = g.new_vertex_property('float')
Mag = g.new_vertex_property('float')
pos = g.new_vertex_property('vector<float>')
pos_ = g.new_vertex_property('vector<float>')

g.vp.mass=Mass
g.vp.lum = Lum
g.vp.mag = Mag
g.vp.pos = pos
g.vp.pos_ = pos_

N=250
v = g.add_vertex(N)

global init_foot, ibin

a=1
b=0 

prop=g.vp.mag

mag =mag[0:N]
lum =lum[0:N]
mass =mass[0:N]

init_foot = 0.003
ibin =      0.003
fbin = 0.21

step = 0.1       # move step
K = 1.5   

##

##
#minmax scaling
mag-=min(mag);mag/=max(mag)
lum-=min(lum);lum/=max(lum)
mass-=min(mass);mass/=max(mass)

min(mag), max(mag)
min(lum), max(lum)
min(mass), max(mass)

for i, v in enumerate(g.vertices()):
    g.vp.mass[v]=mass[i]
    g.vp.lum[v]=lum[i]
    g.vp.mag[v]=mag[i]
    g.vp.pos[v] = np.array([mag[i], lum[i]])

#gtdraw = gt.graph_draw(g, pos=g.vp.pos, vertex_fill_color=g.vp.lum,vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2))
##
posv = copy(g.vp.pos.get_2d_array([0, 1]).T)

#gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, K=1.5)
g.vp.pos = gt.sfdp_layout(g, K=1.5)

#gt.graph_draw(gu, pos=gu.vp.pos, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))
#gt.graph_draw(gu, pos=gu.vp.pos, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))
#gt.graph_draw(gu, pos=gu.vp.pos_, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))
##
win = gt.GraphWindow(g, g.vp.pos, geometry=(500, 400))
count = 0
##
def update_state():

    global ibin
    global count
    
    gg, gpos = gt.geometric_graph(posv, ibin)

    #gt.graph_union(gu, gg, intersection=gu.vertex_index, internal_props=True, include=True)
    
    new_edges = []

    for e2 in gg.get_edges():
        if e2 not in g.get_edges():
            new_edges.append(e2)
    
    g.add_edge_list(new_edges)
        
    g.vp.pos = gt.sfdp_layout(g, pos=g.vp.pos, K=K, init_step=step, max_iter=1)
    
    ibin += step

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
