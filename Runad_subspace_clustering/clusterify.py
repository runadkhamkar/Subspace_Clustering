import pandas as pd
import math
from Initialization import *


def distance(data,v,mnu,u):
    l=[]
    for j in range(len(v)):
        ind=[i for i in range(len(v[j])) if v[j][i]==1]
        dist=0
        for i in ind:
            dist+=abs(data[i]-u[j][i])
        if(len(ind)==0):
        	continue
        l.append(dist/len(ind))
    return l.index(min(l)),min(l)



def actual(df,u,v):
	names=df.columns.tolist()
	label=list(df[names[-1]])
	df2=df
	classes=df[names[-1]].unique()
	df=df.loc[:,names[:-1]]
	df1=df
	df=df.values.tolist()
	mnu=[0 for i in range(len(df[0]))]
	for i in df:
	    for j in range(len(i)):
	        mnu[j]+=i[j]
	mnu=[i/len(df) for i in mnu]
	member=[[0 for i in range(len(df))]for j in range(len(u))]
	labels=[[] for i in range(len(v))]
	for i in range(len(df)):
	    ind,dist=distance(df[i],v,mnu,u)
	    member[ind][i]=1
	    labels[ind].append(int(label[i]))
	print([len(i) for i in labels])
	ind=[]
	for i in range(len(labels)):
		if(len(labels[i])<1):
			ind.append(i)
	print("cluster_map deletion:",len(labels),len(ind))
	for i in ind[::-1]:
		member.remove(member[i])
		labels.remove(labels[i])
		del u[i]
		del v[i]
	if(len(u)==1):
		u,v=initialize(df1,0,classes)
		u,v,member,labels=cluster_map(df2,u,v)
	return u,v,member,labels


def cluster_map(df,u,v):
	xxx=0
	while(xxx<df.shape[0]):
		u,v,member,labels=actual(df,u,v)
		l=[len(i) for i in labels]
		xxx=sum(l)
	#print([len(i) for i in labels])
	return u,v,member,labels