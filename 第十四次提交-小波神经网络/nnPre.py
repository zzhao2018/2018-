import time
import datetime
import copy
from nn import *
from dealdate import *

#get trainset
def getNNTrainSet(data,L):
    LL=len(data)
    X=[]
    Y=[]
    for i in range(LL-L):
        X.append(splitDateList(data,i,L))
        Y.append(data[i+L])
    return X,Y

#product new data
def createNewData(X,Y,pre):
    oneList=[]
    LL=len(X[0])
    for i in range(1,LL):
        oneList.append(X[-1][i])
    oneList.append(Y[-1])
    X.append(oneList)
    Y.append(pre)

#get new trainset
def getNewTrainSet(X,Y):
    oneList=[]
    LL=len(X[0])
    for i in range(1,LL):
        oneList.append(X[-1][i])
    oneList.append(Y[-1])
    return oneList

#get test set
def getnnPredictSet(beginT,endT,X,Y):
    #analyze time
    begin=time.strptime(beginT,'%Y-%m-%d')
    end=time.strptime(endT,'%Y-%m-%d')
    beginDate=datetime.datetime(begin[0],begin[1],begin[2])
    endDate=datetime.datetime(end[0],end[1],end[2])
    #count data
    Sum=0
    #copy the data
    copyX=copy.deepcopy(X)
    copyY=copy.deepcopy(Y)
    #run the nn
    V,W,b1,a=nn(copyX,copyY,4,15000,0.01)
    while beginDate<=endDate:
        oneList=getNewTrainSet(copyX,copyY)
        #predict
        O,onePre,midT=predict(oneList,V,W,b1,a)
        if onePre<0:
            onePre=0
        intPre=int(onePre)
        if onePre-intPre>0.5:
            intPre+=1
        Sum+=onePre
        createNewData(copyX,copyY,intPre)
        #move time
        beginDate=beginDate+datetime.timedelta(days=1)
    intSum=int(Sum)
    if (Sum-intSum)>0.5:
        intSum+=1
    print intSum
    print '*'*25
    return intSum
