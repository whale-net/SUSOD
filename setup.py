"""
SUSOP python package config.

Author: alex harding
"""

from setuptools import setup

setup(
	name='SUSOD',
	version='1.0.0',
	packages=['SUSOD'],
	include_package_data=True,
	install_requires=[
		'Flask',
		'pycodestyle',
		'pydocstyle',
		'gmusicapi',
		'mysql-connector',
		'nodeenv'
	],
)