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
aedat['importParams']['filePath'] = '/home/fdipietro/data/DHP19/mov1.aedat'# Working with a file where the source hasn't been declared - do this explicitly:
aedat['importParams']['source'] = 'Davis240b';

# Shape container to play on mustard
def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

# def rename(self,key,new_key):
#     ind = self._keys.index(key)  #get the index of old key, O(N) operation
#     self._keys[ind] = new_key    #replace old key with new key in self._keys
#     self[new_key] = self[key]    #add the new key, this is added at the end of self._keys
#     self._keys.pop(-1)           #pop the last item in self._keys

aedatData = ImportAedat.ImportAedat(aedat)


# %% Parameters for separating events for each camera
# Cameras number and resolution. Constant for DHP19.
nbcam = 4;
sx = 346;
sy = 260;
# PARAMETERS: 
# Average num of events per camera, for constant count frames.
eventsPerFrame = 7500; 

# Flag and sizes for subsampling the original DVS resolution.
# If no subsample, keep (sx,sy) original img size.
do_subsampling = False;
reshapex = sx;
reshapey = sy;

# Flag to save accumulated recordings.
saveHDF5 = True;

# Flag to convert labels
convert_labels = True;

save_log_special_events = False;
#-----------------------------------------

# Hot pixels threshold (pixels spiking above threshold are filtered out).
thrEventHotPixel = 1*10^4;

# Background filter: events with less than dt (us) to neighbors pass through.
dt = 70000;

# Masks for IR light in the DVS frames.
# Mask 1
xmin_mask1 = 780;
xmax_mask1 = 810;
ymin_mask1 = 115;
ymax_mask1 = 145;
# Mask 2
xmin_mask2 = 346*3 + 214;
xmax_mask2 = 346*3 + 221;
ymin_mask2 = 136;
ymax_mask2 = 144;
events = aedat['data']['polarity']['timeStamp'].astype(np.int64)
startTime = events[0] 
stopTime = events[-1] 
                  
startTime = startTime.astype(np.int32)
stopTime  = stopTime.astype(np.int32)

# [startIndex, stopIndex, pol, X, y, cam, timeStamp] = ...
#     extract_from_aedat(...
#                     aedat, events, ...
#                     startTime, stopTime, ...
#                     sx, sy, nbcam, ...
#                     thrEventHotPixel, dt, ...
#                     xmin_mask1, xmax_mask1, ymin_mask1, ymax_mask1, ...
#                     xmin_mask2, xmax_mask2, ymin_mask2, ymax_mask2);

from AedatTools.PyAedatTools import extract_from_aedat

# rta = extract_from_aedat.extract_from_aedat(aedat, events,
#                          startTime, stopTime, sx, sy, nbcam,
#                     thrEventHotPixel, dt,
#                     xmin_mask1, xmax_mask1, ymin_mask1, ymax_mask1,
#                     xmin_mask2, xmax_mask2, ymin_mask2, ymax_mask2)

# del container['importParams']

#del container['importParams']

# %% Build a container that can be played on mustard

# container = aedatData
# del container['importParams']

info = {}
info['filePathOrName'] = aedat['importParams']['filePath']
data = {}
data['dvs'] = {}
data['dvs']['x'] = aedatData['data']['polarity']['x']
data['dvs']['y'] = aedatData['data']['polarity']['y']
data['dvs']['ts'] = aedatData['data']['polarity']['timeStamp']
data['dvs']['pol'] = aedatData['data']['polarity']['polarity']

container = {}
container['data'] = data
container['info'] = info

# container = {}
# container['data'] = {}
# container['info'] = 
# container['data']['dvs'] = aedatData['data']['polarity']

# container['data']['dvs']['ts'] = container['data']['dvs']['ts'] - container['data']['dvs']['ts'][0]
# container['data']['dvs']['ts'] = container['data']['dvs']['ts'] / 1000000
# container['data']['special']['ts'] = container['data']['special']['ts'] - container['data']['special']['ts'][0]
# container['data']['special']['ts'] = container['data']['special']['ts'] / 1000000


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

# # #%% Export to yarp 

# # from bimvee.exportIitYarp import exportIitYarp

# # exportIitYarp(container, 
# #               exportFilePath= '/home/slam/mov1', 
# #               pathForPlayback= '/home/slam/mov1')