import numpy as np
import matplotlib.pyplot as plt
import pickle

data = np.load('Trace_0.npy','r')

#color1=['#F70000','#970101','#520000','#3B0000']
#color2=['#2644EE','#051CA3','#04125E','#00093B']

color = ["#FF4A46","#0000A6","#008941", "#000000", "#CCAA35", "#1CE6FF", "#FF34FF", "#5A0007", "#006FA6", "#A30059", "#FF8000", "#7A4900", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",  "#809693", "#688A08", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80", "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100", "#5293CC", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F", "#372101", "#FFB500", "#68FFD2", "#A079BF","#CC0744", "#C0B9B2", "#C2FF99", "#001E09", "#00489C", "#6F0062"]

Ref=pickle.load(open('Coord.p','rb'))

xmin=np.min(Ref[:,0])
xmax=np.max(Ref[:,0])

ymin=np.min(Ref[:,1])
ymax=np.max(Ref[:,1])

fig, ax = plt.subplots()
plt.scatter(Ref[:,0],Ref[:,1],c='k',edgecolor='face',s=3, alpha=0.1)
for i in range(1,int(np.max(data))+1):  
    plt.scatter(Ref[data==i,0],Ref[data==i,1],edgecolor='face',c=color[i-1],s=3)
plt.xlim([xmin,xmax])
plt.ylim([ymin,ymax])
ax.spines['bottom'].set_linewidth('2')
ax.spines['top'].set_linewidth('2')
ax.spines['left'].set_linewidth('2')
ax.spines['right'].set_linewidth('2')
plt.savefig('Cores.png')
