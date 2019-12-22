from dealdate import *
import copy
import time
import datetime

#get trainSet
def getLineTrainSet(data,L):
    LL=len(data)
    X=[]
    Y=[]
    for i in range(LL-L):
        mid=[1]
        mid.extend(splitDateList(data,i,L))
        X.append(mid)
        Y.append(data[i+L])
    return X,Y


#init the weight
def initLineW(L):
    w=[]
    weight=0.9
    for i in range(L):
        w.append(weight)
        weight=weight**2
    return w

def getErr(w,X,Y,loc):
    L=len(Y)
    Sum=0
    errPre=0
    for i in range(L):
        errPre+=(Y[i]-getLinePre(w,X[i]))
        Sum+=errPre*X[i][loc]
#    print errPre
#    print '*'*25
    return Sum,abs(errPre)

#train line
def trainLine(X,Y,alpha,step):
    Lx=len(X[0])
    Ly=len(Y)
    w=initLineW(Lx)
    s=0
    preErr=1000000
    minErr=1000000
    minW=w
    while s<step:
        if preErr<minErr:
            minErr=preErr
            minW=w
        for i in range(Lx):
            ErrSum,preErr=getErr(w,X,Y,i)
            w[i]=w[i]+alpha*ErrSum
        s+=1
    return minW

#get predict
def getLinePre(w,X):
    L=len(X)
    Sum=0
    for i in range(L):
        Sum+=w[i]*X[i]
    return Sum

#get new trainset
def getNewTrainSet(X,Y):
    oneList=[1]
    LL=len(X[0])-1
    for i in range(2,LL):
        oneList.append(X[-1][i])
    oneList.append(Y[-1])
    return oneList

#product new data
def createNewData(X,Y,pre):
    oneList=[1]
    LL=len(X[0])-1
    for i in range(2,LL):
        oneList.append(X[-1][i])
    oneList.append(Y[-1])
    X.append(oneList)
    Y.append(pre)


def getLinePreResult(w,X,Y,lastT,beginT,endT):
    #init
    copyX=copy.deepcopy(X)
    copyY=copy.deepcopy(Y)
    allP=[]
    p=[]
    #deal date
    begin=time.strptime(beginT,'%Y-%m-%d')
    end=time.strptime(endT,'%Y-%m-%d')
    last=time.strptime(lastT,'%Y-%m-%d')
    beginDate=datetime.datetime(begin[0],begin[1],begin[2])
    endDate=datetime.datetime(end[0],end[1],end[2])
    lastDate=datetime.datetime(last[0],last[1],last[2])
    #deal time len
    T1=int(str(beginDate-lastDate).split()[0])
    #get all preset
    while lastDate<endDate:
        oneList=getNewTrainSet(copyX,copyY)
        onePre=getLinePre(w,oneList)
        if onePre<0:
            onePre=0
        allP.append(onePre)
        createNewData(copyX,copyY,onePre)
        lastDate=lastDate+datetime.timedelta(days=1)
    #get preset
    L=len(allP)
    for i in range(T1,L):
        p.append(allP[i])
    return p
