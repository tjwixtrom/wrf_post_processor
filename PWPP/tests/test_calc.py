##############################################################################################
#
# test_calc.py - Tests for variable calculation code
#
# by Tyler Wixtrom
# Texas Tech University
#
##############################################################################################
from PWPP import wrfpost
import pytest
from metpy.units import units
from netCDF4 import Dataset
from numpy.testing import assert_array_almost_equal


def test_temp_2m():
    """Test for 2m temperature function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['temp_2m']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    temp2m = data.variables['temp_2m'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    temp2m_truth = data_truth.variables['temp_2m'][:]
    assert_array_almost_equal(temp2m, temp2m_truth, 4)
    data.close()
    data_truth.close()


def test_dewpt_2m():
    """Test for 2m dewpoint function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['dewpt_2m']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    dewpt2m = data.variables['dewpt_2m'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    dewpt2m_truth = data_truth.variables['dewpt_2m'][:]
    assert_array_almost_equal(dewpt2m, dewpt2m_truth, 4)
    data.close()
    data_truth.close()


def test_q_2m():
    """Test for 2m q function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['q_2m']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    q2m = data.variables['q_2m'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    q2m_truth = data_truth.variables['q_2m'][:]
    assert_array_almost_equal(q2m, q2m_truth, 4)
    data.close()
    data_truth.close()


def test_v_10m():
    """Test for 10m v function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['v_10m']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['v_10m'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['v_10m'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_u_10m():
    """Test for 10m u function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['u_10m']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['u_10m'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['u_10m'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_mslp():
    """Test for mslp function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['mslp']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['mslp'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['mslp'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_uh():
    """Test for UH function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['UH']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['UH'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['UH'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_cape_cin():
    """Test for cape and cin function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['cape', 'cin']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['cape'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['cape'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    test_data = data.variables['cin'][:]
    truth_data = data_truth.variables['cin'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_refl():
    """Test for refl function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['refl']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['DBZ'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['DBZ'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_isobaric():
    """Test for isobaric function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['temp']
    plevs = [500] * units.hPa
    with pytest.warns(UserWarning):
        wrfpost(datafile, outfile, variables, plevs=plevs)
    data = Dataset(outfile)
    test_data = data.variables['temp'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['temp'][:]
    assert_array_almost_equal(test_data, truth_data, 4)
    data.close()
    data_truth.close()


def test_precip():
    """Test for refl function"""
    datafile = 'PWPP/tests/testfile.nc'  # Taken from units testing on WRF-Python package
    outfile = 'PWPP/tests/outfile.nc'
    variables = ['timestep_pcp', 'tot_pcp']
    wrfpost(datafile, outfile, variables)
    data = Dataset(outfile)
    test_data = data.variables['timestep_pcp'][:]
    data_truth = Dataset('PWPP/tests/true_out.nc')
    truth_data = data_truth.variables['timestep_pcp'][:]
    assert_array_almost_equal(test_data, truth_data, 4)

    test_data = data.variables['tot_pcp'][:]
    truth_data = data_truth.variables['tot_pcp'][:]
    assert_array_almost_equal(test_data, truth_data, 4)

    data.close()
    data_truth.close()
