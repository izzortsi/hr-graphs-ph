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

offscreen = True
##
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

step = 0.3      # move step
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
    g.vp.mass[v] = mass[i]

#gtdraw = gt.graph_draw(g, pos=g.vp.pos, vertex_fill_color=g.vp.lum,vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2))
##
points = np.array(list(zip(g.vp.lum.a, g.vp.mag.a)))


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
pos = gt.sfdp_layout(ug, eweight = ug.ep.dist, K=K)

##


##
#offscreen = sys.argv[1] == "offscreen" if len(sys.argv) > 1 else False
max_count = 500
if offscreen and not os.path.exists("./frames"):
    os.mkdir("./frames")

# This creates a GTK+ window with the initial graph layout
if not offscreen:
    win = gt.GraphWindow(ug, pos, geometry=(800, 800), vertex_fill_color=ug.vp.lum,vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2))
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(800, 800)
    win.graph = gt.GraphWidget(ug, pos, vertex_fill_color=ug.vp.lum,vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2))
    win.add(win.graph)

count = 0
##
def update_state():

    global ibin
    global count

    edge_filter.a = ug.ep.dist.a < ibin
    ug.set_edge_filter(edge_filter)

    gt.sfdp_layout(ug, pos=pos, eweight = ug.ep.dist, K=K, init_step=step, max_iter=1)
    
    if count > 0 and count % 1000 == 0:
        win.graph.fit_to_window(ink=True)

    ibin += init_foot

    count += 1

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.regenerate_surface()
    win.graph.queue_draw()

    if offscreen:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r'./frames/dancing%06d.png' % count, 'png', [], [])
        if count > max_count:
            sys.exit(0)


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
