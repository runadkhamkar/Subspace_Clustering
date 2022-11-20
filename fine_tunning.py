import pandas as pd
import math,random
from sklearn import metrics
import pareto
from scipy import stats




def nonDominating_sort(data):
    x=[]
    while(len(x)<len(data)):
        nd=pareto.eps_sort(data)
        data=[i for i in data if i not in nd]
        x.append(nd)
    return x

def sorted(data):
	ind=[]
	x=nonDominating_sort(data)
	for i in range(len(data)):
		ind.append(data.index(data[i]))
	return ind


def get_entropy(l):
	d={}
	for i in l:
		if(i not in d.keys()):
			d[i]=1
		else:
			d[i]+=1
	l=list(d.values())
	l=[i/sum(l) for i in l]
	return stats.entropy(l,base=2)


def icc(l,u):
	d=0
	if(len(l)==0):
		return 1
	ind=[i for i in range(len(u)) if u[i]!=0]
	for i in l:
		x=0
		for j in ind:
			x+=(i[j]-u[j])**2
		d+=math.sqrt(x)
	return d/len(l)


def fine_tunning(members,labels,u,v,df,start=0.5,end=0.75):
	if(len(u)<4):
		return u,v
	names=df.columns.tolist()
	label=list(df[names[-1]])
	df=df.loc[:,names[:-1]]
	df=df.values.tolist()
	all_data=[]
	for i in members:
		temp=[]
		for j in range(len(i)):
			if(i[j]==1):
				temp.append(df[j])
		all_data.append(temp)
	obj=[]
	print("Fine_tunning:",len(u),len(labels))
	for i in range(len(labels)):
		s=get_entropy(labels[i])
		ic=icc(all_data[i],u[i])
		obj.append([s,ic/sum(v[i])])
	ind=sorted(obj)
	n=int(len(ind))
	n=max(4,int(n*0.66))
	u_1=[]
	v_1=[]
	#print(ind,n)
	for i in range(n):
		u_1.append(u[ind[i]])
		v_1.append(v[ind[i]])
	return u_1,v_1