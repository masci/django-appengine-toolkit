# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys

import appengine_toolkit

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = appengine_toolkit.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-appengine-toolkit',
    version=version,
    description='Deploy Django projects on Google App Engine with ease',
    long_description=readme + '\n\n' + history,
    author='Massimiliano Pippi',
    author_email='mpippi@gmail.com',
    url='https://github.com/masci/django-appengine-toolkit',
    packages=[
        'appengine_toolkit',
    ],
    include_package_data=True,
    install_requires=[
        'django<1.6',
        'GoogleAppEngineCloudStorageClient',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-appengine-toolkit',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)