import time
import datetime
def pinghua(data,alpha,dateList):
    sL=[]
    sL1=[]
    sD=[]
    s1=0
    k=0
    isFirst=True
    #init
    for e1 in dateList:
       s1+=data[e1]
       k+=1
       if k>=3:
           break
    sL.append(float(s1)/3.0)
    sL1.append(float(s1)/3.0)
    loc=0
    lastData=[]
    #count
    for e in dateList:
        sD.append(e)
        if isFirst:
            isFirst=False
        else:
            lastData=data[e]
            sL.append(lastData*alpha+(1-alpha)*sL[loc])
            sL1.append(alpha*sL[loc+1]+(1-alpha)*sL1[loc])
            loc+=1
           # lastData=data[e]
    return sL1,sL,sD

def predict(s0,s1,sD,beginD,endD,alpha):
    #dealtime
    lastT=time.strptime(sD,'%Y-%m-%d')
    beginT=time.strptime(beginD,'%Y-%m-%d')
    endT=time.strptime(endD,'%Y-%m-%d')
    dateL=datetime.datetime(lastT[0],lastT[1],lastT[2])
    dateB=datetime.datetime(beginT[0],beginT[1],beginT[2])
    dateE=datetime.datetime(endT[0],endT[1],endT[2])
    #predict
    p=[]
    A=2*s0-s1
    B=(alpha/(1-alpha))*(s0-s1)
    while dateB<=dateE:
        T=int(str(dateB-dateL).split()[0])
        xt=A+B*T
        if xt<0:
            xt=0
        p.append(xt)
        dateB=dateB+datetime.timedelta(days=1)
    return p



#def getParameter(data):
#    VList=[0.13,0.1,0.01,0.01,0.044,0.01,0.01,0.04,0.29,0.01,0.07,0.01,\
#           0.01,0.01,0.01]
#    loc=int(data.strip('flavor'))
#    return VList[loc-1]

#def getWeight(L,w):
#    weight=[]
#    W=w
#    for i in range(L):
#        weight.append(W)
#        W=W**2
#    weight=weight[::-1]
#    return weight


#auto get parameter
#def getParameter(data,inputL,dateList):
#    parameter=[]
#    Len=len(dateList)
#    w=getWeight(Len,0.99)
#    for ele in inputL:
#        minErr=100
#        minParameter=0
#        i=0
#        while i<1:
#            i+=0.001
#            s1,s0,sD=pinghua(data[ele],i,dateList)
#            err=0
#            j=0
            #cal Err
#            for e in dateList:
#                err+=w[j]*(s1[j]-data[ele][e])**2
#                j+=1
#            err=float(err)/float(Len)
 #           print err
 ##           print i
  #          print minErr
  #3          print minParameter
  #          print '*'*25
            #get less Err
#            if err<minErr:
#                minErr=err
#                minParameter=i
#        parameter.append(minParameter)
#    print parameter
#    return parameter

