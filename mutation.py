# In[]
import numpy as np
import pandas as pd
import random,math,sys
from Initialization import *
from scipy.stats import binom
from statistics import mode


# In[]

'''
file="F:\\Project\\dataset\\glass\\glass.data"
df=pd.read_csv(file,header=None)
df=df.apply(pd.to_numeric)
names=df.columns.tolist()
classes=df[names[-1]].unique()
M=3*len(classes)
names=df.columns.tolist()
classes=df[names[-1]].unique()
print("Total classes are:",classes,", shape",df.shape)
sc_max=len(classes)*math.ceil((df.shape[1]-2)/2)
print("SC_max=",sc_max)
df=df.loc[:,names[1:-1]]


u,v=initialize(df,sc_max,classes)

for i in v:
    print(i)

'''

# In[]

def exogenous_material_uptake(df,u,v,sc_max):
	ind=random.choice(range(0,df.shape[0]-1))
	f=math.ceil(df.shape[1]/2)
	f=random.choice(range(1,f))
	#print("f",f)
	sample=df.iloc[ind].tolist()
	#print(sample)
	u1=[0 for i in range(df.shape[1])]
	v1=[0 for i in range(df.shape[1])]
	l=random.sample(range(df.shape[1]),f)
	#print(l)
	for i in l:
		u1[i]=sample[i]
		v1[i]=1
	#print("New created:",v1)
	flag=1
	intersection=[]
	Probability=2*f/(len(v)+f)
	#print("New trait probability 1:",Probability)
	max_match=-1
	for i in range(len(v)):
		match=0
		for j in range(len(v1)):
			if(v[i][j]==v1[j] and v1[j]==1):
				match+=1
				if(max_match<match):
					max_match=match
		intersection.append([i,match])
	if(Probability>0.2):
		flag=0
	temp=[i for i in intersection if i==max(intersection)]
	#print("New trait probability:",Probability,"max match:",max_match)
	#print("Proposed prob:",Probability*(f-len(intersection)+len(temp)),"flag:",flag)
	#print("intersection:",intersection,flag)
	if(flag==0):
		#print("One more genotype is added p:",Probability)
		v.append(v1)
		u.append(u1)
		return u,v
	else:
		indices=[i[0] for i in intersection if(i[1]==max_match)]
		if(len(indices)!=0):
			current_center=random.sample(indices,1)[0]
		else:
			current_center=random.sample(range(len(u)),1)[0]
		#print("centers:",current_center)
		x=v[current_center]
		for i in range(len(v1)):
			if(v[current_center][i]==v1[i] and v1[i]==1):
				u[current_center][i]+=u1[i]
				u[current_center][i]/=2
			elif(v[current_center][i]==0 and v1[i]==1):
				u[current_center][i]=u1[i]
				v[current_center][i]=1
		return u,v
# In[]

def modify(l):
	temp=[random.uniform(i-1,i+1) for i in l]
	new=[]
	for i in range(len(l)):
		if(l[i]==0 and type(i)==int):
			new.append(0)
		else:
			new.append(temp[i])
	return new

def deletion(feature_center,v,u,delta,Vfeature_center):
	delta=abs(delta)
	print("deletion delta:",delta)
	n=0
	temp=delta
	total=delta
	current=[sum(i) for i in v]
	#print("Current avilable:",current)
	while(delta>0):
		#print(temp)
		ind=random.choice(range(len(u)))
		max_elements=current[ind]
		if(delta==1):
			change=Vfeature_center.index(1)
			if(v[ind][change]!=0):
				u[ind][change]=0
				v[ind][change]=0
			return u,v
		elif(max_elements==1):
			x=1
			available=[i for i in range(len(Vfeature_center)) if Vfeature_center[i]==1]
			l=random.sample(available,x)
			delta-=x
			#print("selected deletion genes:",x,"delta:",delta)
			for i in l:
				u[ind][i]=0
				v[ind][i]=0
				x-=1
			continue
		x=random.choice(range(1,min(max_elements,delta)))
		available=[i for i in range(len(Vfeature_center)) if Vfeature_center[i]==1]
		l=random.sample(available,x)
		delta-=x
		#print("selected deletion genes:",x,"delta:",delta)
		for i in l:
			u[ind][i]=0
			v[ind][i]=0
			x-=1
	return u,v

"""
def duplication(feature_center,v,u,delta,Vfeature_center):
	print("duplication delta:",delta)
	feature_center=modify(feature_center)
	#print("Modified features in duplication:",feature_center)
	n=0
	temp=delta
	total=delta
	while(n != delta):
		if(temp==1):
			x=1
		else:
			x=random.choice(range(1,temp))
		n+=x
		ind=random.choice(range(len(u)))
		for i in range(len(Vfeature_center)):
			if(Vfeature_center[i]==1 and x>=0):
				if(u[ind][i]!=0 and type(u[ind][i])!=int):
					u[ind][i]+=feature_center[i]
					u[ind][i]/=2
				elif(x>=0):
					u[ind][i]=feature_center[i]
				x-=1
		temp-=x
	return u,v
"""

def duplication(feature_center,v,u,delta,Vfeature_center):
	features=[i for i in range(len(Vfeature_center)) if Vfeature_center[i]==1]
	#features=[0,1,7,8]
	delta=abs(delta)
	print("Duplication delta:",delta)
	while(delta>0):
		if(delta==1):
			ind=random.choice(range(0,len(v)))
			change=Vfeature_center.index(1)
			if(v[ind][change]!=0):
				u[ind][change]+=feature_center[change]
				u[ind][change]/=2
			else:
				u[ind][change]=feature_center[change]
			return u,v
		ind=random.choice(range(0,len(v)))
		select=random.choice(range(1,delta))
		#print("selected:",select)
		delta-=select
		l=random.sample(features,select)
		for i in l:
			features.remove(i)
			if(v[ind][i]!=0):
				u[ind][i]+=feature_center[i]
				u[ind][i]/=2
				u[ind][i]=round(u[ind][i],3)
			else:
				u[ind][i]=feature_center[i]
				v[ind][i]=1
	return u,v



def deletion_duplication(df,u,v,sc_max,udd=0.001):
	n=len(v)
	#print("Original phenotypes:",u)
	required=np.random.binomial(n,udd)
	u_1=list(u)
	#print(required)
	# not clear about iterations (binomial arbitory value[int])
	n_iterations=required      #random value (patch up)
	clusters_list=[sum(i) for i in v]
	for iterator in range(n_iterations):
		ind=random.choice(range(n))
		#random features tou value
		feature_center=[]
		Vfeature_center=[]
		#print(u[ind],v[ind])
		l=[i for i in range(0,len(v[ind])) if v[ind][i]==1]
		#print(l)
		if(len(l)==0):
			iterator=0
			continue
		if(len(l)==1):
			tou=1
		else:
			tou=random.choice(range(1,len(l)))
			l=random.sample(l,tou)
		#print(l,tou)
		for i in range(len(v[ind])):
			if(i in l):
				feature_center.append(u[ind][i])
				Vfeature_center.append(1)
			else:
				feature_center.append(0)
				Vfeature_center.append(0)
		delta=0
		l=[i for i in range(-tou,tou+1)]
		l.remove(0)
		delta=random.choice(l)
		#print(delta,tou,l,feature_center)
		if(delta<0):
			u,v=deletion(feature_center,v,u,delta,Vfeature_center)
		else:
			u,v=duplication(feature_center,v,u,delta,Vfeature_center)
		#print("\n\n")
		#else:
		#	u,v=duplication(feature_center,v,u,delta,Vfeature_center)
	return u,v

#deletion_duplication(df,u,v,sc_max)
# In[]




def create_B1(B):
    B1=[[] for i in range(len(B[0]))]
    for i in range(len(B)):
        for j in range(len(B[0])):
            B1[j].append(B[i][j])
    return B1



def zipf(u,v,mnu):
	v_1=create_B1(v)
	l=[sum(i) for i in v_1]
	ind=[i for i in range(len(l)) if l[i]==0]
	d=[0 for i in range(len(l))]
	p=[0 for i in range(len(l))]
	for i in ind:
		d[i]=1
		p[i]=mnu[i]
	u.append(p)
	v.append(d)
	d=[]
	for i in l:
		if(i not in d):
			d.append(i)
	d=sorted(d)
	x=d[int(len(d)/2)]
	#x=mode(d)
	d=[]
	u_1=[]
	for i in range(len(l)):
		if(l[i]<=x):
			d.append(1)
			u_1.append(mnu[i])
		else:
			d.append(0)
			u_1.append(0)
	#print(u_1,d)
	u.append(u_1)
	v.append(d)
	return u,v



def mutation(u,v,sc_max,df,mnu):
	names=df.columns.tolist()
	df=df.loc[:,names[:-1]]
	u1,v1=exogenous_material_uptake(df,u,v,sc_max)
	u1,v1=deletion_duplication(df,u1,v1,sc_max)
	#print(len(u1))
	u1,v1=zipf(u1,v1,mnu)
	#print(v1)
	return u1,v1
#mutation(u,v,sc_max,df)



# In[]




















