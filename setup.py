from setuptools import setup, find_packages

setup(
    name='xFramework_libraries',
    packages=find_packages(where='libraries'),
    package_dir={'': 'libraries'},
)