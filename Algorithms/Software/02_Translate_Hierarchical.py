# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 12:37:44 2015

@author: Oliver Lemke
"""

import numpy as np
import argparse
import sys
import ast

# Read Input from command line with options

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('-Fra', '--Inputframe', type=int, help='Input: Clusternumber to be translated (default=0)', default=0)
    parser.add_argument('-Inf', '--Inputframelist', type=str, help='Input: Frames of the top N clusters (default=frames_0.ndx)', default='frames_0.ndx')
    parser.add_argument('-Inr', '--Inputreferencelist', type=str, help='Input: Frames of the former clustering step (default=frames.ndx)', default='frames.ndx')
    parser.add_argument('-Out', '--Output', type=str, help='Output: Translated frames of the top N clusters (.ndx- or .txt-file) (default=frames_0n.ndx)', default='frames_0n.ndx')  
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)

# Check for errors

try:
    Rf = int(args.Inputframe)
except:
    print ('Error: Clusternumber must be an integer')
    sys.exit(1)

#Load data

try:
    frload = str(args.Inputframelist)
    frames = open(frload,'r')
    linef = frames.read().splitlines()
except:
    print ('Error: Frame-File not found')
    sys.exit(1)
    
try:
    refload = str(args.Inputreferencelist)
    ref=open(refload,'r')
    liner=ref.read().splitlines()
except:
    print ('Error: Reference-File not found')
    sys.exit(1)
    
# Translate data

Ca=liner[Rf]                            # Load frame
Ref=np.asarray(ast.literal_eval(Ca))    # Convert frame to array

try:
    fram = str(args.Output)
    output=open(fram,'w')
except:
    print ('Error: Output-File not defined')

# Write data into output

for i in range(0,len(linef)):
    Cb=linef[i]
    Cc=np.asarray(ast.literal_eval(Cb))
    C=Ref[Cc]
    output.write('[')
    for item in C:
        output.write('%s, ' % (item))
    output.write(']\n')
output.close()
