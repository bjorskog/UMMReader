#!/usr/bin/en python

from setuptools import setup

setup(
    name='UMMReader',
    version='0.1.0',
    author='bjorskog',
    author_email='bjorn.skogtro@gmail.com',
    packages=['ummreader', 'ummreader.tests'],
    entry_points={
        'console_scripts':[
            'ummreader=ummreader.core:main',
            ],
        },
    package_data={
        'ummreader':{'ummreader':['data/*.xml'],},
        },
    test_suite='nose.collector',
    tests_require='nose',
    license='LICENSE.txt',
    description='Useful tools for reading UMMs.',
    long_description=open('README.txt').read(),
    install_requires=[
        "pymongo >= 2.2",
        "nose >= 1.1.2"
    ],)
    
