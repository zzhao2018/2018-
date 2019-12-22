import copy
from pinghua import *
from knnPre import *
from getKnnData import *

def autoDealParameter(data,dataKnn,inputL,dateList,dateLen):
    upBoard=1
    w1=0.5
    w2=0.5
    bestParameter=[]
    #split the data
    trainDateList,preDateList,beginD,endD=splitDataList(dateList,dateLen)
    for ele in inputL:
        #init
        vL=0
        bestValue=100000
        bestPara=-1
        #type:list
        preTrue=getPreDataSet(data[ele],preDateList)
        while vL<upBoard:
            #pinghua
            s2,s1,s0,sD=pinghua(data[ele],vL,trainDateList)
            L=len(s1)
            p=predict(s0[L-1],s1[L-1],s2[L-1],sD[L-1],beginD,endD,vL)
            #Knn
            X,Y=getTrainSet(dataKnn,ele,trainDateList)
            lastTime,lastNum=getLTN(dataKnn[ele],trainDateList)
            knnPre,preList=getKnnPredictSet(lastTime,lastNum,beginD,endD,X,Y)
            #predict
            Sum=add(p,preList,w1,w2)
            #get the best parameter
            bestValue,bestPara=getBestPara(Sum,preTrue,bestValue,bestPara,vL)
            vL+=0.01
        bestParameter.append(bestPara)
    return bestParameter


def getBestPara(pre,true,bestValue,bestPara,vL):
    L=len(true)
    Err=0
    for i in range(L):
        Err+=abs(pre[i]-true[i])
    Err+=(sum(pre)-sum(true))**2
    if Err<bestValue:
        bestValue=Err
        bestPara=vL
 #   print Err
 #   print sum(pre)
 #   print sum(true)
 #   print bestValue
 #   print bestPara
 #   print '*'*25
    return bestValue,bestPara
    

#get the ture predict data set
def getPreDataSet(data,dateList):
    true=[]
    for ele in dateList:
        true.append(data[ele])
    return true

#split the data
def splitDataList(dateList,Len):
    L=len(dateList)
    LL=L-Len
    trainSet=[]
    preSet=[]
    for i in range(LL):
        trainSet.append(dateList[i])
    for i in range(LL,L):
        preSet.append(dateList[i])
    return trainSet,preSet,preSet[0],preSet[-1]

#add w1*a + w2*b
def add(a,b,w1,w2):
    cb=copy.deepcopy(b)
    L1=len(a)
    try:
        L2=len(a[0])
        for i in range(L1):
            for j in range(L2):
                mid=w2*cb[i][j]+w1*a[i][j]
                intmid=int(mid)
                if (mid-intmid)>0.5:
                    intmid+=1
                cb[i][j]=intmid
    except:
        for i in range(L1):
            mid=w2*cb[i]+w1*a[i]
            intmid=int(mid)
            if (mid-intmid)>0.5:
                intmid+=1
            cb[i]=intmid
    return cb
