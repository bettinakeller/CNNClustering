# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 10:16:42 2017

@author: lupusnoctis
"""

import numpy as np
import matplotlib.pyplot as plt
import ast
from matplotlib import cm, colors

def ismember(a, b):
    bi = {}
    for i, el in enumerate(b):
        if el not in bi:
            bi[el] = i
    return [bi.get(itm, -1) for itm in a]

##### Input #####

ref = 'frames.ndx'		# Reference File (Old)
com = 'frames_0n.ndx'		# Frames to Compare (New)

Out = 'Decomposition.png'	# Output figure

#################

Ref = open(ref,'r').read().splitlines()
Com = open(com,'r').read().splitlines()

R=['']*len(Ref)
C=['']*len(Com)

for ind,el in enumerate(Ref):
    R[ind] = ast.literal_eval(el)
    
for ind,el in enumerate(Com):
    C[ind] = ast.literal_eval(el)

Overlap = np.zeros((len(R),len(C)))
Noise = np.zeros(len(R))
    
for ind, el in enumerate(R):
    for ind2, el2 in enumerate(C):
        Overlap[ind,ind2] = np.shape(np.nonzero(np.asarray(ismember(el,el2))>=0))[1]
    Overlap[ind,:] = Overlap[ind,:]/float(len(el))
    Noise[ind] = 1-np.sum(Overlap[ind,:])

my_cmap = cm.get_cmap('RdPu')
   
fig = plt.figure(1)
gs = plt.GridSpec(2,4,height_ratios=[0.5,len(R)],width_ratios=[len(C),1,1,0.2])
fig.set_size_inches((len(C)*(20.5/18.0))+3.2,len(R))
ax1=plt.subplot(gs[1,0])
ax2=plt.subplot(gs[1,1])
ax3=plt.subplot(gs[1,2])

cb = ax1.pcolor(Overlap[::-1,:],cmap=my_cmap,edgecolor='black',linewidth=2,vmin=0.01,vmax=1,norm=colors.LogNorm())
plt.sca(ax1)
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position('top')
plt.xticks((np.arange(0,len(C))+0.5),np.arange(1,len(C)+1),fontsize=25)
plt.yticks((np.arange(0,len(R))+0.5),np.arange(len(R),0,-1),fontsize=25)
plt.tick_params(axis='x',which='both', bottom='off', top='off')
plt.tick_params(axis='y',which='both', left='off', right='off')
ax1.spines['bottom'].set_linewidth('2')
ax1.spines['top'].set_linewidth('2')
ax1.spines['left'].set_linewidth('2')
ax1.spines['right'].set_linewidth('2')
ax1.grid(True,which='major',axis='both')
ax1.set_ylabel('Ref',fontsize=20+(len(C)*0.5))
ax1.set_xlabel('Comp',fontsize=20+(len(C)*0.5))
ax1.set_xlim([0,len(C)])
ax1.set_ylim([0,len(R)])

ax2.pcolor(np.reshape(Noise[::-1],(1,len(Noise))).T,cmap=my_cmap,edgecolor='black',linewidth=2,vmin=0.01,vmax=1,norm=colors.LogNorm())
plt.sca(ax2)
ax2.xaxis.tick_top()
ax2.xaxis.set_label_position('top')
plt.xticks((0,1),(r'$\ $',r'$\ $'),fontsize=25)
ax2.get_yaxis().set_visible(False)
plt.tick_params(axis='x',which='both', bottom='off', top='off')
plt.tick_params(axis='y',which='both', left='off', right='off')
ax2.spines['bottom'].set_linewidth('2')
ax2.spines['top'].set_linewidth('2')
ax2.spines['left'].set_linewidth('2')
ax2.spines['right'].set_linewidth('2')
ax2.set_xlabel('Noise',fontsize=20+(len(C)*0.5))
ax2.set_xlim([0,1])
ax2.set_ylim([0,len(R)])

cbar=plt.colorbar(cb,cax=ax3)
plt.sca(ax3)
cbar.ax.tick_params(labelsize=25+(len(C)*0.5),width=2)
cbar.set_ticks((0.01,0.1,1))
cbar.outline.set_linewidth(2)
ax3.set_xlim(left=-0.3)
plt.savefig(Out)
