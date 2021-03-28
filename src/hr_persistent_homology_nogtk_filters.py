##
import os
import graph_tool.all as gt
from numpy.linalg import norm
from pylab import *
from datetime import datetime

##
# importing data
##

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

N = 500
v = g.add_vertex(N)

mag = mag[0:N]
lum = lum[0:N]
mass = mass[0:N]

# init_foot = 0.000001
# ibin = 0.000001
# fbin = 0.00002
init_foot = 0.000003
ibin = 0.000001
fbin = 0.2
step = 0.02  # move step
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
ug.num_edges()

##
distances = set_distances(ug)

edge_filter = ug.new_ep("bool")
ug.ep.efilter = edge_filter
ug.ep.efilter.a = ug.ep.dist.a < ibin
ug.set_edge_filter(edge_filter)
##
ug.num_edges()
##
pos = gt.sfdp_layout(ug, pos=ug.vp.pos, K=K)
ug.vp.pos = pos
##


def make_gif(g):
    global ibin, fbin, init_foot, step
    cbin = ibin
    graphs = [g.copy()]
    # pos = gt.sfdp_layout(g, pos=pos, K=1.5)
    while cbin <= fbin:
        g.ep.efilter.a = g.ep.dist.a < cbin
        g.set_edge_filter(g.ep.efilter)
        # print(g.num_edges())
        g.vp.pos = gt.sfdp_layout(g, pos=g.vp.pos, max_iter=1, init_step=step, K=K)
        graphs.append(g.copy())

        cbin += init_foot
        # step += init_foot * 3
    return graphs


##
glist = make_gif(ug)
##
def draw_frames(glist):
    stamp = datetime.strftime(datetime.now(), "%d_%h-%H-%M")
    outpath = f"./outputs_{stamp}"
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    for i, gu in enumerate(glist):
        gt.graph_draw(
            gu,
            pos=gu.vp.pos,
            vertex_fill_color=gu.vp.lum,
            edge_pen_width=0.5,
            vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2),
            output=os.path.join(outpath, "frame%06d.png" % i),
        )


##

draw_frames(glist)

##
