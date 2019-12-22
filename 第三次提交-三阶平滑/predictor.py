from pinghua import *
from bag import *
import copy
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
    data,dateList=getData(ecs_lines,inputL)
    #get predictSet
    pre=getPredictSet(data,inputL,inputSet[-2][0],inputSet[-1][0],dateList)
    sumPre=sum(pre.values())
    #deal result
    preResult,cpuW,memW,Ccpu,Cmem,V,dataName=dealResult(inputSet,pre,inputL,VmList)
    #bag problem
    bagResult=[]
    thing=[]
    init_thing(thing,V)
    sumPack=0
    while V!=[]:
        res=bag(Ccpu,Cmem,cpuW,memW,V)
        package,newcpuW,newmemW,newV,newthing,newdataName=show(Ccpu,Cmem,cpuW,memW,V,res,thing,dataName)
        bagResult.append(package)
        cpuW,memW,V,thing,dataName=newcpuW,newmemW,newV,newthing,newdataName
        sumPack+=1
#    print sumPre
#    print preResult
#    print sumPack
#    print bagResult
    result=getFinalResult(sumPre,preResult,sumPack,bagResult)
    return result

def getFinalResult(sumPre,preResult,sumPack,bagResult):
    result=[]
    result.append(sumPre)
    for line in preResult:
        result.append(str(line[0])+' '+str(line[1]))
    result.append('')
    result.append(sumPack)
    i=1
    for line in bagResult:
        s=str(i)
        for key,value in line.items():
            s=s+' '+str(key)+' '+str(value)
        i+=1
        result.append(s)
    return result

#deal result
def dealResult(inputSet,pre,inputL,List):
    Ccpu=int(inputSet[0][0])
    Cmem=int(inputSet[0][1])
    preSet=[]
    V=[]
    for ele in inputL:
        preSet.append([ele,pre[ele]])
    cpuW,memW,dataName=getBagSet(preSet,List)
    select=inputSet[-3][0]
    if select=='CPU':
        V=copy.deepcopy(cpuW)
    elif select=='MEM':
        V=memW
    else:
        print 'Error'
    return preSet,cpuW,memW,Ccpu,Cmem,V,dataName

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

#get inputL
def getInputL(inputSet):
    inputL=[]
    L=len(inputSet)
    for i in range(2,L-3):
        inputL.append(inputSet[i][0])
    return inputL

#get predictSet
def getPredictSet(data,inputL,beginD,endD,dateList):
    pre={}
    for ele in inputL:
        vL=getParameter(ele)
        s2,s1,s0,sD=pinghua(data[ele],vL,dateList)
        L=len(s1)
        p=predict(s0[L-1],s1[L-1],s2[L-1],sD[L-1],beginD,endD,vL)
        Sum=sum(p)
        iSum=int(Sum)
        if Sum-iSum>0.5:
            iSum+=1
        pre[ele]=iSum
        print iSum
        print '*'*25
    return pre
        

