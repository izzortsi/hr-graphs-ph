'''
 NAME:                simple_plot_9_python
 
 DESCRIPTION:         Displays a Hertzsprung-Russell diagram.

 EXECUTION COMMAND:
                      > python simple_plot_9_python

 INPUTS:              Six theoretical models M???Z14V0.dat.txt
                      from http://obswww.unige.ch/Recherche/evol/

 OUTPUTS:             PDF file: python_plot.pdf

 NOTES:               change the input data. 
                      change the output PDF name.

 AUTHOR:              Leonardo UBEDA
                      Space Telescope Science Institute, USA 
 
 REVISION HISTORY:
                      Written by Leonardo UBEDA, Jan 2012. 

'''

# ------------------------ python code begins here


#!/usr/bin/env python

# name the output file 
pdfname = 'python_plot.pdf'


# import packages

import sys, os
from numpy.random import * 
from graph_tool.all import *
import graph_tool.all as gt
from numpy import *
from pylab import *
import matplotlib.pyplot as plt
from matplotlib import *
import itertools
# read input files: luminosity and effective temperature
mass001,lum001, teff001 = loadtxt('M001Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)
mass002,lum002, teff002 = loadtxt('M002Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)
mass005,lum005, teff005 = loadtxt('M005Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)
mass020,lum020, teff020 = loadtxt('M020Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)
mass040,lum040, teff040 = loadtxt('M040Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)
mass060,lum060, teff060 = loadtxt('M060Z14V0.dat.txt', usecols=(2, 3, 4), unpack=True, skiprows=2)

lum=np.vstack((lum001,np.vstack((lum002,np.vstack((lum005,np.vstack((lum020,np.vstack((lum040,lum060))))))))))
teff=np.vstack((teff001,np.vstack((teff002,np.vstack((teff005,np.vstack((teff020,np.vstack((teff040,teff060))))))))))
mass=np.vstack((mass001,np.vstack((mass002,np.vstack((mass005,np.vstack((mass020,np.vstack((mass040,mass060))))))))))
# create plot
fig = plt.figure(figsize = (7,9), dpi = 120)
plot = plt.plot(teff, lum,".")


xlabel(r'$\log(T_{eff} [K])$')
ylabel(r'$\log(L/L_{\odot})$')
ylim([-0.5, 6.3])
xlim([5.0, 3.4])

# make some annotations
txt = plt.text(4.35, 2.5, r'$5 M_{\odot}$')
txt = plt.text(4.65, 4.4, r'$20 M_{\odot}$')

# close and save file 
savefig(pdfname) 
clf()

g=Graph(directed=False)
Mass = g.new_vertex_property('float')
g.vp['Mass']=Mass
Lum  = g.new_vertex_property('float')
Mag = g.new_vertex_property('float')
pos = g.new_vertex_property('vector<float>')
Rs = g.new_vertex_property('float')
g.vp['Rs']=Rs

v = g.add_vertex(2320)

for i in g.vertices():
    Mass[i]=mass[i]
    Lum[i]=lum[i]
    Mag[i]=mag[i]
    pos[i] = np.array([Mag[i],Lum[i]]) 


# ------------------------ python code ends here
