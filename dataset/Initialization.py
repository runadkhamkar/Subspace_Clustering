import numpy as np
import pandas as pd
import random,math

df=pd.read_csv("glass.data",header=None)
df=df.apply(pd.to_numeric)
print(df[:5])

U=[]	#phenotypes
V=[]   	#genotypes

names=df.columns.tolist()
classes=df[names[-1]].unique()

print("Total classes are:",classes,", shape",df.shape)

SC_max=len(classes)*math.ceil((df.shape[1]-2)/2)
print("SC_max=",SC_max)


df=df.loc[:,names[1:-1]]	#removing index and class type for selecting centers
ind=random.sample(range(0,df.shape[0]-1),SC_max)	#selecting random indices with equal probabilities

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