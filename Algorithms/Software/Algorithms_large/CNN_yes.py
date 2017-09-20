# Stop loading time I

startl=time.clock()

print ('Loading distance matrix')

# Import Python RMSD Matrix including Error report

distload=str(args.Input)

# Load matrix line by line

dist=np.load(distload,mmap_mode='r')
N=np.int_(np.shape(dist)[0])

# Prepare neighborlist

Numbi=np.zeros(N)
distn=[0]*N

# Calculate Neighborlist

for i in range(N):

    Vec=np.nonzero(dist[i,:]<=rc)[0]
    Numbi[i]=len(Vec)
    distn[i]=Vec   

# Preset parameters for the clustering
            
cn=0                # Cluster Number
w=0                 # Control value I
Clust=[0]*N         # Preset Cluster List

# Filter noise points

Numbi[Numbi<nnnc]=0

# Stop loading time II

endel=time.clock()

# Stop clustering time I

start=time.clock()

# Clustering

print ('Clustering process started')

while w<1:    
    
    # Find maximal number of nearest neighbors
    
    Nmax=np.nonzero(Numbi==max(Numbi))[0]
    
    # Reset cluster
    
    C=np.zeros(N,dtype=int)                 
    
    # Write point with the highest density in the cluster
    
    C[0]=Nmax[0]
    
    # Cluster index
    
    cl=int(1)               
    
    # Control value II
    
    cc=1
    
    # Cluster index for new added points    
    
    lv=0                                    
    ci=np.zeros(N,dtype=int)      
    
    # Mask point with the highest density
    
    Numbi[Nmax[0]]=0  

    while cc>0:

        # Reset control value II and define new limits
        
        ci[lv]=cl                   
        cc=0           
        
        for a in C[ci[lv-1]:ci[lv]]:
            
            # Extract Neighborlist of a within rc

            Na=distn[a]
            
            # Compare Neighborlists of a and all reachable datapoints              
            
            for b in Na:
                
                # Check if point is already clustered                  
                
                if Numbi[b]>0:

                    Nb=distn[b]
                    
                    tcc=np.asarray(ismember(Na,Nb))
                    tc=len(tcc[tcc>=0])
                    
                    # Check if b in the Nearest Neighbors of a                    
                    
                    if b in Na:
                        tb=1
                    else:
                        tb=0
                    
                    # Check if a in the Nearest Neighbors of b
                    
                    if a in Nb:
                        ta=1
                    else:
                        ta=0
                    
                    # Check truncation criterion
                    
                    if tc >= nnnc and ta > 0 and tb > 0:
                        
                        # Add point to the cluster
                        
                        C[cl]=b
                        cl=cl+1
                        cc=cc+1
                        
                        # Mask clustered point
                        
                        Numbi[b]=0
                        
        # Update lv
                        
        lv=lv+1                                             
                        
    # Write Cluster to the Cluster List
                        
    Cc=np.int_(C[:cl])                                    
    Clust[cn]=Cc
    cn=cn+1           
    
    # Truncation criteria 

    if sum(Numbi)==0:          # All particles are clustered
        w=2
    if cn==N:               # The maximal number of clusters is reached
        w=2
