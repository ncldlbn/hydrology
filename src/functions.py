#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import params as p
import pandas as pd
import numpy as np
import math
import sys
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Calculate effective area from hypsometric curve
    # hypsometric_csv = hypsometric csv path
    # snowfall = true/false - for taking into account of snowfall precipitation
def effective_area(hypsometric_csv, snowfall):
    # read hypsometric curve data
    data = pd.read_csv(p.hypsometric)
    # cumulated area
    data['cum_area'] = data['cum_area%']*p.basin_area*1e6
    data['area_k'] = data['cum_area'].diff()
    # calculate effective area
    if snowfall == True:
        area = int(data.loc[data['Elevation'] == p.snow_elev, 'cum_area'].values)/1e6
    else:
        area = p.basin_area
        
    return area

# Time of concentration from Ventura formula
    # area = basin area in km2
    # avg_i = average main river slope [-]
    # snowfall = true/false - for taking into account of snowfall precipitation
def Ventura(area, avg_i, snowfall):
    tc = 0.127*(area**0.5)/(avg_i**0.5)
    
    return round(tc, 2)

# Effective precipitation estimated from SCS method
    # Hp = total precipitaion height [mm]
    # Tp = rainfall duration [hours]
    # CN = Curve Number
    # beta = initial loss coefficient
def SCS_rainfall(P, CN, beta):
    S = 25.4*(1000/CN - 10)
    
    if(P > beta*S):
        P_eff = ((P - beta*S)**2)/(P + (1-beta)*S)
    else:
        P_eff = 0
    
    return round(P_eff,1)

# Hydrograph estimation, based on Linear Reservoir model
    # Pe = effective precipitation
    # snowfall = True/False - for taking into account snowfall precipitation
    # plot = True/False to save hydrograph plot in output folder
    # save_csv = True/False to save hydrograph data in output folder
def discharge(pe, snowfall, plot=True, save_csv=True): 
    area = effective_area(p.hypsometric, snowfall)
    print(f'Effective area = {area} km2')
    Tc = Ventura(area, p.avg_i, snowfall)
    print(f'Tc = {Tc} hours')
    
    # time series
    tn = np.arange(0, p.sim_time+1)
    # coefficiente di invaso
    k = 0.7*Tc
    # effective precipitation rate
    ie = (pe/p.Tp)*0.001 # from mm/h to m/h
    # runoff volume rate
    iA = ie*area*1e6 # m3/h
    # init output df
    output = pd.DataFrame({'t [hour]': tn})
    
    # Linear Reservoir model: from t=0 to t=tp flow is increasing
    for t in range(0,p.Tp):
        output.loc[t, 'Q [m3/s]'] = (iA*(1-math.e**(-t/k)))/3600
    # Linear Reservoir model: from t=tp to t=sim_time flow is decreasing
    Qmax = output['Q [m3/s]'].max()
    for t in range(p.Tp, p.sim_time+1):
        output.loc[t, 'Q [m3/s]'] = Qmax*math.e**(-(t-p.Tp)/k)
        
    if plot == True:
        # save hydrograph plot
        plt.figure(figsize=(15, 8))
        plt.plot(output['t [hour]'], output['Q [m3/s]'], marker='o', label='Q', color='blue')
        plt.xlabel('t [hours]')
        plt.ylabel('Q [m3/s]')
        plt.title("Hydrograph")
        plt.grid(True)
        plt.savefig(p.out_path + 'detailed-output/hydrograph.png')
        
    if save_csv == True:
        # save hydrograph data as csv
        output['Q [m3/s]'] = round(output['Q [m3/s]'], 2)
        output.to_csv((p.out_path + 'detailed-output/hydrograph.csv'), index=False)

    return output

# Read reservoir Volume-Elevation data, interpolate and get elevation given volume
def get_water_level(volume):
    # read reservoir curve data
    r = pd.read_csv(p.reservoir_curve)
    # get Volume-Elevation function
    f1 = interp1d(r['Volume'], r['Elevation'], kind='linear', fill_value='extrapolate')
    # get elevation from volume
    elevation = np.round(f1(volume),2)
    
    return elevation

# Read reservoir Volume-Elevation data, interpolate and get volume given elevation
def get_reservoir_volume(elevation):
    # read reservoir curve data
    r = pd.read_csv(p.reservoir_curve)
    # get reservoir volume from elevation
    coeff = np.polyfit(r['Elevation'], r['Volume'], 3)
    # get Elevation-Volume function
    f2 = np.poly1d(coeff)
    # get volume from elevation
    volume = round(f2(elevation)*1e6)
    
    return volume

# Defining turbining flow rate based on given scenario id
    # scenario = 1, 2 or 3
    # time = time of the day
def turbining_rules(scenario, time):
    # Turbining flow and volume
    if scenario == 3:
        # if scenario == 3, then time of the day is needed
        if time.hour >= p.Tstart and time.hour < p.Tend:
            Q_t = p.Tord
        else:
            Q_t = 0
    elif scenario == 2:
        Q_t = p.Tmax
    elif scenario == 1:
        Q_t = 0
    else:
        print("Scenario must be 1, 2 or 3")
        sys.exit(1)
        
    return Q_t

# Get scenario label given scenario id
    # scenario = 1, 2 or 3
def scenario_label(scenario):     
    if scenario == 1:
        label = 'T_0'
    elif scenario == 2:
        label = 'T_MAX'
    elif scenario == 3:
        label = 'T_ORD'
    else:
        print("Scenario must be 1, 2 or 3")
        sys.exit(1)
        
    return label