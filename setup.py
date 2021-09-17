#!/usr/bin/env python
"""Setup pymdown-lexers."""
from setuptools import setup, find_packages

entry_points = '''
[pygments.lexers]
madx=omc_lexers:MadLexer
mad=omc_lexers:MadLexer
'''

setup(
    name='omc-lexers',
    version='0.1.0',
    description='Some OMC related pygments lexers',
    author='Andreas Wegscheider',
    author_email='',
    url='',
    packages=find_packages(),
    entry_points=entry_points,
    install_requires=[
        'Pygments>=2.0.1'
    ],
    zip_safe=True,
    license='MIT License',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only'
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)