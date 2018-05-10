# Calculations for output variables

import numpy as np
from wrf import getvar, ALL_TIMES
from metpy.calc import log_interp
from metpy.units import units
from .variable_def import get_variables


def get_isobaric_variables(data, var_list, plevs, outfile, dtype, compression,
                           complevel, nproc):
    """Gets isobaric variables from a list"""
    # use wrf-python to get data for each of the variables
    var_def = get_variables()

    # get pressure array and attach units
    p = getvar(data, 'p', ALL_TIMES)
    p_np = np.array(p) * units(p.units)

    # write each of the variables to the output file
    def _pres_data_(data, plevs, p_np, var_list, i):
        var_data = getvar(data, var_def[var_list[i]][2], ALL_TIMES)
        var_data_np = np.array(var_data)
        iso_data = log_interp(plevs, p_np, var_data_np, axis=1)
        pres_data = outfile.createVariable(
                    var_list[i],
                    dtype,
                    ('time', 'pressure_levels', 'lat', 'lon'),
                    zlib=compression, complevel=complevel)
        pres_data.units = var_data[i].units
        if var_list[i] == 'height':
            pres_data.decription = 'height [MSL] of isobaric surfaces'
        elif var_list[i] == 'uwnd':
            pres_data.description = 'u-wind component on isobaric surfaces'
        elif var_list[i] == 'vwnd':
            pres_data.description = 'v-wind component on isobaric surfaces'
        elif var_list[i] == 'wwnd':
            pres_data.description = 'w-wind component on isobaric surfaces'
        elif var_list[i] == 'temp':
            pres_data.description = 'temperature on isobaric surfaces'
        elif var_list[i] == 'dewpt':
            pres_data.description = 'dewpoint temperature on isobaric surfaces'
        elif var_list[i] == 'avor':
            pres_data.description = 'absolute vorticity on isobaric surfaces'
        else:
            pres_data.description = var_data.description
        pres_data[:] = iso_data

    for i in range(len(var_list)):
        _pres_data_(data, plevs, p_np, var_list, i)


def get_precip(data, outfile, dtype, compression, complevel,
               RAINNC_out=False, RAINSH_out=False):
    """Gets the total precipitation from grid-scale and convective"""
    # Get grid-scale and convective precip, add for total precip
    grid_pcp = data.variables['RAINNC'][:] * units(data.variables['RAINNC'].units)
    conv_pcp = data.variables['RAINSH'][:] * units(data.variables['RAINSH'].units)
    tot_pcp = grid_pcp + conv_pcp

    pcp_data = outfile.createVariable(
                'tot_pcp',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    pcp_data.units = str(tot_pcp.units)
    pcp_data.description = 'Total Accumulated Precpitation'
    pcp_data[:] = tot_pcp.m

    if RAINNC_out:
        grid_pcp_data = outfile.createVariable(
                    'grid_pcp',
                    dtype,
                    ('time', 'lat', 'lon'),
                    zlib=compression, complevel=complevel)
        grid_pcp_data.units = str(grid_pcp.units)
        grid_pcp_data.description = data.variables['RAINNC'].description
        grid_pcp_data[:] = grid_pcp.m

    if RAINSH_out:
        conv_pcp_data = outfile.createVariable(
                    'conv_pcp',
                    dtype,
                    ('time', 'lat', 'lon'),
                    zlib=compression, complevel=complevel)
        conv_pcp_data.units = str(conv_pcp.units)
        conv_pcp_data.description = data.variables['RAINSH'].description
        conv_pcp_data[:] = conv_pcp.m


def get_timestep_precip(data, outfile, dtype, compression, complevel):
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
                'timestep_pcp',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    pcp_data.units = str(tot_pcp.units)
    pcp_data.description = 'Total Timestep Accumulated Precpitation'
    pcp_data[:] = ts_pcp


def get_temp_2m(data, outfile, dtype, compression, complevel):
    """Gets the 2m temperature data"""
    temp_2m = data.variables['T2'][:]
    temp_data = outfile.createVariable(
                'temp_2m',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    temp_data.units = data.variables['T2'].units
    temp_data.description = data.variables['T2'].description
    temp_data[:] = temp_2m


def get_q_2m(data, outfile, dtype, compression, complevel):
    q_2m = data.variables['Q2'][:]
    q_data = outfile.createVariable(
                'q_2m',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    q_data.units = data.variables['Q2'].units
    q_data.description = data.variables['Q2'].description
    q_data[:] = q_2m


def get_v_10m(data, outfile, dtype, compression, complevel):
    v_10m = data.variables['V10'][:]
    v_data = outfile.createVariable(
                'v_10m',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    v_data.units = data.variables['V10'].units
    v_data.description = data.variables['V10'].description
    v_data[:] = v_10m


def get_u_10m(data, outfile, dtype, compression, complevel):
    u_10m = data.variables['U10'][:]
    u_data = outfile.createVariable(
                'u_10m',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    u_data.units = data.variables['U10'].units
    u_data.description = data.variables['U10'].description
    u_data[:] = u_10m


def get_mslp(data, outfile, dtype, compression, complevel):
    slp = getvar(data, 'slp', ALL_TIMES)
    slp_data = outfile.createVariable(
                'mslp',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    slp_data.units = slp.units
    slp_data.description = slp.description
    slp_data[:] = slp


def get_uh(data, outfile, dtype, compression, complevel):
    uh = getvar(data, 'updraft_helicity', ALL_TIMES)
    uh_data = outfile.createVariable(
                'UH',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    uh_data.units = uh.units
    uh_data.description = uh.description
    uh_data[:] = uh


def get_cape(data, outfile, dtype, compression, complevel):
    capecin = getvar(data, 'cape_2d', ALL_TIMES)
    cape = np.array(capecin[0, ]) * units('J/kg')
    cin = np.array(capecin[1, ]) * units('J/kg')
    cape_data = outfile.createVariable(
                'cape',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    cape_data.units = str(cape.units)
    cape_data.description = '2D Convective Available Potential Energy'
    cape_data[:] = cape.m

    cin_data = outfile.createVariable(
                'cin',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    cin_data.units = str(cin.units)
    cin_data.description = '2D Convective Inhibition'
    cin_data[:] = cin.m


def get_dbz(data, outfile, dtype, compression, complevel):
    dbz = getvar(data, 'mdbz', ALL_TIMES)
    dbz_data = outfile.createVariable(
                'DBZ',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    dbz_data.units = dbz.units
    dbz_data.description = dbz.description
    dbz_data[:] = dbz


def get_dewpt_2m(data, outfile, dtype, compression, complevel):
    """Gets the 2m dewpoint data"""
    dewpt_2m = getvar(data, 'td2', ALL_TIMES)
    dewpt_data = outfile.createVariable(
                'dewpt_2m',
                dtype,
                ('time', 'lat', 'lon'),
                zlib=compression, complevel=complevel)
    dewpt_data.units = dewpt_2m.units
    dewpt_data.description = dewpt_2m.description
    dewpt_data[:] = dewpt_2m
