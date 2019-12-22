from random import *
import math
import copy
#init mat
def initNN(m,n):
    para=[]
    for i in range(m):
        para.append([])
        for j in range(n):
            para[i].append(random())
    return para

#hide level function
def fun(x):
    return 1.0/(math.exp(-x)+1.0)

#forward
def predict(data,V,W,b1,b2):
    #the num of input
    d=len(V)
    #the num of hide
    q=len(V[0])
    O=[]
    #cal the hide level
    for h in range(q):
        Sum=0
        hRes=0
        for i in range(d):
            Sum+=V[i][h]*data[i]
        hRes=fun(Sum-b1[h])
        O.append(hRes)
    #cal the result
    result=0
    for h in range(q):
        result+=W[h]*O[h]
    result-=b2
    return O,result

#n2:the number of hide level
def nn(dataSet,label,q,step,alpha):
    L=len(dataSet)
    LL=L
    d=len(dataSet[0])
    #init
     #init input level
    V=initNN(d,q)
     #init hide level
    W=initNN(1,q)[0]
     #init yuzhi
    b1=initNN(1,q)[0]
    b2=random()
     #init parameter
    s=0
    esp=0.001
    while s<step:
        j=randint(0,L-1)
        #forward
        O,pre=predict(dataSet[j],V,W,b1,b2)
        #backward
        Ek=(pre-label[j])
#        print pre
#        print label[j]
#        print Ek
#        print '*'*25
         #second level backward
        deltaW=getDeltaW(alpha,Ek,O)
        deltab2=alpha*Ek
         #first level backward
        deltaV,deltab1=getDelta(alpha,Ek,pre,W,O,dataSet[j],d,q)
        #updata
        W=add(W,deltaW)
        V=add(V,deltaV)
        b1=add(b1,deltab1)
        b2=b2+deltab2
        s+=1
    return V,W,b1,b2

#get deltaW
def getDeltaW(alpha,Ek,O):
    q=len(O)
    deltaW=[]
    for h in range(q):
        deltaW.append(-alpha*Ek*O[h])
    return deltaW
    
#get deltav
def getDelta(alpha,Ek,pre,W,O,data,d,q):
    deltaV=initNN(d,q)
    deltab1=initNN(1,q)[0]
    for h in range(q):
        s=alpha*Ek*W[h]*O[h]*(1-O[h])
        deltab1[h]=s
        for i in range(d):
            deltaV[i][h]=-s*data[i]
    return deltaV,deltab1

#array a+b
def add(a,b):
    cb=copy.deepcopy(b)
    L1=len(a)
    try:
        L2=len(a[0])
        for i in range(L1):
            for j in range(L2):
                cb[i][j]+=a[i][j]
    except:
        for i in range(L1):
            cb[i]+=a[i]
    return cb


def KnnPredict(X,Y,testData,n):
    #make the data nomal
    xf1=[x[0] for x in X]
    xf1Max=max(xf1)
    xf1Max=max(xf1Max,testData[0])
    xf1Min=min(xf1)
    xf1Min=min(xf1Min,testData[0])
    x1=[float(x-xf1Min)/float(xf1Max-xf1Min) for x in xf1]
    testData[0]=float(testData[0]-xf1Min)/float(xf1Max-xf1Min)

    xf2=[x[1] for x in X]
    xf2Max=max(xf2)
    xf2Max=max(xf2Max,testData[1])
    xf2Min=min(xf2)
    xf2Min=min(xf2Min,testData[1])
    x2=[float(x-xf2Min)/float(xf2Max-xf2Min) for x in xf2]
    testData[1]=float(testData[1]-xf2Min)/float(xf2Max-xf2Min)

    xf3=[x[2] for x in X]
    xf3Max=max(xf3)
    xf3Max=max(xf3Max,testData[2])
    xf3Min=min(xf3)
    xf3Min=min(xf3Min,testData[2])
    x3=[float(x-xf3Min)/float(xf3Max-xf3Min) for x in xf3]
    testData[2]=float(testData[2]-xf3Min)/float(xf3Max-xf3Min)

    dataSet=[]
    #get trainset
    for a1,a2,a3 in zip(x1,x2,x3):
        dataSet.append([a1,a2,a3])
    return onePre
