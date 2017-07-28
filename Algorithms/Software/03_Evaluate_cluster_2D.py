# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 14:59:37 2015

@author: Oliver Lemke
"""

import numpy as np
import argparse
import sys
import ast
import matplotlib.pyplot as plt

# Read Input from command line with options

try:
    parser=argparse.ArgumentParser()
    parser.add_argument('-Inf', '--Inputframes', type=str, help='Input: Framefile (.ndx- or .txt-file) (default=frames.ndx)', default='frames.ndx')
    parser.add_argument('-Ref', '--Referencedata', type=str, help='Input: Coordinate file of all datapoints (.npy-file) (default=Ref.npy)', default='Ref.npy')
    parser.add_argument('-Cln', '--Clusternumber', type=int, help='Maximal number of clusters that should be analyzed (maximal 50 clusters) (default=5)', default=5)
    parser.add_argument('-Fig', '--Figure', type=str, help='Output: Scatter-plot (only file-name) (default=Scatter)', default='Scatter')
    parser.add_argument('-xmin', '--Minimalx', type=str, help='Minimal x-value that should be shown (optional)', default='default')
    parser.add_argument('-xmax', '--Maximalx', type=str, help='Maximal x-value that should be shown (optional)', default='default')
    parser.add_argument('-ymin', '--Minimaly', type=str, help='Minimal y-value that should be shown (optional)', default='default')
    parser.add_argument('-ymax', '--Maximaly', type=str, help='Maximal y-value that should be shown (optional)', default='default')
    parser.add_argument('-Scn', '--Scatter', type=str, help='Save scatterdata in an .txt-file (YES or NO) (default=NO)', default='NO')
    parser.add_argument('-Sca', '--Scatterdata', type=str, help='Output: Scatter-plot-data (only file-name) (default=Scatterdat)', default='Scatterdat')
    args=parser.parse_args()
except:
    print ('Error: False number or type of input arguments')
    sys.exit(1)

# Check for errors

try:
    frload=str(args.Inputframes)
    data=open(frload,'r')
    line=data.read().splitlines()
except:
    print ('Error: Frame-file not found')
    sys.exit(1)

try:
    refload=str(args.Referencedata)
    Ref=np.load(refload)     
except:
    print ('Error: Reference-file not found')
    sys.exit(1)

try:
    Cl=int(args.Clusternumber)
except:
    print ('Error: Clusternumber must be an integer')
    sys.exit(1)
    
if Cl<0:
    print ('Error: Number of clusters incorrect')
    sys.exit(1)

try:
    xmin=float(args.Minimalx)
except:
    xmin=np.min(Ref[:,0])
    
try:
    xmax=float(args.Maximalx)
except:
    xmax=np.max(Ref[:,0])
    
try:
    ymin=float(args.Minimaly)
except:
    ymin=np.min(Ref[:,1])
    
try:
    ymax=float(args.Maximaly)
except:
    ymax=np.max(Ref[:,1])

# Maximal number of isolated clusters

if args.Clusternumber < len(line):
    Nmax=int(args.Clusternumber)
else:
    Nmax=len(line)

if Nmax > 50:
    Nmax=50

Scat=str(args.Scatter)

if Scat!='YES' and Scat!='NO':
    print ('Error: Plotoption incorrect')
    sys.exit(1)
    
# Generate Scatter-plot-data
    
#Col='.r','.b','.g','.y','.m','.k','.c','or','ob','og','oy','om','ok','oc','dr','db','dg','dy','dm','dk'

color = ["#FF4A46","#0000A6","#008941", "#000000", "#CCAA35", "#1CE6FF", "#FF34FF", "#5A0007", "#006FA6", "#A30059", "#FF8000", "#7A4900", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",  "#809693", "#688A08", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100", "#5293CC", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F", "#372101", "#FFB500", "#68FFD2", "#A079BF","#CC0744", "#C0B9B2", "#C2FF99", "#001E09", "#00489C", "#6F0062"]

sfig=str(args.Figure)
Sdat=str(args.Scatterdata)

try:
    fig, ax = plt.subplots()
    plt.scatter(Ref[:,0],Ref[:,1],c='k',edgecolor='face',s=3, alpha=0.1)
    for i in range(0,Nmax):  
        Ca=line[i]
        C=np.asarray(ast.literal_eval(Ca))
        Data=np.copy(Ref[C,:])
        if Scat=='YES':
            Sdata=Sdat+str('_')+str(i)+str('.txt')
            output=open(Sdata,'w')
            for item in Data:
                output.write('%s, ' % (item))
            output.close()
        sfigr=sfig+str('.png')
        plt.scatter(Data[:,0],Data[:,1],edgecolor='face',c=color[i],s=3)
        plt.xlim([xmin,xmax])
        plt.ylim([ymin,ymax])
        ax.spines['bottom'].set_linewidth('2')
        ax.spines['top'].set_linewidth('2')
        ax.spines['left'].set_linewidth('2')
        ax.spines['right'].set_linewidth('2')
    plt.savefig(sfig)
except:
    print ('Error: Number of clusters too high')
    sys.exit(1)
