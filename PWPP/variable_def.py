# Variable definition file


def get_variables():
    """
    Function for getting the master variable dictionary
    :return: variable dictionary
    """
    variables = {
        'uwnd': ['U-component of wind on isobaric levels', 1, 'ua'],
        'vwnd': ['V-component of wind on isobaric levels', 1, 'va'],
        'wwnd': ['W-component of wind on isobaric levels', 1, 'wa'],
        'temp': ['Temperature on isobaric levels', 1, 'temp'],
        'dewpt': ['Dewpoint temperature on isobaric levels', 1, 'td'],
        'avor': ['Absolute vorticity on isobaric levels', 1, 'avo'],
        'height': ['Geopotential height of isobaric levels', 1, 'z'],
        'pres': ['Pressure on model levels', 0, 'p'],
        'mslp': ['Pressure reduced to mean sea level', 0, 'slp'],
        'temp_2m': ['Temperature at 2m', 2, 'T2'],
        'dewpt_2m': ['Dewpoint temperature at 2m', 2, 'td2'],
        'q_2m': ['Specific humidity at 2m', 2, 'Q2'],
        'u_10m': ['U-component of wind at 10m', 2, 'U10'],
        'v_10m': ['V-component of wind at 10m', 2, 'V10'],
        'tot_pcp': ['Total accumulated precipitation', 2, None],
        'timestep_pcp': ['Total timestep accumulated precipitation', 2, None],
        'UH': ['Updraft helicity', 0, 'updraft_helicity'],
        'cape': ['2D convective available potetial energy', 0, 'cape_2d'],
        'cin': ['2D convective inhibition', 0, 'cape_2d'],
        'refl': ['Maximum reflectivity', 0, 'mdbz']
    }
    return variables
