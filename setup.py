#!/usr/bin/env python
"""Setup pymdown-lexers."""
from setuptools import setup, find_packages

entry_points = '''
[pygments.lexers]
madx=omc_lexers:MadLexer
'''

setup(
    name='omc-lexers',
    version='1.0.0',
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: Markup :: HTML'
    ]
)