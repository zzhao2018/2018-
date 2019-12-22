def bag(c1,c2,w1,w2,dataName):
    #the bag set
    resultSet=[{}]
    #loc:the loc of bag
    loc=0
    L=len(w1)
    #init bag size
    Cbag1=c1
    Cbag2=c2
    #begin
    while L>0:
        #flag use to label if has append
        flag=0
        i=0
        while i<L:
            if Cbag1>=w1[i] and Cbag2>=w2[i]:
                #put item to bag
                Name=dataName[i]
                if Name in resultSet[loc]:
                    resultSet[loc][Name]+=1
                else:
                    resultSet[loc][Name]=1
                #updata bag
                Cbag1-=w1[i]
                Cbag2-=w2[i]
                #updata item
                del w1[i]
                del w2[i]
                del dataName[i]
                #label flag
                flag=1
                #updata len
                L-=1
            else:
                i+=1
        #bag space not enought
        if flag==0:
            resultSet.append({})
            loc+=1
            Cbag1=c1
            Cbag2=c2
    print resultSet
    print loc+1
    return resultSet,loc+1



def init_thing(X,V):
    L=len(V)
    for i in range(L):
        X.append(False)

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
