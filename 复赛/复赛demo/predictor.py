from pinghua import *
from bag import *
import copy
from getKnnData import *
from knnPre import *
import dealdate
def predict_vm(ecs_lines, input_lines):
    # Do your work from here#
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    #get inputSet
    inputSet=getInput(input_lines)
    inputL=getInputL(inputSet)
    VmList=getVmsList(inputSet)
    #get trainSet
      #get pinghua data
    middata,middateList=getData(ecs_lines,inputL)
    data,dateList=dealdate.getDealData(middata,middateList,inputL)
    #get predictSet
    pre=getPredictSet(data,inputL,inputSet[-2],inputSet[-1],dateList)
    sumPre=sum(pre.values())
    #deal result
    preResult,itemWeight,itemName,bagName,bagWeight=dealResult(inputSet,pre,inputL,VmList)
#    bag problem
      #cpuW,memW,Ccpu,Cmem,V,dataName
    bagResult=[]
    #tanxin
    itemWeight=itemWeight[::-1]
    itemName=itemName[::-1]
    bagResult,bagLoc=bag(itemName,itemWeight,bagName,bagWeight)
    result=getFinalResult(sumPre,preResult,bagLoc,bagResult,bagName)
    return result

def getFinalResult(sumPre,preResult,bagLoc,bagResult,bagName):
    #deal predict result
    result=[]
    result.append(sumPre)
    for line in preResult:
        result.append(str(line[0])+' '+str(line[1]))
    #deal bag result
    for ele in bagName:
        if bagLoc[ele]==-1:
            continue
        else:
            result.append('')
            s=ele+' '+str(bagLoc[ele]+1)
            result.append(s)
            L1=len(bagResult[ele])
            for i in range(L1):
                s1=ele+'-'+str(i+1)
                for key,value in bagResult[ele][i].items():
                    s1=s1+' '+key+' '+str(value)
                result.append(s1)
    return result
 #   i=1
 #   for line in bagResult:
 #       s=str(int(i))
 #       for key,value in line.items():
 #           s=s+' '+str(key)+' '+str(int(value))
 #       i+=1
 #       result.append(s)
    return result

#deal result
def dealResult(inputSet,pre,inputL,List):
    L=int(inputSet[0][0])+1
    #init parameter
    bagName=[]
    bagWeight=[]
    preSet=[]
    #get pre list
    for ele in inputL:
        preSet.append([ele,pre[ele]])
    #get weight
    itemWeight,itemName=getBagSet(preSet,List)
    #get bag parameter
    for i in range(1,L):
        bagName.append(inputSet[i][0])
        bagWeight.append([int(inputSet[i][1]),int(inputSet[i][2])])
    return preSet,itemWeight,itemName,bagName,bagWeight


#ok
#get inputSet
def getInput(inputLine):
    data=[]
    for line in inputLine:
        line=line.strip()
        if line=='':
            continue
        lineData=line.split()
        data.append(lineData)
    return data

#ok
#get trainSet
def getData(fileLine,inputL):
    L=len(inputL)
    dayNum={}
    dateList=[]
    #init 
    for i in range(L):
        dayNum[inputL[i]]={}
    for line in fileLine:
        line=line.strip()
        data=line.split()
        Type=data[1]
        date=data[2].split()[0]
        #init every day
        for i in range(L):
            if date not in dayNum[inputL[i]]:
                dayNum[inputL[i]][date]=0
        if Type in dayNum:
            dayNum[Type][date]+=1
        if date not in dateList:
            dateList.append(date)
    return dayNum,dateList

#ok
#get inputL
def getInputL(inputSet):
    inputL=[]
    L=len(inputSet)
    beginLoc=int(inputSet[0][0])+2
    for i in range(beginLoc,L-2):
        inputL.append(inputSet[i][0])
    return inputL

#ok
#get predictSet
def getPredictSet(data,inputL,beginD,endD,dateList):
    pre={}
    w1=0.5
    w2=0.6
    for ele in inputL:
        #pinghua
        s2,s1,s0,sD=pinghua(data[ele],0.3,dateList)
        print s2
        L=len(s1)
        p=predict(s0[L-1],s1[L-1],s2[L-1],sD[L-1],beginD,endD,0.3)
        print p
        #predict
        Sum=sum(p)
        iSum=int(Sum)
        if Sum-iSum>0.5:
            iSum+=1
        pre[ele]=iSum
    return pre
        

