# Top level code for wrf post processor
# by Tyler Wixtrom
# Texas Tech University

import numpy as np
from netCDF4 import Dataset, date2num
import datetime
from wrf import getvar, ALL_TIMES
from .variable_def import get_variables
from .calc import get_isobaric_variables
import warnings


def wrfpost(inname, outname, variables, plevs=None):
    """
    Runs the WRF Post Processor
    :param inname: string of input file path
    :param outname: string of output file path
    :param variables: list of desired variable strings
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
        vtimes.append(datetime.datetime.strptime(str(times[i]),
                                                 '%Y-%m-%dT%H:%M:%S.000000000'))

    # open the output file
    outfile = Dataset(outname, 'w')

    # copy original global attributes
    for name in data.ncattrs():
        setattr(outfile, name, getattr(data, name))

    # create output dimensions
    outfile.createDimension('Time', data.dimensions['Time'].size)
    outfile.createDimension('Latitude', data.dimensions['south_north'].size)
    outfile.createDimension('Longitude', data.dimensions['west_east'].size)

    # parse input variable list against dictionart to pull out isobaric variables
    iso_vars = []
    other_vars = []
    for variable in variables:
        var_def = get_variables()
        if var_def[variable][1] == 1:
            iso_vars.append(variable)
        else:
            other_vars.append(variable)

    # create dimension for isobaric levels
    if plevs is not None:
        outfile.createDimension('Pressure Levels', plevs.size)
        p_lev = outfile.createVariable('pressure levels', 'f8', ('Pressure Levels'))
        p_lev.units = 'Pascal'
        p_lev.description = 'Isobaric Pressure Levels'
        p_lev[:] = plevs.to('Pa').m
        if len(iso_vars) < 1:
            warnings.warn('Pressure levels specified but no isobaric variables requested')
    else:
        if len(iso_vars) > 0:
            raise ValueError('Isobaric variables requested, no pressure levels given')

    # write times, lats, lons, and plevs to output file
    valid_times = outfile.createVariable('time', 'f8', ('Time',))
    valid_times.units = 'hours since ' + str(vtimes[0])
    valid_times.description = 'Model Forecast Times'
    valid_times[:] = date2num(vtimes, valid_times.units)

    latitude = outfile.createVariable('lat', 'f8', ('Time', 'Latitude', 'Longitude'))
    latitude.units = lat.units
    latitude.description = lat.description
    latitude[:] = np.array(lat)

    longitude = outfile.createVariable('lon', 'f8', ('Time', 'Latitude', 'Longitude'))
    longitude.units = lon.units
    longitude.description = lon.description
    longitude[:] = np.array(lon)

    # interpolate to isobaric levels and save to file
    get_isobaric_variables(data, iso_vars, plevs, outfile)

    outfile.close()
