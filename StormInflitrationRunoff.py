# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 01:44:29 2020

@author: yuvals
"""


import os
import numpy as np
from landlab.io import read_esri_ascii, write_esri_ascii
from landlab import imshow_grid_at_node
from landlab.components import SpatialPrecipitationDistribution
from landlab.components import OverlandFlow
import matplotlib.pyplot as plt
from landlab.components import SoilInfiltrationGreenAmpt
from landlab.components.uniform_precip import PrecipitationDistribution
import random
import matplotlib.pyplot as plt
import seaborn as sns


fname = 'hugo_site.asc'
mg, z = read_esri_ascii(fname, name='topographic__elevation')
mg.status_at_node[mg.nodes_at_right_edge] = mg.BC_NODE_IS_FIXED_VALUE
mg.status_at_node[np.isclose(z, -9999.)] = mg.BC_NODE_IS_CLOSED





## Inflitration component

hydraulic_conductivity = mg.ones('node')*1.e-6
hydraulic_conductivity.reshape(mg.shape)[0:2,:] *= 10000.
h = mg.add_ones("surface_water__depth", at="node")
mg.at_node['surface_water__depth'].fill(1.e-12)  # a veneer of water stabilises the model
h *= 0.01
d = mg.add_ones("soil_water_infiltration__depth", at="node", dtype=float)
d *= 0.2

## Initialization
SI = SoilInfiltrationGreenAmpt(mg,hydraulic_conductivity=hydraulic_conductivity)
of = OverlandFlow(mg, steep_slopes=True)

## Defiend param for the generator - i.e., rainfall scenario (Need to check the units)
mean_duration = 7 #hours
mean_inter_duration = 20  #hours
mean_depth = 0.5 # meters.
total_time  = 50 #hours
delta_t = 1; # 
np.random.seed(np.arange(10))

# Initialize generator
precip = PrecipitationDistribution(mg, mean_storm_duration=mean_duration, mean_interstorm_duration=mean_inter_duration, mean_storm_depth=mean_depth, total_t=total_time,delta_t=delta_t)
n = random.randint(1,101) ## random number for stochastic results.
precip.seed_generator(seedval=n)



for (storm_t, interstorm_dt) in precip.yield_storms():
    

    node_of_max_q = 2126
    total_mins_to_plot = 60  # in minutes.
    plot_interval_mins = 10.  
    min_tstep_val = 1.  # necessary to get the model going cleanly
    outlet_depth = []
    outlet_times = []
    storm_elapsed_time = 0.
    total_elapsed_time = 0.
    last_storm_loop_tracker = 0.
    while total_elapsed_time < total_mins_to_plot*60:
        dt = of.calc_time_step()
        remaining_total_time = total_mins_to_plot * 60. - total_elapsed_time
        if storm_elapsed_time < storm_t * 3600.:
            remaining_storm_time = storm_t * 3600. - storm_elapsed_time
            dt = min((dt, remaining_total_time, remaining_storm_time, min_tstep_val))
        else:
            dt = min((dt, remaining_total_time, min_tstep_val))
        of.run_one_step(dt=dt)
        SI.run_one_step(dt=dt) 
        total_elapsed_time += dt
        storm_elapsed_time += dt
        storm_loop_tracker = total_elapsed_time % (plot_interval_mins * 60.)
        # NB: Do NOT allow this plotting if there are multiple files in the folder
        if storm_loop_tracker < last_storm_loop_tracker:
            plt.figure()
            imshow_grid_at_node(
                mg,
                'surface_water__depth',
                var_name='Stage (m)')
            plt.title('Stage at t=' + str(total_elapsed_time//1) + 's')
            plt.show()
        last_storm_loop_tracker = storm_loop_tracker
        outlet_depth.append(mg.at_node['surface_water__depth'][node_of_max_q])
        outlet_times.append(total_elapsed_time)
        if storm_elapsed_time < storm_t * 3600.:
            mg.at_node['surface_water__depth'] += mg.at_grid['rainfall__flux'] * dt / 3600
            
    
plt.figure()
plt.plot(outlet_times, outlet_depth, '-')
plt.xlabel('Time elapsed (s)')
plt.ylabel('Flood stage (m)')
plt.plot(yuval1, yuval2, '-')

