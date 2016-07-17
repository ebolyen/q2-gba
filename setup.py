# ----------------------------------------------------------------------------
# Copyright (c) 2016 Evan Bolyen.
#
# Distributed under the terms of The MIT License (MIT).
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import setup, find_packages

setup(
    name="q2-gba",
    version='0.0.1dev',
    packages=find_packages(),
    install_requires=['qiime >= 2.0.0'],
    package_data={'q2-gba': [
        'assets/*', 'assets/resources/*', 'assets/js/*', 'assets/js/video/*'
    ]},
    author="Evan Bolyen",
    author_email="ebolyen@gmail.com",
    description="Functionality for working with .gba files in QIIME 2",
    license="MIT",
    url="https://github.com/ebolyen/q2-gba",
    entry_points={
        'qiime.plugins':
        ['q2-gba=q2_gba.plugin_setup:plugin']
    }
)
