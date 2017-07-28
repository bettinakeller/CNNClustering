# -*- coding: utf-8 -*-
"""
Created on Tue Oct  7 12:29:23 2014

@author: Oliver Lemke
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

# Read Input from command line with options

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('-In','--Input', type=str, help='Input: Distance matrix (default=dist.npy)', default='dist.npy') 
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)
 
# Load data and check for errors
    
try:
    Clload=str(args.Input)
    x=np.load(Clload,mmap_mode='r')
except:
    print ('Error: Distance matrix not found')
    sys.exit(1)
   
# Define Parameters

Nbin=100                    	# Number of bins
width=np.max(x)/float(Nbin)     # Width of the bins

# Generate histdata

(hist,hbin)=np.histogram(x,bins=Nbin)

# Plot histdata

fig,ax=plt.subplots()
rf=ax.bar(hbin[0:Nbin], hist, width)

xmax=np.max(x)
ymax=np.max(hist)

plt.axis([0, xmax, 0, ymax*1.1])
plt.xlabel('Distance / [AU]')
plt.ylabel('Amount of appearance')
plt.tight_layout()
fig.savefig('Hist.png')
plt.close()
