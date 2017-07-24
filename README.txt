Documentation:
**********************
**********************
General:
**********************

All programs are called with python $(Program).py (e.g. python 01_Cluster-dataset.py). The input is provided using flags (see below). The scripts are written in python 3.6.1. Alternatively, a bash-script can be used to execute the python scripts (Examples included).

**********************
00_Hist_distmatrix.py
**********************

00_Hist_distmatrix.py is a software to display the distribution of the distances in a histogram plot. This software is an optional tool and can be useful to determine parameters for the cluster algorithms.

For the use of the program a distance matrix (no condensed matrix) is necessary. This matrix has to contain the distances between all pairs of data points in an (D,D)-array where D is the number of data points. This matrix can be provided by the -In option.

Input:

-In	--Input			str	Distance matrix (default = dist.npy)

**********************
01_Cluster_dataset_large.py
**********************

01_Cluster_dataset_large is a tool to cluster data points by a partitioning density based cluster algorithm. In the software the Common Nearest Neighbor cluster algorithm is implemented:

Common-Nearest-Neighbor-Algorithm (CNN):
The CNN-Algorithm (B. Keller et al. JCP, 132 (2010), p. 074110) clusters all data points which have at least N nearest neighbors within a cutoff radius R in common.

For the use of the tool a complete distance matrix (no condensed matrix) is necessary. This matrix has to contain the distances between all pairs of data points in an (D,D)-array where D is the number of data points.

At the end of the clustering process a short summary is shown in the terminal which includes the time for the clustering process (preprocessing and clustering) the number of clusters found as well as the number of points that are declared as noise. Additionally, 3 Output-files are written:

	Summary-file:
	.txt-file that contains information such as the parameters, the algorithm and the number of clusters found

	Cluster-file:
	.p-file that contains a list of all clusters

	Clustersize-file:
	.p-file that contains the size of all clusters

Additionally, it is possible to extract the number of Clusters that have at least Min members. This can be done by using the -Nl option.

New features: The bash-files for further scripts are provided as an output with all parameters included (if accessible).

Input:

-Cut	--Cutoff		float	Cutoff criterion (R)
-Sim	--Similarity		int	Criterion of similarity (N)
-In	--Input			str	Distance matrix (default = dist.npy)

Optional Input:

-Nl	--Clustersize		int	Minimal Clustersize (Min) (default = 2)
-Screen	—-Screen		str	Clustering Scan (YES or NO) (default=NO)
-Ntr	—-NumberTra		int 	Number of Number of trajectories (replica) (default=1)

Output:

-Out	--Output		str	Summary-File (default = Summary.txt)
-Clf	--Clusterfile		str	Clusterfile (.p-file) (default = Cluster.p)
-Csf	--Clustersizefile	str	Clustersizefile (.p-file) (default = Clustersize.p)

**********************
02_Isolate_cluster.py
**********************

02_isolate_cluster.py is a tool to read the generated clusterfile and extract the top M clusters in an index-file.

The tool needs at least one input-file: the cluster-file that is obtained by 01_Cluster_dataset.py 01_Cluster_dataset_large.py. Optionally the clustersizefile can be provided too, but is not necessary. If no clustersizefile is provided the clustersize will be calculated during the isolation step.

As a default the tool isolates the 5 largest clusters in the dataset. This number can be varied by using the -Nci option. Additionally it is possible to extract a single cluster using the -Nco option.

The extracted cluster(s) can be found in an Index-file which is written as an output.

Additionally, it is possible to obtain the distribution of the distances for each cluster using the -Plo YES option. Therefor a distancematrix has to be provided using the -Ind option. The histograms are saved in figures and named after the following scheme:
	$(filename)_$(clusternumber).png
The number of isolated Clusters is equal to the number of histogram plots

Input:

-Inc	--Inputcluster		str	Clusterfile (.p-file) (default = Cluster.p)
-Nci	--Number		int	Maximal number of isolated clusters (default = 5)

Optional Input:

-Ins	--Inputclustersize	str	Clustersizefile (p.file) (default = Clustersize.p) (optional)
-Nco	--Numberopt		int	Cluster that should be isolated (optional)
-Ind	--Inputdistmat		str	Distancematrix (optional) (default = dist.npy)
-Plot	--Plot			str	Plot of the histograms for each cluster (YES or NO) (default=NO)

Output:

-Out	--Output		str	Frames of the top N clusters (.ndx- or .txt-file) (default = frames.ndx)

Optional Output:

-Opt	--Outopt		str	Frames of one Cluster (.ndx- or .txt.file) (default=framescl.ndx)
-Fig	--Figure		str	Histogram-plot (only file-name) (default=Hist)
