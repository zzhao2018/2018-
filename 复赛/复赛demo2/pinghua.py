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
            #update s0 s1
            lastData=data[e]
            sL.append(lastData*alpha+(1-alpha)*sL[loc])
            sL1.append(alpha*sL[loc+1]+(1-alpha)*sL1[loc])
            loc+=1
    return sL1,sL,sD

def predict(s0,s1,sD,beginD,endD,alpha):
    #make time to date
    #dealtime
    lastT=time.strptime(sD,'%Y-%m-%d')
    beginT=time.strptime(beginD[0],'%Y-%m-%d')
    endT=time.strptime(endD[0],'%Y-%m-%d')
    dateL=datetime.datetime(lastT[0],lastT[1],lastT[2])
    dateB=datetime.datetime(beginT[0],beginT[1],beginT[2])
    dateE=datetime.datetime(endT[0],endT[1],endT[2])
    if int(beginD[1].split(':')[0])>12:
        dateB=dateB+datetime.timedelta(days=1)
    if int(endD[1].split(':')[0])>12:
        dateE=dateE+datetime.timedelta(days=1)
    #predict
    p=[]
    A=2*s0-s1
    B=(alpha/(1-alpha))*(s0-s1)
    while dateB<dateE:
        T=int(str(dateB-dateL).split()[0])
        xt=A+B*T
        if xt<0:
            xt=0
        p.append(xt)
        dateB=dateB+datetime.timedelta(days=1)
    return p

    
