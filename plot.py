import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


res=pd.read_csv("Final.csv")
#print(df.head())



names=res.columns

d={i:res[i].tolist() for i in names}
plt.ylim(0,1)
w='CE'
l=d[w]
m=l.index(max(l))
print(m)
plt.scatter(d['NumCluster'],d[w])
plt.scatter(d['NumCluster'][m],d[w][m],color='red')
plt.xlabel('Number of cluster',fontweight='bold')
plt.ylabel(w,fontweight='bold')
plt.savefig(w+".png")