# Top level code for wrf post processor
# by Tyler Wixtrom
# Texas Tech University

import numpy as np
from netCDF4 import Dataset, date2num
import datetime
from wrf import getvar, ALL_TIMES
from metpy.calc import log_interp
from metpy.units import units


def wrfpost(inname, outname, variables, plevs=None):
    """
    Runs the WRF Post Processor
    :param infile: string of input file path
    :param outfile: string of output file path
    :param variables: list of desired variable strings
    :param plevs: optional array of desired output pressure levels
    :return: File of post-processed WRF output
    """

    data = Dataset(inname)

    times = getvar(data, 'times', ALL_TIMES, meta=False)
    lat = getvar(data, 'lat', ALL_TIMES)
    lon = getvar(data, 'lon', ALL_TIMES)

    vtimes = []
    for i in range(times.shape[0]):
        vtimes.append(datetime.datetime.strptime(str(times[i]),
                                                 '%Y-%m-%dT%H:%M:%S.000000000'))

    outfile = Dataset(outname, 'w')

    for name in data.ncattrs():
        setattr(outfile, name, getattr(data, name))

    outfile.createDimension('Time', data.dimensions['Time'].size)
    outfile.createDimension('Latitude', data.dimensions['south_north'].size)
    outfile.createDimension('Longitude', data.dimensions['west_east'].size)

    if plevs is not None:
        outfile.createDimension('Pressure Levels', plevs.size)
        p_lev = outfile.createVariable('pressure levels', 'f8', ('Pressure Levels'))
        p_lev.units = 'Pascal'
        p_lev.description = 'Isobaric Pressure Levels'
        p_lev[:] = plevs.to('Pa').m

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

    outfile.close()
