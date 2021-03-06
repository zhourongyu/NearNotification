"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""
import os
import sys
from setuptools import setup

APP = ['nearNotification.py']
APP_NAME = "NearNotification"
DATA_FILES = []
OPTIONS = {'argv_emulation': True, 'iconfile': 'ico.icns'}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
