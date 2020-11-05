# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:30:52 2020

@author: yuvals
"""


############## Rainstorms generator #######################3

## load pkg
from landlab.components.uniform_precip import PrecipitationDistribution
import numpy as np
from landlab import RasterModelGrid
import random
import matplotlib.pyplot as plt
import seaborn as sns
from landlab.components import SoilInfiltrationGreenAmpt
from landlab.components.overland_flow import OverlandFlow
from landlab.plot.imshow import imshow_grid
from landlab.io import read_esri_ascii, write_esri_ascii
from landlab import imshow_grid_at_node


## Create Grid - !! later we can load a real ascii file
#mg = RasterModelGrid((4, 5))

fname = 'hugo_site.asc'
mg, z = read_esri_ascii(fname, name='topographic__elevation')
mg.status_at_node[mg.nodes_at_right_edge] = mg.BC_NODE_IS_FIXED_VALUE
mg.status_at_node[np.isclose(z, -9999.)] = mg.BC_NODE_IS_CLOSED



h = mg.add_ones("surface_water__depth", at="node")
h *= 0.01 # in meters
#mg.add_zeros("topographic__elevation", at="node")
d = mg.add_ones("soil_water_infiltration__depth", at="node",dtype = float)
d *= 0.2 # in meters
HC = mg.ones('node')*1**-6  ## meter per sec

## Defiend param for the generator - i.e., rainfall scenario (Need to check the units)
mean_duration = 6 #hours
mean_inter_duration = 20  #hours
mean_depth = 0.5
total_time  = 24*30 #hours
delta_t = 1; # sec
np.random.seed(np.arange(10))

# Initialize generator
precip = PrecipitationDistribution(mg, mean_storm_duration=mean_duration, mean_interstorm_duration=mean_inter_duration, mean_storm_depth=mean_depth, total_t=total_time,delta_t=delta_t)
n = random.randint(1,101) ## random number for stochastic results.
precip.seed_generator(seedval=n)

## Arrays for saving the outputs.
storm_dts = []
interstorm_dts = []
intensities = []
storm_dts = []


node_of_max_q = 2126
## Iterating over all of the storms.
for (storm_dt, interstorm_dt) in precip.yield_storms():
        ## Save rainfall data
    #intensities = mg.at_grid['rainfall__flux']
    storm_dts.append(np.array(storm_dt))
    interstorm_dts.append(interstorm_dt)
    intensities.append(mg.at_grid['rainfall__flux']) ## mm/minute
    
    
    
number_of_storms = str(len(storm_dts))
    
## This is ugly but just for now:    
storm_dts = np.asanyarray(storm_dts)
interstorm_dts = np.asanyarray(interstorm_dts)
intensities = np.asanyarray(intensities)

## Building a  time-series rainfall vector for the total month.
rain_sequence = []
for i in range(0,len(storm_dts)):
    storm = np.ones(int(np.round(storm_dts[i])))*intensities[i]
    rain_sequence.extend(storm)
    interstorm = np.ones(int(np.round(interstorm_dts[i])))*0
    rain_sequence.extend(interstorm)



    
## Plotting the full rainfall series
figure ,ax = plt.subplots()
plt.plot(np.asanyarray(rain_sequence)*60) ## In mm/h 
plt.xlabel('Time')
plt.ylabel('Rainfall intensity [mm $h^{-1}]$')
plt.text(0.2, 0.9,'Number of storms: ' + number_of_storms, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
## 


## Plotting kernel density of storm duration
figure ,ax = plt.subplots()
ax = sns.kdeplot(intensities,color='blue')
ax = sns.kdeplot(intensities,color = 'r')
#plt.hist(storm_dts)
plt.xlabel('Storm duration [min]')
plt.ylabel('Density')
plt.legend()
##


## Plotting rainstorm depth CDF-plot
figure ,ax = plt.subplots()
hist, bin_edges = np.histogram(intensities, normed=True)
b = [0]
b.extend(np.cumsum(hist)/np.sum(hist))
plt.plot(bin_edges,b,color='b',label='Scenario #2')
hist, bin_edges = np.histogram(intensities, normed=True)
b = [0]
b.extend(np.cumsum(hist)/np.sum(hist))
plt.plot(bin_edges,b,color='r',label='Scenario #1')
plt.xlabel('Storm depth [m]')
plt.ylabel('F(x)')
ax.legend()
##
