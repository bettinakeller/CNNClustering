# -*- coding: utf-8 -*-
"""
Created on Mon Mar 9 2015

@author: Oliver Lemke
"""

import numpy as np
import numpy.matlib as M
from numpy.matlib import rand,zeros,ones,empty,eye
import time
import sys
import argparse
import pickle
import os

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
    parser.add_argument('-Cut', '--Cutoff', type=float, help='Cutoff criterion (R)')
    parser.add_argument('-Sim', '--Similarity', type=int, help='Criterion of similarity (N)')
    parser.add_argument('-In', '--Input', type=str, help='Input: distance matrix (default=dist.npy)', default='dist.npy')
    parser.add_argument('-Nl', '--Clustersize', type=int, help='Minimal Clustersize (M)(default=2)', default=2)    
    parser.add_argument('-Out', '--Output', type=str, help='Output: Summary-file (default=Summary.txt)', default='Summary.txt')
    parser.add_argument('-Clf', '--Clusterfile', type=str, help='Output: Cluster-file (.p-file) (default=Cluster.p)', default='Cluster.p')
    parser.add_argument('-Csf', '--Clustersizefile', type=str, help='Output: Clustersize-file (.p-file) (default=Clustersize.p)', default='Clustersize.p' )
    parser.add_argument('-Spt', '--Softwarepath', type=str, help='Input: Software path (default=.)', default='.' )
    parser.add_argument('-Screen', '--Screen', type=str, help='Clustering Screen (YES or NO) (default=NO)', default='NO' )
    parser.add_argument('-Ntr', '--NumberTra', type=int, help='Number of trajectories (replica) (default=1)', default=1)
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)

Algo='CNN'
Var='Yes'
    
try:
    Auto = str(args.Screen)
except:
     print ('Error: Auto missing or type of Auto incorrect')
     sys.exit(1) 
     
try:    
    Ntr = int(args.NumberTra)
except:
    print ('Error: Similatiry criterion missing or type of similarity criterion incorrect')
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

if Auto!='YES' and Auto!='NO':
    print ('Error: Choice of Auto mode incorrect')
    sys.exit(1)

if Ntr <= 0:
    print ('Error: Number of trajectories must be at least 1')
    sys.exit(1)
    
if rc <=0:
    print ('Error: Definition of the cutoff incorrect')
    sys.exit(1)
if nnnc <= 0:
    print ('Error: Definition of the nnnc incorrect')
    sys.exit(1)
        
try:
    Nl=int(args.Clustersize)
except:
    print ('Error: Clustersize number must be an integer')

path=str(os.path.dirname(os.path.realpath(__file__)))

# Run cluster algorithm

try:
    exec(open(path+'/Algorithms_large/CNN_yes.py').read())
except:
    print ('Error: Algorithm-file not found or no distance matrix found')
    sys.exit(1)

Software=str(args.Softwarepath)

print ('Clustering finished')
    
# Stop clustering time II
        
ende=time.clock()

# Time calculation

timet=ende-start

#timepp=endepp-startpp
timel=endel-startl

#timecp=timet+timepp
timetot=timet+timel

print ('Time for the clustering process: %.2f s' %(timet))

# Determine number of clusters and clustersize

Cs=np.zeros((2,N))

for a in range(0,N):
    Ca=Clust[a]
    if np.int_(np.shape(Ca)) > 1:
        Cs[0,a]=np.int_(np.shape(Ca))
        Cs[1,a]=a
        
(a1,Nc)=np.int_(np.shape(np.nonzero(Cs[0])))
Cmax=np.int_(np.max(Cs[0]))

Ncl= np.count_nonzero(np.extract(Cs[0,:]>=Nl,Cs))

# Percentage of the largest cluster

Pc=float(Cmax)/float(N)

# Determine number of noise points

Nn=float(N)-np.sum(Cs[0,:])
Pcn= 1-(np.sum(Cs[0,:])/float(N))

# Print Outcome

Ab='Parameters: rc = %.2f, nnnc = %d' %(rc, nnnc)
#print Ab

print ('%d Cluster(s) found' %(Nc))

print ('%d Cluster(s) found that have at least %d Members' %(Ncl, Nl))

print ('Largest cluster found: %d (Percentage: %.2f)' %(Cmax, Pc))

print ('Number of datapoints declared as noise: %d (Percentage: %.2f)' %(Nn, Pcn))

# Write output-files

summsave=str(args.Output)
Clf=str(args.Clusterfile)
Csf=str(args.Clustersizefile)

pickle.dump(Clust, open(Clf, 'wb'))            # Clusterlist
pickle.dump(Cs, open(Csf, 'wb'))           # Clustersize
output=open(summsave,'w')
output.write('Summary:\n\n')
output.write('**********************\n\n')
output.write('Settings:\n\n')
output.write('Algorithm used: %s\n' %(Algo))
if Algo=='CNN' or Algo=='JP':
    output.write('Special criterium: %s\n' %(Var))
output.write('Number of datapoints %d\n' %(N))
output.write('%s\n\n' %(Ab))
output.write('**********************\n\n')
output.write('Results:\n\n')
output.write('Time for the loading of the distance matrix: %.2f s\n' %(timel))
output.write('Time for the clustering process: %.2f s\n' %(timet))
output.write('Total time: %.2f s\n' %(timetot))
output.write('%d Cluster(s) found\n' %(Nc))
output.write('%d Cluster(s) found that have at least %d Members\n' %(Ncl, Nl))
output.write('largest cluster found: %d (Percentage: %.2f)\n' %(Cmax, Pc))
output.write('Number of datapoints declared as noise: %d (Percentage: %.2f)\n\n' %(Nn, Pcn))
output.write('**********************\n\n')
output.close()

output=open('02_Isolate.sh','w')
output.write('#!/bin/bash \n')
output.write('\n')
output.write('# Input \n')
output.write('\n')
output.write('Path=. \n')
output.write('Software=%s \n' %Software)
output.write('Input=${Path} \n')
output.write('Output=${Path} \n')
output.write('\n')
output.write('Inc=%s \n' %Clf)
output.write('Ins=%s \n' %Csf)
output.write('Nci=%d \n' %Ncl)
output.write('Out=frames.ndx \n')
output.write('\n')
output.write('Plo=NO \n')
output.write('Ind=%s \n' %distload)
output.write('\n')
output.write('# Execution')
output.write('\n')
output.write('python ${Software}/02_Isolate_cluster.py -Inc ${Input}/${Inc} -Ins ${Input}/${Ins} -Nci ${Nci} -Out ${Output}/${Out} -Plo ${Plo} -Ind ${Ind}')
output.close()

output=open('04_Merge_all.sh','w')
output.write('#!/bin/bash \n')
output.write('\n')
output.write('# Input \n')
output.write('\n')
output.write('Path=. \n')
output.write('Software=%s \n' %Software)
output.write('Input=${Path} \n')
if Auto == "YES":
    output.write('Input2=${Path}/../../.. \n')
if Auto == "NO":
    output.write('Input2=${Path} \n')
output.write('Output=${Path} \n')
output.write('\n')
output.write('Cut=%.6f \n' %rc)
output.write('Sim=%d \n' %nnnc)
output.write('Nc=%d \n' %Ncl)
output.write('\n')
output.write('Fra=frames.ndx\n')
output.write('\n')
output.write('# Execution\n')
output.write('\n')
output.write('for i in {0..%d}\n' %(Ntr-1))
output.write('do\n')
output.write('\tOut=Trace_${i}.npy\n')
output.write('\tMap=dist_comp${i}.npy\n')
output.write('\tpython ${Software}/04_Merge.py -Nc ${Nc} -Cut ${Cut} -Sim ${Sim} -Fra ${Input}/${Fra} -Map ${Input2}/${Map} -Out ${Output}/${Out}\n')
output.write('done')
output.close()

output=open('04_Distmat.sh','w')
output.write('#!/bin/bash \n')
output.write('\n')
output.write('# Input \n')
output.write('\n')
output.write('Path=. \n')
output.write('Software=%s \n' %Software)
output.write('Input=${Path} \n')
if Auto == "YES":
    output.write('Input2=${Path}/../../.. \n')
if Auto == "NO":
    output.write('Input2=${Path} \n')
output.write('Output=${Path} \n')
output.write('\n')
output.write('Inc=%s \n' %Clf)
output.write('Ins=%s \n' %Csf)
output.write('Nci=1 \n')
output.write('\n')
output.write('Ind=dist.npy \n')
output.write('\n')
output.write('Out=dist \n')
output.write('\n')
output.write('# Execution')
output.write('\n')
output.write('python ${Software}/04_Isolate_distmat.py -Inc ${Input}/${Inc} -Ins ${Input}/${Ins} -Nci ${Nci} -Ind ${Input2}/${Ind} -Out ${Output}/${Out} \n')
output.close()

output=open('02_Translate.sh','w')
output.write('#!/bin/bash \n')
output.write('\n')
output.write('# Input \n')
output.write('\n')
output.write('Path=. \n')
output.write('Software=%s \n' %Software)
output.write('Input=${Path} \n')
output.write('Input2=${Path} \n')
output.write('Output=${Path} \n')
output.write('\n')
output.write('Fra= # Otimized Cluster\n')
output.write('Inf= # Name of new frame-File \n')
output.write('Inr=frames.ndx \n')
output.write('\n')
output.write('Out= # Name of translated File \n')
output.write('\n')
output.write('# Execution')
output.write('\n')
output.write('python ${Software}/02_Translate_Hierarchical.py -Fra ${Fra} -Inf ${Input}/${Inf} -Inr ${Input2}/${Inr} -Out ${Output}/${Out}\n')
output.close()

output=open('03_Evaluate_2D.sh','w')
output.write('#!/bin/bash \n')
output.write('\n')
output.write('# Input \n')
output.write('\n')
output.write('Path=. \n')
output.write('Software=%s \n' %Software)
output.write('Input=${Path} \n')
if Auto == "YES":
    output.write('Input2=${Path}/../../.. \n')
if Auto == "NO":
    output.write('Input2=${Path} \n')
output.write('Output=${Path} \n')
output.write('\n')
output.write('Inf=frames.ndx \n')
output.write('Ref=reduced_data.npy \n')
output.write('\n')
output.write('Fig=Scatter.png \n')
output.write('Cln=50 \n')
output.write('\n')
output.write('# Execution')
output.write('\n')
output.write('python ${Software}/03_Evaluate_cluster_2D.py -Inf ${Input}/${Inf} -Ref ${Input2}/${Ref} -Fig ${Output}/${Fig} -Cln ${Cln}\n')
output.close()

print ('Output-files written')
