##
import os
import graph_tool.all as gt
import numpy as npr
import numpy.random as npr
import numpy.ma as npma
from numpy.linalg import norm
from pylab import *

##
#importing data

mass, lum, mag= loadtxt('new_data.txt', usecols=(2,3,4), unpack=True, skiprows=2)
                                     #building the graph
##
g = gt.Graph(directed=False)

Lum  = g.new_vertex_property('float')
Mag = g.new_vertex_property('float')
Mass = g.new_vertex_property('float')

g.vp.lum = Lum
g.vp.mag = Mag
g.vp.mass= Mass

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
mag-=min(mag); mag/=max(mag)
lum -= min(lum); lum /= max(lum)
mass-=min(mass); mass/=max(mass)

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
points[0,:]

##
g.vp.mag[0]


##
#def make_geograph(g, points, ibin):
#    L = []
#    for iv in range(g.num_vertices()):
#        vnbs = []
#        posv = np.array([g.vp.lum[iv], g.vp.mag[iv]])
#        for i, row in enumerate(points[:,:]):
#            #print(row)
#            if norm(posv - row) <= ibin:
#                if i != iv:
#                    vnbs.append(set([i, iv]))
#        L.append(vnbs)
#    for iv in range(g.num_vertices()):
#        for e in L[iv]:
#            g.add_edge(*e)
#
#    return g

##
import timeit
##

def make_geograph(g, points, ibin):
    L = []
    for iv in range(g.num_vertices()):
        posv = np.array([g.vp.lum[iv], g.vp.mag[iv]])
        for i, row in enumerate(points[:,:]):
            #print(row)
            if norm(posv - row) <= ibin:
                if i != iv:
                    L.append(set([i, iv]))
    
    for e in L:
        g.add_edge(*e)

    return g
##
g1 = make_geograph(g, points, ibin)

##


##
g1
##
gt.graph_draw(g1)
##
gg, gpos = gt.geometric_graph(points, ibin)
##
gt.graph_draw(gg)
##
gg.num_edges()

##
ug = gt.graph_union(gg, g, intersection = g.vertex_index, internal_props=True)
##
pos = gt.sfdp_layout(ug, K=K)
##
win = gt.GraphWindow(ug, pos, geometry=(500, 400), vertex_fill_color=ug.vp.lum,vertex_size=gt.prop_to_size(ug.vp.mass, mi=2, ma=10, log=False, power=2))
count = 0
##
##

import numpy as np

##
z = np.array([[0,4],[0,5],[3,5],[6,8],[9,1],[6,1], [6,1]])
rows=np.where(z[:,:]==np.array([6, 8]))
print(z[rows])
##
#for row in z[:,:]:
#    print(row == [6, 8])
##
rows
##
z[mask, :]

##