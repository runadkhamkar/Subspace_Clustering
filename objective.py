import pandas as pd
import numpy as np
import math
from sklearn import metrics
from scipy import stats




def icc(members,u,v):
	d=0
	#print(len(v),len(members))
	size=sum([len(i) for i in members])
	for i in range(len(u)):
		ind=[j for j in range(len(v[i])) if v[i][j]!=0]
		#print(ind)
		for j in members[i]:
			x=0
			for k in ind:
				#print(u[i][k])
				#print(j[k])
				x+=(u[i][k]-j[k])**2
			d+=math.sqrt(x)
	return d/size

def sillout(members,labels):
	size=sum([len(i) for i in labels])
	sill=0
	for i in range(len(labels)):
		X=members[i]
		l=labels[i]
		if(len(np.unique(np.asarray(l)))!=1):
			s=metrics.silhouette_score(X, l, metric='euclidean')
		else:
			s=0
		w=len(l)/size
		sill+=s*w
	return sill




def Accuracy_Entropy(labels,c):
	acc=0
	ent=0
	size=sum([len(i) for i in labels])
	for i in labels:
		d={}
		for j in i:
			if(j not in d.keys()):
				d[j]=1
			else:
				d[j]+=1
		x=list(d.values())
		if(len(x)==0):
			return 0,1
		weight=sum(x)/size
		a=max(x)/sum(x)
		acc+=a*weight
		x=[i/sum(x) for i in x]
		ent+=(stats.entropy(x,base=c)*weight)
		#print("Accuracy, Entropy:",a,acc,ent,weight)
	return acc,ent
def dot(K, L):
	if len(K) != len(L):
		return 0
	return sum(i[0] * i[1] for i in zip(K, L))

def fnr(v):
	n=len(v[0])
	x=(n*(n-1))/2
	if(len(v)<1):
		return sum(v[0])/x
	p=0
	for i in range(len(v)-1):
		for j in range(i+1,len(v)):
			d=dot(v[i],v[j])
			p+=d
	return p/x

def fpc(v):
	return abs(sum([sum(i) for i in v])/len(v)-(len(v[0])+1)/2)




def get_objective(df,members,labels,u,v):
	psm=(2*fpc(v)+fnr(v))
	names=df.columns.tolist()
	label=list(df[names[-1]])
	classes=len(list(df[names[-1]].unique()))
	df=df.loc[:,names[:-1]]
	df=df.values.tolist()
	a,e=Accuracy_Entropy(labels,classes)
	all_data=[]
	#print(len(members))
	for i in members:
		temp=[]
		for j in range(len(i)):
			if(i[j]==1):
				temp.append(df[j])
		all_data.append(temp)
	ic=icc(all_data,u,v)
	s=0
	return a,e,psm,s,ic