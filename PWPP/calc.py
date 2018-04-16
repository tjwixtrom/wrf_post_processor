# Calculations for output variables

import numpy as np
from wrf import getvar, ALL_TIMES
from metpy.calc import log_interp
from metpy.units import units
from .variable_def import get_variables


def get_isobaric_variables(data, var_list, plevs, outfile):
    """Gets isobaric variables from a list"""
    # use wrf-python to get data for each of the variables
    var_data = []
    var_def = get_variables()
    for name in var_list:
        var_data.append(getvar(data, var_def[name][2], ALL_TIMES))

    # convert data to numpy arrays
    var_data_np = [np.array(data) for data in var_data]

    # get pressure array and attach units
    p = getvar(data, 'p', ALL_TIMES)
    p_np = np.array(p) * units(p.units)
    iso_data = log_interp(plevs, p_np, *var_data_np, axis=1)

    # write each of the variables to the output file
    for i in range(len(var_list)):
        pres_data = outfile.createVariable(
                    var_list[i],
                    'f8',
                    ('Time', 'Pressure Levels', 'Latitude', 'Longitude'))
        pres_data.units = var_data[i].units
        pres_data.description = var_data[i].description
        pres_data[:] = iso_data[i]


def get_precip(data, outfile, RAINNC_out=False, RAINSH_out=False):
    """Gets the total precipitation from grid-scale and convective"""
    # Get grid-scale and convective precip, add for total precip
    grid_pcp = data.variables['RAINNC'][:] * units(data.variables['RAINNC'].units)
    conv_pcp = data.variables['RAINSH'][:] * units(data.variables['RAINSH'].units)
    tot_pcp = grid_pcp + conv_pcp

    pcp_data = outfile.createVariable(
                'tot_pcp',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    pcp_data.units = str(tot_pcp.units)
    pcp_data.description = 'Total Accumulated Precpitation'
    pcp_data[:] = tot_pcp.m

    if RAINNC_out:
        grid_pcp_data = outfile.createVariable(
                    'grid_pcp',
                    'f8',
                    ('Time', 'Latitude', 'Longitude'))
        grid_pcp_data.units = str(grid_pcp.units)
        grid_pcp_data.description = data.variables['RAINNC'].description
        grid_pcp_data[:] = grid_pcp.m

    if RAINSH_out:
        conv_pcp_data = outfile.createVariable(
                    'conv_pcp',
                    'f8',
                    ('Time', 'Latitude', 'Longitude'))
        conv_pcp_data.units = str(conv_pcp.units)
        conv_pcp_data.description = data.variables['RAINSH'].description
        conv_pcp_data[:] = conv_pcp.m


def get_timestep_precip(data, outfile):
    """Gets the precipitation accumulation for each timestep"""
    # Get grid-scale and convective precip, add for total precip
    grid_pcp = data.variables['RAINNC'][:] * units(data.variables['RAINNC'].units)
    conv_pcp = data.variables['RAINSH'][:] * units(data.variables['RAINSH'].units)
    tot_pcp = grid_pcp + conv_pcp

    # Calculate precip accumulation at each timestep
    ts_pcp = np.zeros(tot_pcp.shape)
    for i in range(tot_pcp.shape[0] - 1):
        ts_pcp[i + 1, ] = tot_pcp[i + 1, ] - tot_pcp[i, ]

    # Save to file
    pcp_data = outfile.createVariable(
                'APCP_03',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    pcp_data.units = str(tot_pcp.units)
    pcp_data.log_name = 'Timestep Precipitation Accumulation'
    pcp_data.level = 'A3'
    pcp_data.description = 'Total Timestep Accumulated Precpitation'
    pcp_data[:] = ts_pcp


def get_temp_2m(data, outfile):
    """Gets the 2m temperature data"""
    temp_2m = data.variables['T2'][:]
    temp_data = outfile.createVariable(
                'temp_2m',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    temp_data.units = data.variables['T2'].units
    temp_data.description = data.variables['T2'].description
    temp_data[:] = temp_2m


def get_q_2m(data, outfile):
    q_2m = data.variables['Q2'][:]
    q_data = outfile.createVariable(
                'q_2m',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    q_data.units = data.variables['Q2'].units
    q_data.description = data.variables['Q2'].description
    q_data[:] = q_2m


def get_v_10m(data, outfile):
    v_10m = data.variables['V10'][:]
    v_data = outfile.createVariable(
                'v_10m',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    v_data.units = data.variables['V10'].units
    v_data.description = data.variables['V10'].description
    v_data[:] = v_10m


def get_u_10m(data, outfile):
    u_10m = data.variables['U10'][:]
    u_data = outfile.createVariable(
                'u_10m',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    u_data.units = data.variables['U10'].units
    u_data.description = data.variables['U10'].description
    u_data[:] = u_10m


def get_mslp(data, outfile):
    slp = getvar(data, 'slp', ALL_TIMES)
    slp_data = outfile.createVariable(
                'mslp',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    slp_data.units = slp.units
    slp_data.description = slp.description
    slp_data[:] = slp


def get_uh(data, outfile):
    uh = getvar(data, 'updraft_helicity', ALL_TIMES)
    uh_data = outfile.createVariable(
                'UH',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    uh_data.units = uh.units
    uh_data.description = uh.description
    uh_data[:] = uh


def get_cape(data, outfile):
    capecin = getvar(data, 'cape_2d', ALL_TIMES)
    cape = np.array(capecin[0, ]) * units('J/kg')
    cin = np.array(capecin[1, ]) * units('J/kg')
    cape_data = outfile.createVariable(
                'cape',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    cape_data.units = str(cape.units)
    cape_data.description = '2D Convective Available Potential Energy'
    cape_data[:] = cape.m

    cin_data = outfile.createVariable(
                'cin',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    cin_data.units = str(cin.units)
    cin_data.description = '2D Convective Inhibition'
    cin_data[:] = cin.m


def get_dbz(data, outfile):
    dbz = getvar(data, 'mdbz', ALL_TIMES)
    dbz_data = outfile.createVariable(
                'DBZ',
                'f8',
                ('Time', 'Latitude', 'Longitude'))
    dbz_data.units = dbz.units
    dbz_data.description = dbz.description
    dbz_data[:] = dbz
