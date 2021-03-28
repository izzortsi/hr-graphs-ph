##
import os
import graph_tool.all as gt
from numpy.linalg import norm
from pylab import *
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib


##
# importing data

offscreen = True
max_count = 30
outpath = "./outputs_2"
if offscreen and not os.path.exists(outpath):
    os.mkdir(outpath)
##
mass, lum, mag = loadtxt("new_data.txt", usecols=(2, 3, 4), unpack=True, skiprows=2)
# building the graph


g = gt.Graph(directed=False)

Lum = g.new_vertex_property("float")
Mag = g.new_vertex_property("float")
Mass = g.new_vertex_property("float")
Position = g.new_vp("vector<double>")
Distance = g.new_edge_property("float")

g.vp.lum = Lum
g.vp.mag = Mag
g.vp.mass = Mass
g.vp.pos = Position
g.ep.dist = Distance

N = 2000
v = g.add_vertex(N)

mag = mag[0:N]
lum = lum[0:N]
mass = mass[0:N]

init_foot = 0.000001
ibin = 0.000001
fbin = 0.21

step = 0.05  # move step
K = 0.5

##
# minmax scaling
mag -= min(mag)
mag /= max(mag)
lum -= min(lum)
lum /= max(lum)
mass -= min(mass)
mass /= max(mass)
##
# applying properties
for i, v in enumerate(g.vertices()):
    g.vp.mass[v] = mass[i]
    g.vp.lum[v] = lum[i]
    g.vp.mag[v] = mag[i]
    g.vp.pos[v] = np.array([mag[i], -lum[i]])

##
posv = g.vp.pos.get_2d_array([0, 1]).T
##
gg, gpos = gt.geometric_graph(posv, fbin)
##
ug = gt.graph_union(gg, g, intersection=g.vertex_index, internal_props=True)
##

# g.copy_property(gpos, g.vp.pos)
##
def set_distances(g):
    dists = []
    for e in ug.edges():
        s, t = e
        pos_s = np.array(g.vp.pos[s])
        pos_t = np.array(g.vp.pos[t])
        distance = norm(pos_s - pos_t)
        # print(distance)
        dists.append(distance)
        g.ep.dist[e] = distance
    return dists


##
distances = set_distances(ug)

edge_filter = ug.new_ep("bool")
edge_filter.a = ug.ep.dist.a < ibin
ug.set_edge_filter(edge_filter)
##
pos = gt.sfdp_layout(ug, pos=ug.vp.pos, K=K)

##


##
# offscreen = sys.argv[1] == "offscreen" if len(sys.argv) > 1 else False


# This creates a GTK+ window with the initial graph layout
if not offscreen:
    win = gt.GraphWindow(
        ug,
        pos,
        geometry=(800, 800),
        vertex_fill_color=ug.vp.lum,
        vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2),
    )
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(800, 800)
    win.graph = gt.GraphWidget(
        ug,
        pos,
        vertex_fill_color=ug.vp.lum,
        vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2),
    )
    win.add(win.graph)

count = 0
##
def update_state():

    global ibin
    global count
    global step

    edge_filter.a = ug.ep.dist.a < ibin
    ug.set_edge_filter(edge_filter)

    gt.sfdp_layout(ug, pos=pos, K=K, init_step=step, max_iter=1)

    if count > 0 and count % 1000 == 0:
        win.graph.fit_to_window(ink=True)

    ibin += init_foot
    step += init_foot * 3
    count += 1

    # The following will force the re-drawing of the graph, and issue a
    # re-drawing of the GTK window.
    win.graph.regenerate_surface()
    win.graph.queue_draw()

    if offscreen:
        pixbuf = win.get_pixbuf()
        pixbuf.savev(r"%s/frame%06d.png" % (outpath, count), "png", [], [])
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
