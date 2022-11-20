import pandas as pd
import random,math
from clusterify import *
from fine_tunning import *
from tournament import *




def clustering(u,v,df,iter=1):
	for i in range(iter):
		u,v,member,label=cluster_map(df,u,v)
		u,v=make_offsprings(df,u,v,label,member)
		u,v,member,label=cluster_map(df,u,v)
		print("Number of phenotypes after make_offsprings:",len(u))
		u,v=fine_tunning(member,label,u,v,df)
		#print(len(u),len(member))
	return u,v