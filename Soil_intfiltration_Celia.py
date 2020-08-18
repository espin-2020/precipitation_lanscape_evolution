#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:06:43 2020

@author: cctrunz
"""

from landlab import RasterModelGrid
from landlab.components import SoilInfiltrationGreenAmpt
mg = RasterModelGrid((4,3), xy_spacing=10.)
hydraulic_conductivity = mg.ones('node')*1.e-6
hydraulic_conductivity.reshape((4,3))[0:2,:] *= 10000.
h = mg.add_ones("surface_water__depth", at="node")
h *= 0.01
d = mg.add_ones("soil_water_infiltration__depth", at="node", dtype=float)
d *= 0.2
SI = SoilInfiltrationGreenAmpt(
    mg,hydraulic_conductivity=hydraulic_conductivity)

for i in range(10):  # 100s total
    SI.run_one_step(10.)
    
    
    
mg.at_node['surface_water__depth']
# array([  1.00000000e-08,   1.00000000e-08,   1.00000000e-08,
#          1.00000000e-08,   1.00000000e-08,   1.00000000e-08,
#          9.88530416e-03,   9.88530416e-03,   9.88530416e-03,
#          9.88530416e-03,   9.88530416e-03,   9.88530416e-03])
mg.at_node['soil_water_infiltration__depth']
# array([ 0.20999999,  0.20999999,  0.20999999,  0.20999999,  0.20999999,
#         0.20999999,  0.2001147 ,  0.2001147 ,  0.2001147 ,  0.2001147 ,
#         0.2001147 ,  0.2001147 ])


SoilInfiltrationGreenAmpt.input_var_names