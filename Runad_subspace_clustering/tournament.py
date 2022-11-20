from sklearn.ensemble import ExtraTreesClassifier
from sklearn.svm import LinearSVC
from sklearn.feature_selection import SelectFromModel
import random




def make_offsprings(df,u,v,labels,members):
	clf = ExtraTreesClassifier(n_estimators=50)
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
	off=[]
	lab=[]
	u_1=[]
	v_1=[]
	c=0
	for i in range(len(all_data)):
		for j in range(i+1,len(all_data)):
			c+=1
			t=all_data[i]+all_data[j]
			off.append(t)
			l=labels[i]+labels[j]
			lab.append(l)
			clf=clf.fit(t,l)
			#lsvc=lsvc.fit(t,l)
			model = SelectFromModel(clf, prefit=True,max_features=int(len(t[0])*1))
			l1=list(model.get_feature_names_out([k for k in range(len(t[0]))]))
			l=[0 for k in range(len(t[0]))]
			u1=[0 for k in range(len(t[0]))]
			ind=[0 for k in range(len(t[0]))]
			for k in t:
				for ii in range(len(k)):
					#print(k)
					ind[ii]+=k[ii]
			ind=[k/len(t) for k in ind]
			for k in range(len(l1)):
				l[l1[k]]=1
				u1[k]=ind[l1[k]]
			v_1.append(l)
			u_1.append(u1)
	print(len(u_1),len(all_data),c)
	return u_1,v_1

			

