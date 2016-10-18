#!/usr/bin/env python

from distutils.core import setup

setup(
    name='cryptall',
    version='0.0.1',
    description='a small command-line interface helping you crypt, decrypt, '
                'and brute-force various crypto algorithms',
    author='Antoine Chauvin',
    author_email='blackrushx@gmail.com',
    url='https://github.com/Blackrush/cryptall',
    packages=['cryptall'],
    entry_points={
        'console_scripts': [
            'cryptall=cryptall.cli:main',
        ],
    },
)
