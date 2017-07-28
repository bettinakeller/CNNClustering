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
    parser.add_argument('-Ind', '--Inputdistmat', type=str, help='Input: Distancematrix (optional) (default=dist.npy)', default='dist.npy')
    parser.add_argument('-Nci', '--Number', type=int, help='Maximal number of isolated clusters (default=5)', default=5)
    parser.add_argument('-Nco', '--Numberopt', type=int, help='Cluster that should be isolated (optional)', default=-1)
    parser.add_argument('-Plo', '--Plot', type=str, help='Plot of the histograms for each cluster (YES or NO) (default=NO)', default ='NO')
    parser.add_argument('-Fig', '--Figure', type=str, help='Output: Histogram-plot (only file-name) (default=Hist)', default='Hist')
    parser.add_argument('-Out', '--Output', type=str, help='Output: Frames of the top N clusters (.ndx- or .txt-file) (default=frames.ndx)', default='frames.ndx')
    parser.add_argument('-Opt', '--Outopt', type=str, help='Output: Frames of one Cluster (.ndx- or .txt.file) (default=framescl.ndx)', default='framescl.ndx')    
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

#try:
Clload=str(args.Inputcluster)
Clust=pickle.load(open(Clload, 'rb'))
N=len(Clust)
#except:
#    print ('Error: Cluster-file not found')
#    sys.exit(1)

if str(args.Inputclustersize) is not 'default':
    try:
        Csload=str(args.Inputclustersize)
        Cs=pickle.load(open(Csload, 'rb'))
    except:
        print ('Error: Clustersize-file not found')
        sys.exit(1)
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

Ploto=str(args.Plot)
Plon=str(args.Figure)

distm=str(args.Inputdistmat)

if Ploto!='YES' and Ploto!='NO':
    print ('Error: Plotoption incorrect')
    sys.exit(1)
    
if Ploto=='YES':
    try:
        dist=np.load(distm,mmap_mode='r')
        Nbin=100                    # Number of bins
        xmax=np.max(dist)
        width=xmax/float(Nbin)
    except:
        print ('Error: Distancematrix not found')
        sys.exit(1)
            
# Isolate clusters

j=0
frames=str(args.Output)

output=open(frames,'w')

while j<Nmax:
    C=np.sort(Clust[Csr[1,j]])-1
    
    if Ploto=='YES':    
        A=dist[C[:],:]
        B=A[:,C[:]]
        bi=int(np.round(np.max(B)/width))
        if bi==0:
            bi=1
        (hist,hbin)=np.histogram(B,bins=bi)
        ymax=np.max(hist)
        Plonr=Plon+str('_')+str(j)+str('.png')
        fig,ax=plt.subplots()
        rf=ax.bar(hbin[0:bi], hist, width)
        plt.axis([0, xmax, 0, ymax*1.1])
        plt.xlabel('Distance / [AU]')
        plt.ylabel('Amount of appearance')
        plt.tight_layout()
        plt.savefig(Plonr)
        plt.close(fig)
    
    j=j+1
    output.write('[')
    for item in C:
        output.write('%s, ' % (item))
    output.write(']\n')
output.close()

# Isolate single cluster

if int(args.Numberopt)>=0:
    fro=int(args.Numberopt)
    if fro<=Nmaxx:
        Nfro=str(args.Outopt)
        outopt=open(Nfro,'w')
        C=np.sort(Clust[Csr[1,fro]])-1
        outopt.write('[')
        for item in C:
            outopt.write('%s, ' % (item))
        outopt.write(']')
        outopt.close()
    else:
        print ('Error: cluster cannot be found')
        sys.exit(1)
