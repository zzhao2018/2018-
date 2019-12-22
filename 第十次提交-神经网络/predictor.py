from getData import *
from nnPre import *
from bag import *
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
    #predict
    pre={}
    for ele in inputL:
        X,Y=getTrainSet(data,ele,dateList)
        lastTime,lastNum=getLTN(data[ele],dateList)
        preResult=getKnnPredictSet(lastTime,lastNum,inputSet[-2][0],inputSet[-1][0],X,Y)
        pre[ele]=preResult
    #get predictSet
    sumPre=sum(pre.values())
    #deal result
    preResult,cpuW,memW,Ccpu,Cmem,V,dataName=dealResult(inputSet,pre,inputL,VmList)
    #bag problem
      #cpuW,memW,Ccpu,Cmem,V,dataName
    bagResult=[]
    #tanxin
    cpuW=cpuW[::-1]
    memW=memW[::-1]
    V=V[::-1]
    dataName=dataName[::-1]
    bagResult,sumPack=bag(Ccpu,Cmem,copy.deepcopy(cpuW),copy.deepcopy(memW),copy.deepcopy(dataName))
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

#get inputL
def getInputL(inputSet):
    inputL=[]
    L=len(inputSet)
    for i in range(2,L-3):
        inputL.append(inputSet[i][0])
    return inputL

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


