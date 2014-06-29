#!/usr/bin/env python

from distutils.core import setup
with open('README') as file:
    long_description = file.read()

setup(name='TimeMachine',
      long_description=long_description,	
      version='0.1',
      description='A Python module that exposes some useful date manipulation methods.',
      author='Brian K. Jones',
      author_email='bkjones@gmail.com',
      url='http://www.github.com/bkjones/TimeMachine',
      download_url='http://www.github.com/bkjones/TimeMachine',
      license='MIT',
      py_modules=['TimeMachine'],
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.0",
          "Programming Language :: Python :: 3.2",
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='python date datetime wrapper time',
)

