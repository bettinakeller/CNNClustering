# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:37:44 2015

@author: Oliver Lemke
"""

import numpy as np
import pickle
import argparse
import sys
import matplotlib.pyplot as plt

# Read Input from command line with options

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('-Inc', '--Inputcluster', type=str, help='Input: Clusterfile (.p-file) (default=Cluster.p)', default='Cluster.p')
    parser.add_argument('-Ins', '--Inputclustersize', type=str, help='Input: Clustersizefile (.p-file) (optional)', default='default')
    parser.add_argument('-Ind', '--Inputdistmat', type=str, help='Input: Distancematrix (default=dist.npy)', default='dist.npy')
    parser.add_argument('-Nci', '--Number', type=int, help='Maximal number of isolated clusters (default=5)', default=5)
    parser.add_argument('-Out', '--Output', type=str, help='Output: Distance matrices of the top N clusters (only filename) (default=dist)', default='dist')
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)

# Check for errors
    
try:
    Nci=int(args.Number)
except:
    print ('Error: Number of isolated clusters must be an integer')
    sys.exit(1)
    
if Nci<=0:
    print ('Error: Number of isolated clusters incorrect')
    sys.exit(1)

# Load data

try:
    Clload=str(args.Inputcluster)
    Clust=pickle.load(open(Clload, 'rb'))
    N=len(Clust)
except:
    print ('Error: Cluster-file not found')
    sys.exit(1)

# Check if Size-File provided

if str(args.Inputclustersize) is not 'default':
    try:
        Csload=str(args.Inputclustersize)
        Cs=pickle.load(open(Csload, 'rb'))
    except:
        print ('Error: Clustersize-file not found')
        sys.exit(1)
        
# If file is missing        
        
else:
    Cs=np.zeros((2,N))
    for a in range(0,N):
        Ca=Clust[a]
        if np.int_(np.shape(Ca)) > 1:
            Cs[0,a]=np.int_(np.shape(Ca))
            Cs[1,a]=a

# Sort clusters by size

Css=Cs[:,(np.argsort(Cs[0,:]))]
Csr=np.int_(np.fliplr(Css))

# Determine maximal number of clusters

Csi=np.asarray(np.nonzero(Cs[0,:]))
Nmaxx=np.size(Csi)

# Maximal number of isolated clusters

if args.Number < Nmaxx:
    Nmax=int(args.Number)
else:
    Nmax=Nmaxx
    
# load distance matrix

distm=str(args.Inputdistmat)
   
   
try:
    dist=np.load(distm,mmap_mode='r')
except:
    print ('Error: Distancematrix not found')
    sys.exit(1)
            
# Isolate clusters

j=0
distmat=str(args.Output)

while j<Nmax:
    C=np.sort(Clust[Csr[1,j]])-1    
    A=dist[C[:],:]
    B=A[:,C[:]] 
    distmata=distmat+str('_')+str(j)
    np.save(distmata, B)
    j=j+1
