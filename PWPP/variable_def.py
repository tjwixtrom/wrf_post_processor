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
        'q_2m': ['Specific humidity at 2m', 2, 'Q2'],
        'u_10m': ['U-component of wind at 10m', 2, 'U10'],
        'v_10m': ['V-component of wind at 10m', 2, 'V10'],
        'cu_pcp': ['Shallow cumulus accumulated precipitation', 2, 'RAINSH'],
        'grid_pcp': ['Grid scale accumulated precipitation', 2, 'RAINNC'],
        'tot_pcp': ['Total accumulated precipitation', 3, None]
    }
    return variables
