def bag(c1,c2,w1,w2,v):
    n=len(v)
    res=[[[0 for i in range(c2+1)] for j in range(c1+1)] for k in range(n+1)]
    for i in range(1,n+1):
        for weight1 in range(1,c1+1):
            for weight2 in range(1,c2+1):
                res[i][weight1][weight2]=res[i-1][weight1][weight2]
                if weight1>=w1[i-1] and weight2>=w2[i-1] and \
                   res[i][weight1][weight2]< \
                   (res[i-1][weight1-w1[i-1]][weight2-w2[i-1]]+v[i-1]):
                    res[i][weight1][weight2]=res[i-1][weight1-w1[i-1]][weight2-w2[i-1]]+v[i-1]
    #out put use
   # print res[n][c1][c2]
    return res

def init_thing(X,V):
    L=len(V)
    for i in range(L):
        X.append(False)


def show(c1,c2,w1,w2,V,res,x,dataName):
    n=len(w1)
    weight1=c1
    weight2=c2
    package={}
    #get thing
    for i in range(n,0,-1):
        if res[i-1][weight1][weight2]!=res[i][weight1][weight2]:
            x[i-1]=True
            weight1-=w1[i-1]
            weight2-=w2[i-1]
    #pack the bag
    newW1=[]
    newW2=[]
    newV=[]
    newX=[]
    newDataName=[]
    sumCpu=0
    sumMem=0
    sumValue=0
    k=0
    for i in range(n):
        if x[i]==False:
            newW1.append(w1[i])
            newW2.append(w2[i])
            newV.append(V[i])
            newX.append(x[i])
            newDataName.append(dataName[i])
        else:
            if dataName[i] not in package:
                package[dataName[i]]=1
            else:
                package[dataName[i]]+=1
            k+=1
            sumCpu+=w1[i]
            sumMem+=w2[i]
            sumValue+=V[i]
            ##test
#            print '*'*25
#            print 'dataName:',dataName[i]
#            print 'wcpu:',w1[i]
#            print 'wmem',w2[i]
#            print 'value:',V[i]
#            print 'sum',sumValue
#            print '*'*25
#    print 'SumCpu:',sumCpu
#    print 'SumMem:',sumMem
#    print 'SumValue:',sumValue
#    print 'use:',float(sumValue)/float(56)
#    print '$'*30
#    print '&'*30
#    for key,value in package.items():
#        print 'dataName',key
#        print 'packageNum',value
#    print k
    return package,newW1,newW2,newV,newX,newDataName

def getVmsList(data):
    List={}
    L=len(data)
    for i in range(2,L-3):
        Type=data[i][0]
        List[Type]={}
        List[Type]['cpu']=int(data[i][1])
        List[Type]['mem']=int(data[i][2])
    return List
        


def changeToData(name,List):
    return List[name]['cpu'],(List[name]['mem']/1024)


def getBagSet(data,List):
    cpuW=[]
    memW=[]
    dataName=[]
    for line in data:
        num=line[1]
        if num!=0:
            for i in range(num):
                dataName.append(line[0])
                cpu,mem=changeToData(line[0],List)
                cpuW.append(cpu)
                memW.append(mem)
    return cpuW,memW,dataName
