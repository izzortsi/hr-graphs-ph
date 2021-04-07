##
import os
import graph_tool.all as gt
from pylab import *
from datetime import datetime

##
# importing data
##
stamp = datetime.strftime(datetime.now(), "%d_%h-%H-%M")
##
offscreen = True
max_count = 30
outpath = f"./outputs_{stamp}"
if offscreen and not os.path.exists(outpath):
    os.mkdir(outpath)

mass, lum, mag = loadtxt("new_data.txt", usecols=(2, 3, 4), unpack=True, skiprows=2)
g = gt.Graph(directed=False)

Mass = g.new_vertex_property("float")
Lum = g.new_vertex_property("float")
Mag = g.new_vertex_property("float")
pos = g.new_vertex_property("vector<float>")

##
g.vp.mass = Mass
g.vp.lum = Lum
g.vp.mag = Mag
g.vp.pos = pos

##
# global parameters

N = 2300
v = g.add_vertex(N)

mag = mag[0:N]
lum = lum[0:N]
mass = mass[0:N]

init_foot = 0.001
ibin = 0.001
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
gtdraw = gt.graph_draw(
    g,
    pos=g.vp.pos,
    vertex_fill_color=g.vp.lum,
    vertex_size=gt.prop_to_size(g.vp.mass, mi=3, ma=9.5, log=False, power=2),
    output=os.path.join(outpath, "HR_diag.png"),
)
##
posv = g.vp.pos.get_2d_array([0, 1]).T
##
gg, gpos = gt.geometric_graph(posv, ibin)
##
gu = gt.graph_union(gg, g, intersection=g.vertex_index, internal_props=True)
##
gt.graph_draw(
    gu,
    pos=gu.vp.pos,
    vertex_fill_color=gu.vp.lum,
    vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2),
    output=os.path.join(outpath, f"HR_diag_edges_{ibin}.png"),
)
##
gu.vp.pos = gt.sfdp_layout(gu, pos=gu.vp.pos, K=1.5)
##
gt.graph_draw(
    gu,
    pos=gu.vp.pos,
    vertex_fill_color=gu.vp.lum,
    vertex_size=gt.prop_to_size(gu.vp.mass, mi=2, ma=10, log=False, power=2),
    output=os.path.join(outpath, f"HR_sfdp{ibin}.png"),
)
##
