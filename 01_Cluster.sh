#!/bin/bash

# Input

Path=.
Software=INSERT_PATH/Algorithms/Software   ##### Important !!!!
Input=${Path}
Output=${Path}

# Cluster Parameters

Cut=2
Sim=15

# Optional Input

Dist=dist.npy
For=Mat
Nl=10
Screen=NO
Ntr=1

# Optional Output

Out=Summary.txt
Clf=Cluster.p
Csf=Clustersize.p

# Execution

python ${Software}/01_Cluster_dataset_large.py \
-Cut ${Cut} \
-Sim ${Sim} \
-In ${Input}/${Dist} \
-Out ${Output}/${Out} \
-Clf ${Output}/${Clf} \
-Csf ${Output}/${Csf} \
-Nl ${Nl} \
-Spt ${Software} \
-Ntr ${Ntr} \
-Screen ${Screen}
