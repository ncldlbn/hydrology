#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

# --------------------------------------------------------------------------- #
# PATHS AND FILENAMES
in_path = '../data/in/'
out_path = '../data/out/'
hypsometric = in_path + 'hypsometric-curve.csv'
reservoir_curve = in_path + 'reservoir-elevation-volume.csv'

# --------------------------------------------------------------------------- #
# BASIN PARAMS
basin_area = 200 # basin area [km2]

# Hypotesis -------------------------------------- #
avg_i = 0.02 # average main river slope [-]        
CN = 100     # average basin Curve Number [0-100]  
beta = 0.2   # initial loss coefficient [-]

# --------------------------------------------------------------------------- #
# PRECIPITATION PARAMS
Hp = 120         # total rainfall height [mm]
Tp = 24          # rainfall duration [hours]
snow_elev = 1200 # snowfall elevation [m slm]

# --------------------------------------------------------------------------- #
# RESERVOIR PARAMS
max_volume = 40e6   # max reservoir volume [m3]
water_elev_t0 = 823 # water elevation at t=0 [m slm]
overflow_elev = 830 # overflow elevation [m slm]

# Hypotesis -------------------------------------- #
Q_dmv = 2    # environmental flow [m3/s]

# --------------------------------------------------------------------------- #
# TURBINING PARAMS
Tmax = 16   # maximum discharge for the turbine [m3/s]
Tord = 12   # ordinary discharge for the turbine [m3/s]
Tstart = 10 # ordinary turbining start time [HH]
Tend = 18   # ordinary turbining end time [HH]

# --------------------------------------------------------------------------- #
# MODELING PARAMS
sim_time = 72 # simulation time length [hours]
start_date = datetime(2023, 1, 1)

# --------------------------------------------------------------------------- #
