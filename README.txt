Important: The program is automated and uses default names which can but do not have to be adjusted.

Documentation.txt contains description of all programs included in Algorithms/Software/

Additionally, four optional scripts are included to calculate the Inputs. Therefore, only the 2-3 Input Parameter in the Files have to be modified, which are in the beginning of the respective scripts. (Section „Input“)

Most of the bash scripts are generated during the clustering run, with the correct variables. However, for the start of the run the existing bash-files have to be modified. (Section “Important Scripts“) IMPORTANT: Bash-Script does not support space after variable assignment (e.g i=1 is ok; i= 1 or i = 1 is not ok).

The general clustering procedure looks like 01_Cluster.sh for the CNN-Clustering, 02_Isolate.sh to extract the frames and if 2D data sets are used 03_Evaluate_2D.sh to visualize the clusters. If a reduced data set was applied for the clustering a mapping of the complete data set onto the clusters can be achieved using 04_Merge_all.sh.

If the clustering is not sufficient you can refine clusters using 04_Distmat.sh. This script isolates the distance matrix of a single cluster which can then be used for a new clustering step. After the clustering step 02_Translate_hierarchical.sh has to be used to obtain the correct indices for the new clusters (Further information in Documentation.txt). 
Important: For the merging step the parameters that were used to extract the cluster should be applied. Therefore, for each clustering step a single merging step should be performed with updated parameters. To avoid doublings the refined clusters have to be removed manually from the original frame file(s). In the end the resulting trajectories for all merging steps have to be combined. Keep in mind that for each merging step the micro state index starts at 1. Therefore, the maximal micro state index of the current trajectory has to be added to the new added trajectory. Example:

Trajectory_step1: 4 micro states: 1 2 3 4	(new numbering 1 2 3 4)
Trajectory_step2: 3 micro states: 1 2 3		(new numbering 5 6 7)
Trajectory_step3: 3 micro states: 1 2 3		(new numbering 8 9 10)
…

=====================================

Input:

The input files can be generated using the provided scripts:

Input 1: Distance matrix nxn (Optimal 10.000 - 20.000 data points) (Calculate_dist.py)
Input 2:
    Option 1) Distance matrix nxmx2 (Calculate_MapMatrix.py, Use 04_Merge_not_reduced.py later)
    Option 2) RECOMMENDED: Distance matrix nxkx2 (Preordered to k nearest neighbors ==> Sim should be smaller than 0.1*k during Clustering!) (Calculate_MapMatrix_red.py, Use 04_Merge.py later)

=====================================

Other importants Scripts:

00_Hist.sh --> Histogram of the data set (IMPORTANT: Adjust Path!!!)
01_Cluster.sh --> Clustering of the data set (IMPORTANT: Adjust Path!!!)
01_Cluster_screen_example.sh --> Screen of the data set for different parameter sets (IMPORTANT: Adjust Path!!!)

Decomposition.py --> Compare the Outcome of two different clusterings (Example in test/)

=====================================

Example data:

Example data including the outcome (Figures, Clustering Results, ...(for: R=6, N=4, M=20 ,n=1000 (Full set n=10000))) can be found in the directory test/. In this directory a 2D data set is given (Coord.p, 10000 data points) describing a trajectory in a 3-well-2D-potential (O. Lemke, B.G. Keller, Algorithms (Special issue: Clustering Algorithms 2017) 2017, submitted). A script plot_cores.py for plotting the resulting core sets (after the mapping step) is included. Suitable parameter sets for a 1-step clustering using 1000 data points (every 10th data point) are (R=6,N=4) and for a hierarchical clustering {(R=9,N=4),(R=6,N=4)}. Additionally, an example figure for the comparison of two clustering steps is included for a more complex system (Decomposition_Example.png).

=====================================

General Procedure (1-step Clustering):

0.) Calculation of the Distance Matrix for the Reduced data set and the Map Matrix
1.) Histogramm to evaluate cut off R (left of the first maximum) (00_Hist.sh)
2.) Clustering (Single or Screen) (01_Cluster.sh/01_Cluster_screen.sh)
 --> Automated Generation of 02_Isolate.sh (Isolation of the clusters), 02_Translate.sh (Translating the frames after a hierarchical clustering step), 03_Evaluate_2D.sh (Visualization of 2D clustering results), 04_Merge_all.sh (Mapping the original data onto the cluster) and 04_Distmat.sh (Isolation of the distance matrix of a single cluster) using the used parameters
3.) Isolation of the clusters (02_Isolate.sh) and optional visualiztion of the clusters (03_Evaluate_2D.sh)
4.) Mapping of the trajectory onto the clusters (04_Merge_all.sh)

General Procedure (Multi-step Clustering):

0.) Calculation of the Distance Matrix for the Reduced data set and the Map Matrix
1.) Histogramm to evaluate cut off R (left of the first maximum) (00_Hist.sh)
2.) Clustering (Single or Screen) (01_Cluster.sh/01_Cluster_screen.sh)
 --> Automated Generation of 02_Isolate.sh (Isolation of the clusters), 02_Translate.sh (Translating the frames after a hierarchical clustering step), 03_Evaluate_2D.sh (Visualization of 2D clustering results), 04_Merge_all.sh (Mapping the original data onto the cluster) and 04_Distmat.sh (Isolation of the distance matrix of a single cluster) using the used parameters
3.) Isolation of the clusters (02_Isolate.sh) and optional visualiztion of the clusters (03_Evaluate_2D.sh)
4.) Extraction of the distance matrices for the clusters that have to be refined (04_Distmat.sh)
5.) Clustering using the new distance matrix (01_Cluster.sh) and isolation of the clusters (02_Isolate.sh)
6.) Correction of the indices of the new clusters (02_Translate.sh) and the removal of the refined cluster from the frame-file of the former step (Manually)
7.) Repeat of steps 4.)-6.) until clustering is sufficient
8.) Mapping of the trajectory onto the clusters (04_Merge_all.sh) for every clustering step
9.) Combining the projected trajectories (as described above)
