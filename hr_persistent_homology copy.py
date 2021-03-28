##
import os
import graph_tool.all as gt
import numpy as npr
import numpy.random as npr
from numpy.linalg import norm
from pylab import *
import cairo


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


##
g.vp.mass=Mass
g.vp.lum = Lum
g.vp.mag = Mag
g.vp.pos = pos
g.vp.pos_ = pos_


##
#global parameters

N=800
v = g.add_vertex(N)


a=1
b=0 

prop=g.vp.mag

mag =mag[0:N]
lum =lum[0:N]
mass =mass[0:N]

init_foot = 0.003
ibin =      0.003
fbin =      0.46

foot = (init_foot)*(10**a)
BIN = ibin - foot*b

draw = True


##
min(mag), max(mag)
min(lum), max(lum)
min(mass), max(mass)
##
#minmax scaling
mag-=min(mag);mag/=max(mag)
lum-=min(lum);lum/=max(lum)
mass-=min(mass);mass/=max(mass)

min(mag), max(mag)
min(lum), max(lum)
min(mass), max(mass)
##
#applying properties




for i, v in enumerate(g.vertices()):
    g.vp.mass[v]=mass[i]
    g.vp.lum[v]=lum[i]
    g.vp.mag[v]=mag[i]
    g.vp.pos[v] = np.array([mag[i], lum[i]])


##


##
posv = g.vp.pos.get_2d_array([0, 1]).T.copy()
##
gg, gpos = gt.geometric_graph(posv, ibin)
##
gu = gt.graph_union(gg, g, intersection=g.vertex_index, internal_props=True)


##
def make_gif(g, points, a, b, bin_step):
    ibin = a
    g.vp.pos = gt.sfdp_layout(g, K=0.5)
    graphs = [g]
    while ibin <= b:
        gg, gpos = gt.geometric_graph(points, ibin)

        gu=graphs[-1].copy()
        ggedgelist=gg.get_edges()
        guedgelist=gu.get_edges()
        for edge in ggedgelist:
            if not(edge in guedgelist):
                gu.add_edge(edge[0], edge[1]) 
        
        gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, max_iter=1, init_step=0.1, K=0.5)
        graphs.append(gu)
        
        ibin+=bin_step
    return graphs


##
graphlist = make_gif(gu, posv, ibin,fbin, init_foot)
##
for i, gu in enumerate(graphlist):
    gt.graph_draw(gu, pos=gu.vp.pos, vertex_fill_color=gu.vp.lum, edge_pen_width=0.5, vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2), output=f"draw {i}.png")



##

##
