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
        pres_data = outfile.createVariable(var_list[i], 'f8',
                                          ('Time', 'Pressure Levels', 'Latitude',
                                           'Longitude'))
        pres_data.units = var_data[i].units
        pres_data.description = var_data[i].description
        pres_data[:] = iso_data[i]
