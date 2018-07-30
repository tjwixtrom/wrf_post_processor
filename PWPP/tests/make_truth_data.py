# Creates the output truth data for testing
from PWPP import wrfpost
from metpy.units import units
datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
outfile = 'PWPP/tests/true_out.nc'
plevs = [500.] * units.hPa
variables = ['temp_2m',
             'dewpt_2m',
             'q_2m',
             'v_10m',
             'u_10m',
             'mslp',
             'UH',
             'cape',
             'cin',
             'refl',
             'temp',
             'tot_pcp',
             'timestep_pcp']
wrfpost(datafile, outfile, variables, plevs=plevs)
