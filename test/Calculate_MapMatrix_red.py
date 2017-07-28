# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:03:41 2016

@author: Oliver Lemke
"""

import numpy as np
import sys
import timeit
import pickle

### Input ###

N = 500				# Number of nearest neighbors (should be in [200,500])
Dim = 5				# Number of Dimensions to be considered
File = 'Coord.p'		# Input (Coordinates TxDim) (pickle)

#############

# Get Replica Number from Console

try:
    i=int(sys.argv[1])		# Execute File with: python Calculate_MapMatrix.py 0 (for replica 0)
except:
    i=0
 
# Load Data

data = pickle.load(open(File,'rb')) 		# Original Data
rdata = np.load('reduced_data.npy','r') 	# Reduced Data

if N > len(rdata):
	N = len(rdata)

if np.shape(np.shape(data[0]))[0]==1:
    data=[data]
data=data[i][:,:Dim]

num_of_frames = (len(data))
num_of_frames_ref = (len(rdata))

# Calculate Map Matrix

dist=np.zeros((num_of_frames,N,2))

start = timeit.default_timer()
for j in range(num_of_frames):
    Val = 0
    for k in range(np.shape(rdata)[1]):
        Val += (data[j,k]-rdata[:,k])**2
    Val = np.sqrt(Val)
    
    distsort = np.zeros((num_of_frames_ref,2))
    distsort[:,0] = np.argsort(Val)+1
    distsort[:,1] = np.sort(Val)
    
    dist[j,:,:] = distsort[:N,:]

    # Time Estimator

    if j == 1000:
        stop = timeit.default_timer()
        time = (stop - start) * (num_of_frames/float(1000))
        hours = time/float(3600)
        minutes = (hours - np.floor(hours))*60
        seconds = (minutes - np.floor(minutes))*60
        print ("Estimated Run-Time (without writing to Disc): %d:%d:%d " %(np.floor(hours),np.floor(minutes),np.floor(seconds)))

# Save Output

print ("Size of Map matrix %d x %d" %(np.shape(dist)[0],np.shape(dist)[1]))

N1='dist_comp'+str(i)+'.npy'

np.save(N1,dist)
