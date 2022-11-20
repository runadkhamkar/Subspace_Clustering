
from sklearn.preprocessing import *
from imblearn.over_sampling import SMOTE 
import numpy as np
import pandas as pd
import random,math
def preprocess(main_df):
	names=main_df.columns.tolist()
	label=list(main_df[names[-1]])
	df=main_df.loc[:,names[:-1]]
	df=df.values.tolist()
	l=[[] for i in range(len(df[0]))]
	mnu=[0 for i in range(len(df[0]))]
	for i in df:
		for j in range(len(df[0])):
			mnu[j]+=i[j]
			l[j].append(i[j])
	mnu=[i/len(df) for i in mnu]
	s=[np.std(i) for i in l]
	data=[]
	for i in df:
		temp=[]
		for j in range(len(df[0])):
			temp.append((i[j]-mnu[j])/s[j])
		data.append(temp)
	for i in range(len(data)):
		data[i].append(label[i])
	df=pd.DataFrame(data)
	return df,mnu