##
import graph_tool.all as gt
import matplotlib
from numpy.random import *
import sys, os, os.path
from gi.repository import Gtk, Gdk, GdkPixbuf, GObject, GLib

g = gt.collection.data["football"]

max_count = 200
offscreen = True
if offscreen and not os.path.exists("./frames"):
    os.mkdir("./frames")
state = gt.IsingGlauberState(g, beta=1.5 / 10)
if not offscreen:
    win = gt.GraphWindow(
        g, g.vp.pos, vertex_fill_color=state.get_state(), geometry=(800, 800)
    )
else:
    win = Gtk.OffscreenWindow()
    win.set_default_size(800, 800)
    win.graph = gt.GraphWidget(g, g.vp.pos, vertex_fill_color=state.get_state())
    win.add(win.graph)

##
# ret = state.iterate_sync(niter=100)
count = 1


def update_state():
    global count
    count += 1

    ret = state.iterate_sync(niter=1)
    win.graph.regenerate_surface()
    win.graph.queue_draw()

    pixbuf = win.get_pixbuf()
    pixbuf.savev(r"./frames/dancing%06d.png" % count, "png", [], [])

    if count > max_count:
        sys.exit(0)

    return True


cid = GLib.idle_add(update_state)

# We will give the user the ability to stop the program by closing the window.
win.connect("delete_event", Gtk.main_quit)

# Actually show the window, and start the main loop.
win.show_all()
Gtk.main()
##

##
