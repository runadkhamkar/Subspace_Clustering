import numpy as np
import pandas as pd
import random,math
import matplotlib.pyplot as plt
import pickle,sys
from Initialization import *
from mutation import *
from sorting import *
from preprocessing import *
from scipy import stats
from clusterify import *
from fine_tunning import *
from tournament import *
from cluster_optimizer import *
from objective import *


#  No data preprocessing

path=".\dataset"
file=path+"\\breast_cancer\\wdbc_clean.csv"
#file="F:\\Project\\dataset\\glass_clean.data"
#file="F:\\Project\\dataset\\pendigits_clean.data"
#file="F:\\Project\\dataset\\liver\\bupa.data"
#file="F:\\Project\\dataset\\diabetes.csv"
#file="F:\\Project\\dataset\\vowel_clean.data"
#file="F:\\Project\\dataset\\iris.data"
#file="F:\\Project\\dataset\\synthetic3.data"
df=pd.read_csv(file)
df=df.apply(pd.to_numeric)
#df=df.sample(frac=1)
names=df.columns.tolist()
classes=df[names[-1]].unique()
label=list(df[names[-1]])
M=3*len(classes)
M=10
names=df.columns.tolist()
classes=df[names[-1]].unique()
print("Total classes are:",classes,", shape",df.shape)
sc_max=(len(classes)*math.ceil((df.shape[1]-2)))*5
print("SC_max=",sc_max)
#df=df.loc[:,names[1:]]	#removing index and class type for selecting centers
# In[]
old_models=[]
df1=df.values.tolist()
mnu=[0 for i in range(df.shape[1])]
for i in df1:
    for j in range(len(df1[0])):
        mnu[j]+=i[j]
mnu=[i/len(df) for i in mnu]
#df,mnu=preprocess(df)
main_df=df
tp=[]
#df=pd.DataFrame(preprocess(df))

print(main_df.head())
Acc=[]
best_a=0

#try:
for iteration in range(2):
    print(iteration)
    df=main_df.sample(frac=0.75)
    members=[]
    if(iteration==0):
        for i in range(M):
            names=main_df.columns.tolist()
            label=list(main_df[names[-1]])
            df=main_df.loc[:,names[:-1]]
            print(df.shape,main_df.shape)
            u,v=initialize(df,sc_max,classes)
            u,v,members,labels=cluster_map(main_df,u,v)
            acc,ent,psm,sil,icc=get_objective(main_df,members,labels,u,v)
            if(acc>best_a):
                best_a=acc
                best_sol=[u,v,members,labels]
            Acc.append([acc,ent])
            print(i,acc,ent,len(v[0]))
            temp=[u,v,psm,icc,ent]
            old_models.append(temp)
            continue
    else:
        new_models=[]
        for i in range(M):
            x=old_models[i]
            u,v=x[0],x[1]
            u,v=mutation(u,v,sc_max,df,mnu)
            u,v,members,labels=cluster_map(main_df,u,v)
            u,v=clustering(u,v,main_df)
            u,v,members,labels=cluster_map(main_df,u,v)
            acc,ent,psm,sil,icc=get_objective(main_df,members,labels,u,v)
            if(acc>best_a):
                best_a=acc
                best_sol=[u,v,members,labels]
            Acc.append([acc,ent])
            print(iteration,i,acc,ent,icc,len(v[0]))
            temp=[u,v,psm,icc,ent]
            new_models.append(temp)
        data=[]
        obj=[]
        se=[]
        if(acc==1):
            break
        for m in old_models:
            data.append(m)
            obj.append([m[-2],m[-1]])
        for m in new_models:
            data.append(m)
            obj.append([m[-2],m[-1]])
        sol,ind=nsga(obj)
        old_models=[]
        for i in ind:
            old_models.append(data[i])
data=old_models
#pickle.dump(tp,open("./iterative.txt","wb"))
pickle.dump(Acc,open("./iterative.txt","wb"))
l=[Acc[i][0] for i in range(0,len(Acc))]
print("accuracy:",stats.describe(l))

pickle.dump(best_sol,open("best_solution.txt","wb"))




members=[]
l=[]
avg_dim=0
clu=0
ncluster=[]
for i in data:
    if([i[0],i[1]] not in l):
        l.append([i[0],i[1]])
        print(np.sum(np.array(i[1]))/len(i[1]))
        ncluster.append(len(i[1]))
print(stats.describe(ncluster))
a=0
b=0
J=0
B=0
all_labels=[]
final_obj=[]
A=[]
E=[]
for i in l:
    a=0
    B=0
    u,v,member,labels=cluster_map(main_df,i[0],i[1])
    for x in v:
        print(x)
    acc,ent,psm,sil,icc=get_objective(main_df,member,labels,i[0],i[1])
    A.append(acc)
    E.append(ent)
    members.append(member)
    all_labels.append(labels)
    final_obj.append([acc,ent])
    print("Accuracy:",acc,"Entropy",ent,"ICC:",icc,"PSM:",psm,"sillout:",sil)
    print("=="*50)

print("best accuracy so far:",best_a)

print(stats.describe(A),stats.describe(E))

pickle.dump(members,open("./members.txt","wb"))
pickle.dump(all_labels,open("./labels.txt","wb"))
pickle.dump(l,open("./solutions.txt","wb"))





