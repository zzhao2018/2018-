from random import *
import math
import copy
import getParameterValue
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
def nn(dataSet,label,q,step,alpha,Type):
    L=len(dataSet)
    LL=L
    d=len(dataSet[0])
    #init
    V=getParameterValue.getInitV(Type)
    W=getParameterValue.getInitW(Type)
    b1=getParameterValue.getInitB1(Type)
    b2=getParameterValue.getInitB2(Type)
     #init input level
#    V=initNN(d,q)
     #init hide level
#    W=initNN(1,q)[0]
     #init yuzhi
#    b1=initNN(1,q)[0]
#    b2=random()
     #init parameter
    s=0
    bestW=[]
    bestV=[]
    bestB1=0
    bestB2=0
    minErr=10000000
    while s<step:
        #forward
        O,pre=getAllPredict(dataSet,V,W,b1,b2)
        #get the best para
        absErr=getAbsErr(pre,label)
        if absErr<minErr:
            minErr=absErr
            bestW=W
            bestV=V
            bestB1=b1
            bestB2=b2
        #backward
         #second level backward
        deltaW=getDeltaW(alpha,pre,O,label)
        deltab2=getDeltaB2(alpha,pre,O,label)
         #first level backward
        deltaV,deltab1=getDelta(alpha,pre,W,O,dataSet,d,q,label)
        #updata
        W=add(W,deltaW)
        V=add(V,deltaV)
        b1=add(b1,deltab1)
        b2=b2+deltab2
        s+=1
#    print 'mimErr:',minErr
#    print 'V:',bestV
#    print 'VW:',bestW
#    print 'b1:',bestB1
#    print 'b2:',bestB2
    return bestV,bestW,bestB1,bestB2

def getAbsErr(pre,label):
    L=len(pre)
    Sum=0
    for i in range(L):
        Sum+=abs(pre[i]-label[i])
    return Sum


def getAllPredict(dataSet,V,W,b1,b2):
    allPre=[]
    allO=[]
    for ele in dataSet:
        O,pre=predict(ele,V,W,b1,b2)
        allPre.append(pre)
        allO.append(O)
    return allO,allPre


#get deltaW
def getDeltaW(alpha,pre,O,label):
    q=len(O[0])
    m=len(pre)
    deltaW=[]
    for h in range(q):
        Sum=0
        for i in range(m):
            Sum+=(pre[i]-label[i])*O[i][h]
        deltaW.append(-alpha*Sum)    
    return deltaW


#get deltab1
def getDeltaB2(alpha,pre,O,label):
    m=len(pre)
    Sum=0
    for i in range(m):
        Sum+=(pre[i]-label[i])
 #   print Sum
 #   print '*'*25
    return alpha*Sum

#get deltav
def getDelta(alpha,pre,W,O,data,d,q,label):
    m=len(pre)
    deltaV=initNN(d,q)
    deltab1=initNN(1,q)[0]
    for h in range(q):
        for i in range(d):
            Sum=0
            for j in range(m):
                Sum+=(pre[j]-label[j])*O[j][h]*(1-O[j][h])*data[j][i]
            deltaV[i][h]=-alpha*Sum*W[h]

    for h in range(q):
        Sum=0
        for j in range(m):
            Sum+=(pre[j]-label[j])*O[j][h]*(1-O[j][h])
        deltab1[h]=alpha*Sum*W[h]
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
