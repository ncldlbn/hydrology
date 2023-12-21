#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions import discharge, get_water_level, get_reservoir_volume, turbining_rules, scenario_label, SCS_rainfall
from datetime import timedelta
import pandas as pd
import params as p
import argparse

# -----------------------------------------------------------------------------
# ARGUMENT PARSING
# -----------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='main.py --snow --scenario [1,2,3]')
parser.add_argument('--snow', action='store_true', help='Take into account snowfall precipitation')
args = parser.parse_args()

# Check snow argument: consider snowfall if True
if args.snow:
    snow = True
else:
    snow = False

# -----------------------------------------------------------------------------
# RUNOFF AND DISCHARGE MODELING
# -----------------------------------------------------------------------------
# Effective precipitation based on SCS method
Pe = SCS_rainfall(p.Hp, p.CN, p.beta)
print(f'Effective precipitation = {Pe} mm')

# Hydrograph estimation based on Linear Reservoir model
flow = discharge(Pe, snow, plot=True, save_csv=True)

# -----------------------------------------------------------------------------
# RESERVOIR MODELING
# -----------------------------------------------------------------------------
# init output dataframe
output = pd.DataFrame()

# loop over scenarios
scenario = [1,2,3]
for s in scenario:

    print('---------------------------')
    print(f'SCENARIO {s}: {scenario_label(s)}')
    
    # Volumes at t=0:
    # Initial reservoir volume
    V_0 = get_reservoir_volume(p.water_elev_t0)
    V_res = V_0
    # Cumulated loss volume (due to overflow)
    V_loss_tot = 0
    # Cumulated turbined volume
    V_turb_tot = 0
    
    # init result list
    result = []
    
    # loop over time from t=0 to t=sim_time
    for i in flow.index:
        data = {}
        
        # timestamp
        t = int(flow.loc[i, 't [hour]'])
        timestamp = p.start_date + timedelta(hours=t)
    
        # inflows and outflows
        Q_in = flow.loc[i, 'Q [m3/s]']
        Q_dmv = p.Q_dmv
        Q_turb = turbining_rules(s, timestamp)
        
        # Water balance
        balance = Q_in - Q_dmv - Q_turb
        V_res += balance*3600
        V_turb_tot += Q_turb*3600
        
        # Volume loss
        if V_res > p.max_volume:
            V_loss = V_res - p.max_volume
            V_res = V_res - V_loss
        else:
            V_loss = 0
        V_loss_tot += V_loss
        
        # append data to result list
        data['timestamp'] = timestamp
        data['Q_in [m3/s]'] = round(Q_in,1)
        data['Q_dmv [m3/s]'] = round(Q_dmv,1)
        data['Q_t [m3/s]'] = round(Q_turb,1)
        data['Water balance [m3/s]'] = round(balance,1)
        data['Reservoir Volume [m3]'] = round(V_res)
        data['Water level [m slm]'] = get_water_level(V_res/1e6)
        data['Volume loss [m3]'] = round(V_loss)
        data['Overflow [m3/s]'] = round(V_loss/3600,1)
        data['Cum Volume loss [m3]'] = round(V_loss_tot)
        data['Cum Volume turb [m3'] = round(V_turb_tot)
        result.append(data)
        
    # save complete results to csv for each scenario
    dfout = pd.DataFrame(result)
    if snow == True:
        dfout.to_csv(f'{p.out_path}detailed-output/scenario_{s}_snow.csv', index=False)
    else:
        dfout.to_csv(f'{p.out_path}detailed-output/scenario_{s}.csv', index=False)
    
    # append results to output dataframe
    # output dataframe has only water level and volume loss
    output[f'{scenario_label(s)} - Water level [m slm]'] = dfout['Water level [m slm]']
    output[f'{scenario_label(s)} - Overflow [m3/s]'] = dfout['Overflow [m3/s]']
    
    # If overflow occurs, then calculate water level at t=0 to avoid overflow
    if V_loss_tot > 0:
        water_level_no_overflow = get_water_level((V_0-V_loss_tot)/1e6)
        print(f'Overflow volume: {round(V_loss_tot)} m3')
        print(f'Water level at t=0 to avoid overflow: {water_level_no_overflow} m slm')
    else:
        print('No overflow')

print('---------------------------')

# save output to csv file as requested
if snow == True:
    output.to_csv(f'{p.out_path}output_snow.csv')
else:
    output.to_csv(f'{p.out_path}output.csv')
