from setuptools import setup

setup(
    name='PWPP',
    version='0.1',
    url='',
    license='',
    author='Tyler Wixtrom',
    author_email='tyler.wixtrom@ttu.edu',
    description='Python WRF Post Processor',
    packages=['PWPP'],
    requires=['netcdf4', 'numpy', 'metpy', 'xarray']
)
