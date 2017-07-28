# -*- coding: utf-8 -*-
"""
Created on Mon Mar 9 2015

@author: Oliver Lemke
"""

# Stop loading time I

startl=time.clock()

print ('Loading distance matrix')

# Import Python RMSD Matrix including Error report

distload=str(args.Input)

# Load matrix line by line

dist=np.load(distload,mmap_mode='r')
N=np.int_(np.shape(dist)[0])

# Prepare neighborlist

Numbi=np.zeros((N))
distnll=[0]*N

# Sort matrix according to the distance measurement

for i in range(0,N):
    distsort=np.zeros((1,N,2))          
    distsort[0,:,0]=np.argsort(dist[i,:])+1          
    distsort[0,:,1]=np.sort(dist[i,:]) 

# Determine all Neighbors that are located within rc

    j=0
    Vecl=np.zeros((1,N))
    Vecr=np.zeros((1,N))
    while distsort[0,j,1]<=rc:
        Vecl[0,j]=distsort[0,j,0]
        j=j+1
        Numbi[i]=Numbi[i]+1
        if j==N:
            break
    nll=np.nonzero(Vecl)
    distnll[i]=Vecl[0,nll[1]]

# Calculate the total number of nearest neighbors

km=int(max(Numbi))                  # Maximal number of nearest neighbors
distn=np.zeros((N,km))              # Distance Matrix for nearest neighbors

for i in range(0,N):
    distn[i,0:len(distnll[i])]=distnll[i]           # Distance Matrix for nearest neighbors

# Clear Memory II

del distsort
del distnll

# Preset parameters for the clustering
            
cn=0                # Cluster Number
w=0                 # Control value I
Clust=[0]*N         # Preset Cluster List

# Filter noise points

Numbi[np.nonzero(Numbi<nnnc)]=0

# Stop loading time II

endel=time.clock()

# Stop clustering time I

start=time.clock()

# Clustering

print ('Clustering process started')

while w<1:    
    
    # Find maximal number of nearest neighbors
    
    Nmax=np.asarray(np.nonzero(Numbi==max(Numbi)))+1
    
    # Reset cluster
    
    C=np.zeros((1,N),dtype=int)                 
    
    # Write point with the highest density in the cluster
    
    C[0,0]=Nmax[0,0]
    
    # Cluster index
    
    cl=np.int_(1)               
    
    # Control value II
    
    cc=1
    
    # Cluster index for new added points    
    
    lv=1                                    
    ci=np.int_(np.zeros((1,N+1)))         
    
    # Mask point with the highest density
    
    Numbi[Nmax[0,0]-1]=0  

    while cc>0:

        # Reset control value II and define new limits
        
        ci[0,lv]=cl                   
        cc=0           
        
        for a in range (ci[0,lv-1],ci[0,lv]):
            
            # Extract Neighborlist of a within rc             
            
            na=np.nonzero(distn[C[0,a]-1,:])

            # Extract all reachable neighbors (rc)              
            
            Nr=distn[C[0,a]-1,na]                       
            sNr=np.shape(Nr)[1]
            
            # Compare Neighborlists of a and all reachable datapoints              
            
            for c in range(0,sNr):
                b=np.int_(Nr[0,c])
                
                # Check if point is already clustered                  
                
                if Numbi[(b-1)]>0:
                    nb=np.nonzero(distn[b-1,:])
                    
                    # List of nearest neighbors of a (Clustered) 
                    
                    Na=distn[C[0,a]-1,na]
                   
                    # List of nearest neighbors of b (Not clustered) 
                    
                    Nb=distn[b-1,nb]
                    
                    # Compare neighbors of a and b
                    
                    ttc=ismember(Na[0,:],Nb[0,:])
                    tcl=np.asarray(ttc)+1
                    tc=np.shape(np.nonzero(tcl))[1]
                    
                    # Check if b in the Nearest Neighbors of a                    
                    
                    if b in Na:
                        tb=1
                    else:
                        tb=0
                    
                    # Check if a in the Nearest Neighbors of b
                    
                    if C[0,a] in Nb:
                        ta=1
                    else:
                        ta=0
                    
                    # Check truncation criterion
                    
                    if tc >= nnnc and ta > 0 and tb > 0:
                        
                        # Add point to the cluster
                        
                        C[0,cl]=b
                        cl=cl+1;
                        cc=cc+1
                        
                        # Mask clustered point
                        
                        Numbi[b-1]=0
                        
        # Update lv
                        
        lv=lv+1                                             
                        
    # Write Cluster to the Cluster List
                        
    Cc=np.int_(C[np.nonzero(C)])                                    
    Clust[cn]=Cc
    cn=cn+1
    
    # Reset
    
    dd=0             
    
    # Truncation criteria 

    if sum(Numbi)==0:          # All particles are clustered
        w=2
    if cn==N:               # The maximal number of clusters is reached
        w=2
