# In[]
import pickle,random
import matplotlib.pyplot as plt
import pareto

#data=pickle.load(open("F:\Project\Programms\First2_nsga.txt","rb"))



def nonDominating_sort(data):
    x=[]
    while(len(x)<len(data)):
        nd=pareto.eps_sort(data)
        data=[i for i in data if i not in nd]
        x.append(nd)
    return x
#nonDominating_sort(data)




def crowding_distance(f):
    l=f
    temp=[]
    for i in l:
        i.append(0)
    for m in range(len(l[0])-1):
        l=sorted(l,key=lambda x:x[m])
        l[0][-1]=l[-1][-1]=math.inf
        M=max([i[m] for i in l])
        mn=min([i[m] for i in l])
        x=M-mn
        #print(x,M,mn)
        for i in range(1,len(l)-1):
            l[i][-1]=l[i][-1]+(l[i+1][m]+l[i-1][m])/x
            temp.append(l[i][-1])
    return l
#crowding_distance(x[1])



def nsga(data):
    ind=[]
    x=nonDominating_sort(data)
    n=len(data)
    #print(n)
    consider=[]
    solutions=[]
    flag=-1
    for i in x:
        if(len(solutions)+len(i)>int(n/2)):
            flag=int(n/2)-len(solutions)
            consider=i
            break
        for j in i:
            solutions.append(j)
            ind.append(data.index(j))
    if(flag!=-1):
        consider=random.sample(consider,flag)
        for i in consider:
            solutions.append(i)
            ind.append(data.index(i))
    return solutions,ind