# -*- coding: utf-8 -*-

from setuptools import setup
from codecs import open
from os import path

import gameoflife

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='GameOfLife',

    version=gameoflife.__version__,

    description='Game Of Life',
    # long_description=long_description,
    long_description='Game Of Life cellular automata.',

    url='https://github.com/pkobrien/game-of-life',

    author="Patrick K. O'Brien",
    author_email='patrick.keith.obrien@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Simulation',
        'Topic :: Scientific/Engineering :: Artificial Life',
    ],

    keywords='conway game life',

    extras_require={
        'test': ['pytest'],
    },
)
