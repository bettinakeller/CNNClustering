#!/bin/bash

# Input

Path=.
Software=/INSERT_FULL_PATH/Algorithms/Software   ##### Important !!!!
Input=${Path}/../../../
Output=${Path}

# Optional Input

Dist=dist.npy
For=Mat
Nl=10
Screen=YES
Ntr=1

# Optinal Output

Out=Summary.txt
Clf=Cluster.p
Csf=Clustersize.p

# Execution

mkdir Results
cd Results

for Cut in 0.05 0.1 0.2
do
	mkdir Cut_${Cut}
	cd Cut_${Cut}
	for Sim in 2 5 10 15
	do
		mkdir Sim_${Sim}
		cd Sim_${Sim}
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
		-Screen ${Screen} &
		cd ..
	done
	cd ..
	sleep 60s      # Every Clustering needs 1 CPU => Time for clustering of 10,000 Data points approx. 30 seconds
done
