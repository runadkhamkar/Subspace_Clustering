import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random,os,math,scipy,pickle
from sklearn.metrics import f1_score


df=pd.read_csv("F:\Project\dataset\\synthetic1.data")
cls=list(df[df.columns[-1]].unique())
df=df.loc[:,df.columns[1:]]
DF={k:[] for k in cls}
for i,r in df.iterrows():
    DF[r[df.columns[-1]]].append(list(r))

for i in DF:
    l=DF[i]
    x=[]
    y=[]
    z=[]
    for j in l:
        x.append(j[0])
        y.append(j[1])
        z.append(j[2])
    plt.xlim(-5, 5)
    plt.ylim(-5,5)
    
    plt.subplot(1,3,1)
    plt.scatter(x,y)
    plt.title("X-Y Plane")
    
    plt.subplot(1,3,2)
    plt.scatter(x,z)
    plt.title("X-Z Plane")
    
    plt.subplot(1,3,3)
    plt.scatter(y,z)
    plt.title("Y-Z Plane")
plt.show()