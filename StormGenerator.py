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

## Create Grid - !! later we can load a real ascii file
mg = RasterModelGrid((4, 5))

## Defiend param for the generator - i.e., rainfall scenario (Need to check the units)
mean_duration = 50 
mean_inter_duration = 20
mean_depth = 0.5
total_time  = 60*24*30 #60 min * 24 hours * 30 days
delta_t = 1;
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

## Iterating over all of the storms.
for (storm_dt, interstorm_dt) in precip.yield_storms():
    storm_dts.append(np.array(storm_dt))
    interstorm_dts.append(interstorm_dt)
    intensities.append(mg.at_grid['rainfall__flux'])
        
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
    
## Plotting the rainfall series
plt.plot(rain_sequence)
plt.xlabel('Duration [min]')
plt.ylabel('Storm depth [?]')
    