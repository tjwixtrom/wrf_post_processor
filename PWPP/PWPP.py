# Top level code for wrf post processor
# by Tyler Wixtrom
# Texas Tech University

import numpy as np
from netCDF4 import Dataset, date2num
from datetime import datetime
from wrf import getvar, ALL_TIMES
import warnings
from .variable_def import get_variables
from .calc import (get_isobaric_variables, get_precip, get_timestep_precip,
                   get_temp_2m, get_q_2m, get_u_10m, get_v_10m, get_mslp, get_uh,
                   get_cape, get_dbz, get_dewpt_2m)


def wrfpost(inname, outname, variables, plevs=None):
    """
    Runs the WRF Post Processor
    :param inname: string of input file path
    :param outname: string of output file path
    :param variables: list of desired variable strings
        Supported diagnostic variable strings:
            uwnd: U-component of wind on isobaric levels
            vwnd: V-component of wind on isobaric levels
            wwnd: W-component of wind on isobaric levels
            temp: Temperature on isobaric levels
            dewpt: Dewpoint temperature on isobaric levels
            avor: Absolute vorticity on isobaric levels
            height: Geopotential height of isobaric levels
            pres: Pressure on model levels
            mslp: Pressure reduced to mean sea level
            temp_2m: Temperature at 2m
            q_2m: Specific humidity at 2m
            u_10m: U-component of wind at 10m
            v_10m: V-component of wind at 10m
            conv_pcp: Shallow cumulus accumulated precipitation
            grid_pcp: Grid scale accumulated precipitation
            tot_pcp: Total accumulated precipitation
            timestep_pcp: Total timestep accumulated precipitation
            UH: Updraft helicity
            cape: 2D convective available potetial energy
            cin: 2D convective inhibition
            refl: Maximum reflectivity

    :param plevs: optional array of desired output pressure levels
    :return: File of post-processed WRF output
    """
    # open the input file
    data = Dataset(inname)

    # get out time, lat, lon from original data
    times = getvar(data, 'times', ALL_TIMES, meta=False)
    lat = getvar(data, 'lat', ALL_TIMES)
    lon = getvar(data, 'lon', ALL_TIMES)

    # parse time string to make CF-compliant
    vtimes = []
    for i in range(times.shape[0]):
        vtimes.append(datetime.strptime(str(times[i]), '%Y-%m-%dT%H:%M:%S.000000000'))

    # open the output file
    outfile = Dataset(outname, 'w')

    # copy original global attributes
    for name in data.ncattrs():
        setattr(outfile, name, getattr(data, name))

    # create output dimensions
    outfile.createDimension('time', data.dimensions['Time'].size)
    outfile.createDimension('lat', data.dimensions['south_north'].size)
    outfile.createDimension('lon', data.dimensions['west_east'].size)

    # parse input variable list against dictionary to pull out isobaric,
    # wrf-python, and other variables
    iso_vars = []
    other_vars = []
    for variable in variables:
        var_def = get_variables()
        try:
            var_def[variable]
            if var_def[variable][1] == 1:
                iso_vars.append(variable)
            else:
                other_vars.append(variable)
        except KeyError:
            outfile.close()
            raise KeyError('Definition for '+variable+' not found.')
    # create dimension for isobaric levels
    if plevs is not None:
        outfile.createDimension('pressure levels', plevs.size)
        p_lev = outfile.createVariable('pressure levels', 'f8', ('pressure levels'))
        p_lev.units = 'Pascal'
        p_lev.description = 'Isobaric Pressure Levels'
        p_lev[:] = plevs.to('Pa').m
        if len(iso_vars) < 1:
            warnings.warn('Pressure levels specified but no isobaric variables requested')
    elif len(iso_vars) > 0:
        raise ValueError('Isobaric variables requested, no pressure levels given')

    # write times, lats, lons, and plevs to output file
    valid_times = outfile.createVariable('valid_time_ut', 'f8', ('time',))
    valid_times.units = 'seconds since 1970-01-01 UTC'
    valid_times.description = 'Model Forecast Times'
    valid_times[:] = date2num(vtimes, valid_times.units)
    del vtimes

    latitude = outfile.createVariable('lat', 'f8', ('time', 'lat', 'lon'))
    latitude.units = lat.units
    latitude.description = lat.description
    latitude[:] = np.array(lat)
    del lat

    longitude = outfile.createVariable('lon', 'f8', ('time', 'lat', 'lon'))
    longitude.units = lon.units
    longitude.description = lon.description
    longitude[:] = np.array(lon)
    del lon

    # interpolate to isobaric levels and save to file
    if len(iso_vars) > 0:
        get_isobaric_variables(data, iso_vars, plevs, outfile)

    # get precipitation variables if requested
    if 'tot_pcp' in other_vars:
        if ('grid_pcp' in other_vars) and ('conv_pcp' in other_vars):
            get_precip(data, outfile, RAINNC_out=True, RAINSH_out=True)
        elif 'grid_pcp' in other_vars:
            get_precip(data, outfile, RAINNC_out=True)
        elif 'conv_pcp' in other_vars:
            get_precip(data, outfile, RAINSH_out=True)
        else:
            get_precip(data, outfile)

    if 'timestep_pcp' in other_vars:
        get_timestep_precip(data, outfile)

    # get surface variables if requested
    if 'temp_2m' in other_vars:
        get_temp_2m(data, outfile)

    if 'q_2m' in other_vars:
        get_q_2m(data, outfile)

    if 'u_10m' in other_vars:
        get_u_10m(data, outfile)

    if 'v_10m' in other_vars:
        get_v_10m(data, outfile)

    if 'mslp' in other_vars:
        get_mslp(data, outfile)

    if 'UH' in other_vars:
        get_uh(data, outfile)

    if ('cape' in other_vars) or ('cin' in other_vars):
        get_cape(data, outfile)

    if 'refl' in other_vars:
        get_dbz(data, outfile)

    if 'dewpt_2m' in other_vars:
        get_dewpt_2m(data, outfile)

    outfile.close()
