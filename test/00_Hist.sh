#!/bin/bash

# Input

Path=.
Software=../Algorithms/Software   ##### Important !!!!
Input=${Path}

Dist=dist.npy

# Execution

python ${Software}/00_Hist_distMatrix.py \
-In ${Input}/${Dist} \
