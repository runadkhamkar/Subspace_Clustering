# In[]
import numpy as np
import pandas as pd
import random,math

def initialize(df,SC_max,classes):
    #print(df[:5])
    # In[]
    U=[]	#phenotypes
    V=[]   	#genotypes
    l=[]
    n=max(10,len(classes))
    for i in range(n):
        while(True):
            ind=random.choice(range(0,df.shape[0]-1))
            if(ind not in l):
                l.append(ind)
                break
        f=math.ceil(df.shape[1]/2)
        temp=df.iloc[ind].tolist()
        f=random.choice(range(2,df.shape[1]))
        co_ordinates=random.sample(range(0,len(temp)),f)
        v=[0 for i in range(len(temp))]
        for i in range(len(temp)):
            if(i not in co_ordinates):
                temp[i]=0
                continue
            v[i]+=1
        U.append(temp)
        V.append(v)
    return U,V
"""u,v,sc_max=initialize("F:\\Project\\dataset\\glass\\glass.data") 
print(u,v,sc_max)"""
# In[]
'''
ind=random.sample(range(0,df.shape[0]-1),SC_max)    #selecting random indices with equal probabilities
print("Indices are selected uniformly")
for i in ind:
    u=df.iloc[i].tolist()
    v=[0 for x in range(len(u))]
    f=math.ceil(df.shape[1]/2)
    for k in range(len(classes)):
        x=random.sample(range(0,df.shape[1]),f)
        for j in x:
            v[j]+=1
    U.append(u)
    V.append(v)
print(U[:5])
print(V[:5],sum(V[0]))
'''