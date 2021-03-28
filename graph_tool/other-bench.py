##
import os
import graph_tool.all as gt
import numpy as np
import numpy as npr
import numpy.random as npr
from numpy.linalg import norm

##
g = gt.Graph(directed=False)
N = 100
v = g.add_vertex(N)
##

pos = g.new_vertex_property('vector<double>')
g.vp["pos"] = pos
##
poss = npr.randn(2, 100)
pos.set_2d_array(poss)

##
avg_vec = np.average(poss, axis=1)
##
avg_dists = []
for pos in g.vp.pos:
    avg_dists.append(norm(pos - avg_vec))

ibin = sum(avg_dists) / len(avg_dists)
##
ibin
##
np.array(g.vp.pos[1]) - np.array(g.vp.pos[0])
##
np.array(g.vp.pos[1]), np.array(g.vp.pos[0])
##
for iv in range(g.num_vertices()):
        for iu in range(g.num_vertices()):
            dist = norm(np.array(g.vp.pos[iv]) - np.array(g.vp.pos[iu]))
            if dist <= ibin:
                print(iv, iu, dist)
##
def make_geograph(g, ibin):
    g = g.copy()
    L = []
    for iv in range(g.num_vertices()):
        for iu in range(g.num_vertices()):
            if norm(np.array(g.vp.pos[iv]) - np.array(g.vp.pos[iu])) < ibin:
                if iu != iv:
                    L.append(set([iu, iv]))
    L_ = [tuple(e) for e in L]
    L_ = set(L_)
    for e in L_:
        g.add_edge(*e)

    return g
##
g1 = make_geograph(g, ibin)
##
g1.num_edges()
##
g.num_edges()
##
gt.graph_draw(g1)
##
points = g.vp.pos.get_2d_array([0, 1]).T
##
points
##
points[0,:]
##
g.vp.pos[0]
##

type(points[1,:])
##
gg, gpos = gt.geometric_graph(points, ibin)



##
gg.num_edges()
##
import timeit
##
g = gt.Graph(directed=False)
N = 100
v = g.add_vertex(N)


pos = g.new_vertex_property('vector<double>')
g.vp["pos"] = pos

poss = npr.randn(2, 100)
pos.set_2d_array(poss)


avg_vec = np.average(poss, axis=1)

avg_dists = []
for pos in g.vp.pos:
    avg_dists.append(norm(pos - avg_vec))

ibin = sum(avg_dists) / len(avg_dists)
##

def time_mine():
    make_geograph(g, ibin)
##

import time
##
timergt = timeit.Timer(lambda: gt.geometric_graph(points, ibin))
##
timergt.repeat(repeat=10, number=3)
##
timermine = timeit.Timer(lambda: make_geograph(g, ibin))

##
timermine.repeat(repeat=10, number=3)
##
