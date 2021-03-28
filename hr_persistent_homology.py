##
import os
##
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

N=1400
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
fbin =      0.21

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
gtdraw = gt.graph_draw(g, pos=g.vp.pos, vertex_fill_color=g.vp.lum,vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2))

##
posv = g.vp.pos.get_2d_array([0, 1]).T
##
gg, gpos = gt.geometric_graph(posv, ibin)
##
gu = gt.graph_union(gg, g, intersection=g.vertex_index, internal_props=True)
##
gu.copy_property(gpos, tgt=gu.vp.pos, g=gg)

##
gt.graph_draw(gu, pos=gu.vp.pos, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))
##
gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, K=1.5)
##
gt.graph_draw(gu, pos=gu.vp.pos, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))

##
#gt.graph_draw(gu, pos=gu.vp.pos_, vertex_fill_color=gu.vp.lum,vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2))


##
def make_gif(g, points, a, b, step):
    bin = a
    g.vp.pos_ = gt.sfdp_layout(g, pos=g.vp.pos, K=1.5)
    graphs = [g]
    while bin <= b:
        gg, gpos = gt.geometric_graph(points, bin)

        gu=graphs[-1].copy()
        ggedgelist=gg.get_edges()
        guedgelist=gu.get_edges()
        for edge in ggedgelist:
            if not(edge in guedgelist):
                gu.add_edge(edge[0], edge[1]) 
        gu.vp.pos_ = gt.sfdp_layout(gu, pos=gu.vp.pos_, max_iter=8, init_step=0.5, K=1.5)
        graphs.append(gu)
        
        bin+=step
    return graphs


##
graphlist = make_gif(gu, posv, ibin,fbin, init_foot)


##
for i, gu in enumerate(graphlist):
    gt.graph_draw(gu, pos=gu.vp.pos_, vertex_fill_color=gu.vp.lum,edge_color= "white", edge_pen_width=0.5, vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2), output="draw %i.png" %i)


