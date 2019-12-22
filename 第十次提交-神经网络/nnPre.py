import time
import datetime
import copy
from nn import *

#get test set
def getKnnPredictSet(lastDate,lastNum,beginT,endT,X,Y):
    #analyze time
    last=time.strptime(lastDate,'%Y-%m-%d')
    begin=time.strptime(beginT,'%Y-%m-%d')
    end=time.strptime(endT,'%Y-%m-%d')
    lastD=datetime.datetime(last[0],last[1],last[2])
    beginDate=datetime.datetime(begin[0],begin[1],begin[2])
    endDate=datetime.datetime(end[0],end[1],end[2])
    #count data
    Sum=0
    #copy the data
    copyX=copy.deepcopy(X)
    copyY=copy.deepcopy(Y)
    #run the nn
    V,W,b1,b2=nn(copyX,copyY,4,15000,0.05)
    while beginDate<=endDate:
        #get test data
        lastT=int(str(beginDate-lastD).split()[0])
        oneList=[beginDate.weekday(),lastT,lastNum]
        #predict
        O,onePre=predict(oneList,V,W,b1,b2)
        if onePre<0:
            onePre=0
        Sum+=onePre
        if onePre>=1:
            lastD=beginDate
            lastNum=onePre
        #move time
        beginDate=beginDate+datetime.timedelta(days=1)
    print int(Sum)
    print '*'*25
    return int(Sum)
