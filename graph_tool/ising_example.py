##
import graph_tool.all as gt
import matplotlib
from numpy.random import *
import sys, os, os.path
##
g = gt.collection.data["football"]
state = gt.IsingGlauberState(g, beta=1.5/10)
win = None
for i in range(100):
    ret = state.iterate_sync(niter=100)
    win = gt.graph_draw(g, g.vp.pos, vertex_fill_color=state.get_state(),
                        vcmap=matplotlib.cm.bone_r, window=win, return_window=True,
                        main=False)
##
