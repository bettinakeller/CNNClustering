# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:37:44 2015

@author: Oliver Lemke
"""

import numpy as np
import argparse
import sys
import ast
import timeit

# Define ismember function

def ismember(a, b):
    bi = {}
    for i, el in enumerate(b):
        if el not in bi:
            bi[el] = i
    return [bi.get(itm, -1) for itm in a]

# Read Input from command line with options

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('-Fra', '--InputFramefile', type=str, help='Input: Framefile (.ndx-file) (default=frames.ndx)', default='frames.ndx')
    parser.add_argument('-Nc', '--Numberclusters', type=int, help='Input: Number of Clusters (N biggest clusters) (default=100)', default=100)
    parser.add_argument('-Map', '--InputMapMatrix', type=str, help='Input: Map-matrix (default=Map_dist.npy)', default='Map_dist.npy')
    parser.add_argument('-Cut', '--Cutoff', type=float, help='Cutoff criterion (rc for CNN, nnn for JP and eps for DBSCAN)')
    parser.add_argument('-Sim', '--Similarity', type=int, help='Criterion of similarity (nnnc for CNN and JP and MinPts for DBSCAN)')
    parser.add_argument('-Out', '--Output', type=str, help='Output: Projected Trajectory (.npy-file) (default=Trace.npy)', default='Trace.npy') 
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)

try:
    rc = float(args.Cutoff)
except:
    print ('Error: Cutoff missing or type of cutoff incorrect')
    sys.exit(1)   
try:    
    nnnc = int(args.Similarity)
except:
    print ('Error: Similatiry criterion missing or type of similarity criterion incorrect')
    sys.exit(1)   
   

# Check for errors

if rc <=0:
    print ('Error: Definition of the cutoff incorrect')
    sys.exit(1)
if nnnc <= 0:
    print ('Error: Definition of the nnnc incorrect')
    sys.exit(1)

try:
    Nc = int(args.Numberclusters)
except:
    print ('Error: Clusternumber must be an integer')
    sys.exit(1)
    
try:
    TrNa = str(args.Output)
except:
    print ('Error: Output-File incorrect')
    sys.exit(1)

#Load data

try:
    frload = str(args.InputFramefile)
    datafr=open(frload,'r')
    linefr=datafr.read().splitlines()
except:
    print ('Error: Frame-File not found')
    sys.exit(1)

# Load Map-Matrix

try:
    merge = str(args.InputMapMatrix)
    dist=np.load(merge,mmap_mode='r')
    (M,N,L)=np.shape(dist)
except:
    print ('Error: Map-Matrix not found')
    sys.exit(1)

# Check the number of clusters

if len(linefr) < Nc:
    Nc = len(linefr)

# Convert frame List to array-type

C=[0]*Nc
    
for i in range(0,Nc):
    Ca=linefr[i]
    C[i]=np.asarray(ast.literal_eval(Ca))+1

# Sort distance matrix

Numbi=np.zeros((M))         # Number of neighbors within rc
distnll=[0]*M               # Neighborlist
Trace=np.zeros((M))         # Projected Trajectory

for i in range(0,M):
    distsort=np.copy(dist[i,:,:])        
    
    # Determine all Neighbors that are located within rc
    
    j=0
    Vecl=np.zeros((1,N))
    while distsort[j,1]<=rc:
        Vecl[0,j]=distsort[j,0]
        j=j+1
        Numbi[i]=Numbi[i]+1
        if j==N:
            break
    nll=np.nonzero(Vecl)
    distnll[i]=Vecl[0,nll[1]]
    
# Calculate the total number of nearest neighbors
    
km=int(max(Numbi))                  # Maximal number of nearest neighbors
distn=np.zeros((M,km))              # Distance Matrix for nearest neighbors
    
for i in range(0,M):
    distn[i,0:len(distnll[i])]=distnll[i]           # Distance Matrix for nearest neighbors
    
# Clear Memory
    
del distnll

# Assigne data points either to a cluster or to the transition region (not assigned)

start = timeit.default_timer()

for i in range(0,M):
    for j in range(0,Nc):
        if np.shape(np.nonzero((np.asarray(ismember(C[j],distn[i,:]))+1)))[1] >= nnnc:
            Trace[i]=j+1
        # Time Estimator

    if i == 100:
        stop = timeit.default_timer()
        time = (stop - start) * M/float(100)
        hours = time/float(3600)
        minutes = (hours - np.floor(hours))*60
        seconds = (minutes - np.floor(minutes))*60
        print ("Estimated Run-Time: %d:%d:%d " %(np.floor(hours),np.floor(minutes),np.floor(seconds)))
        

#Save projected trajectory

np.save(TrNa,Trace)
