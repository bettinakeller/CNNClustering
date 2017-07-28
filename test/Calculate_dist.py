# -*- coding: utf-8 -*-
"""
Created on Wed Oct 19 14:01:09 2016

@author: Oliver Lemke
"""

import numpy as np
import pickle

### Input ###

Slice = 10			# Every nth data point
Dim = 2				# Number of Dimensions to be considered
File = 'Coord.p'		# TICA Output

#############

# Load TICA-Data

data=pickle.load(open(File,'rb'))	# Original Data

if np.shape(np.shape(data[0]))[0]==1:
    data=[data]

if Dim > np.shape(data[0])[1]:
	Dim = np.shape(data[0])[1]

# Reduce Data

reduced_data=data[0][::Slice,:Dim]	# Reduced Data

if len(data)>1:
    for i in range(1,len(data)):
        reduced_data=np.vstack((reduced_data,data[i][::Slice,:Dim]))

# Calculate Distance Matrix

dist=np.zeros((len(reduced_data),len(reduced_data)))

print ("Size of Distance matrix %d x %d" %(np.shape(reduced_data)[0],np.shape(reduced_data)[0]))

for i in range(np.shape(reduced_data)[1]):
    (A,B) = np.meshgrid(reduced_data[:,i],reduced_data[:,i])
    dist += ((A-B)**2)
dist = np.sqrt(dist)

# Save Data

np.save('dist',dist)
np.save('reduced_data',reduced_data)
