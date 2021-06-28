#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:13:19 2021

@author: fdipietro
"""

# %% Preliminaries

import numpy as np
import os
import sys

# Env variables to be set on .bashrc
repos_path = os.getenv('GIT_REPOS_PATH')
bimvee_path = os.environ.get('BIMVEE_PATH')
mustard_path = os.environ.get('MUSTARD_PATH')
datasets_path = os.environ.get('DATASETS_PATH')

# Add local paths
sys.path.insert(0, repos_path)
sys.path.insert(0, bimvee_path)
sys.path.insert(0, mustard_path)

# %% Load aedat file

import sys
from AedatTools.PyAedatTools import ImportAedat

# Create a dict with which to pass in the input parameters.
aedat = {}
aedat['importParams'] = {}

# Put the filename, including full path, in the 'filePath' field.
aedat['importParams']['filePath'] = '/home/slam/datasets/mov1.aedat'# Working with a file where the source hasn't been declared - do this explicitly:
aedat['importParams']['source'] = 'Davis240b';

# Shape container to play on mustard
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

container = ImportAedat.ImportAedat(aedat)
del container['importParams']

container['data']['dvs']['ts'] = container['data']['dvs']['ts'] - container['data']['dvs']['ts'][0]
container['data']['dvs']['ts'] = container['data']['dvs']['ts'] / 1000000
container['data']['special']['ts'] = container['data']['special']['ts'] - container['data']['special']['ts'][0]
container['data']['special']['ts'] = container['data']['special']['ts'] / 1000000


# %% Start Mustard

cwd = os.getcwd()

import threading
import mustard
app = mustard.Mustard()
thread = threading.Thread(target=app.run)
thread.daemon = True
thread.start()

# %% Once mustard is open, undo the change of working directory

os.chdir(cwd)

#%% See raw data

app.setData(container)

# #%% Export to yarp 

# from bimvee.exportIitYarp import exportIitYarp

# exportIitYarp(container, 
#               exportFilePath= '/home/slam/mov1', 
#               pathForPlayback= '/home/slam/mov1')