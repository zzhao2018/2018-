from random import *
import copy
#cal the bound
def calBound(pre,VmList,Ccpu,Cmem):
    AllCpu=0
    AllMem=0
    for key,value in pre:
        AllCpu+=value*VmList[key]['cpu']
        AllMem+=value*VmList[key]['mem']
    AllMem=AllMem/1024
    bound=max(AllCpu/Ccpu*1.5,AllMem/Cmem*1.5)
    return int(bound)

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
                #change find turn
                w1=w1[::-1]
                w2=w2[::-1]
                dataName=dataName[::-1]
            else:
                i+=1
        #bag space not enought
        if flag==0:
            resultSet.append({})
            loc+=1
            Cbag1=c1
            Cbag2=c2
    return resultSet,loc+1


def init_thing(X,V):
    L=len(V)
    for i in range(L):
        X.append(False)


#yichuan
def yichuan(L,bound,num,c1,c2,cpuW,memW,stepNum,Pc,Pm):
    #init
    i=0
    first=Init_thing(L,bound,num,c1,c2,cpuW,memW)
    value,minBag,result=evaluate(first,bound)
    while i<stepNum:
        #select father
        father=selectFather(first,value,num)
        #cross
        father=cross(copy.deepcopy(father),c1,c2,cpuW,memW,Pc)
        #mutate
        first=mutate(father,c1,c2,cpuW,memW,Pm)
        value,minBag,result=evaluate(first,minBag)
        i+=1
    print minBag
    return result,minBag

#mutate
def mutate(father,c1,c2,cpuW,memW,Pm):
    f=copy.deepcopy(father)
    L1=len(f)
    L2=len(f[0])
    for i in range(L1):
        t=copy.deepcopy(f[i]) 
        for j in range(L2):
            p=random()
            if p<Pm:
                bound=t[j]
                t[j]=randint(1,bound)
                if testFather(t,c1,c2,cpuW,memW)==1:
                    f[i]=t
    return f
    


#cross
def cross(father,c1,c2,cpuW,memW,Pc):
    #get the select object
    selectOne=[]
    L=len(father)
    for i in range(L):
        p=random()
        if p<Pc:
            selectOne.append(i)
    if len(selectOne)%2!=0:
        selectOne.pop()
    #begin cross
    cL=len(selectOne)
    k=0
    while k<cL:
        pos=randint(1,L)
        f1=copy.deepcopy(father[selectOne[k]])
        f2=copy.deepcopy(father[selectOne[k+1]])
        t=f1[0:pos]
        f1[0:pos]=f2[0:pos]
        f2[0:pos]=t
        if testFather(f1,c1,c2,cpuW,memW)==1:
            bound=len(set(father[selectOne[k]]))
            if len(set(f1))<bound:
                resetBagPut(f1)
            father[selectOne[k]]=f1
        if testFather(f2,c1,c2,cpuW,memW)==1:
            bound=len(set(father[selectOne[k+1]]))
            if len(set(f2))<bound:
                resetBagPut(f2)
            father[selectOne[k+1]]=f2
        k+=2
    return father

#select father
def selectFather(first,value,num):
    #init
    father=[]
    L=len(value)
    #get q
    fenmu=float(sum(value))
    q=[]
    for i in range(L):
        value[i]=value[i]/fenmu
        if i==0:
            q.append(value[i])
        else:
            q.append((q[i-1]+value[i]))
    #select father
    for i in range(num):
        p=random()
        k=0
        while p>q[k]:
            k+=1
        father.append(first[k])
    return father
        

#evaluate
def evaluate(data,bound):
    value=[]
    Min=bound
    MinData=[]
    for ele in data:
        S=set(ele)
        Ls=len(S)
        if Ls<bound:
            resetBagPut(ele)
            Min=Ls
            MinData=ele
        value.append(1.0/Ls)
    return value,Min,MinData


#renew the father set
def resetBagPut(father):
    #init
    fatherName=sorted(list(set(father)))
    L=len(fatherName)
    Name={}
    newName=1
    for ele in fatherName:
        Name[ele]=newName
        newName+=1
    #change name
    LItem=len(father)
    for i in range(LItem):
        father[i]=Name[father[i]]
        

#test if the father can be one
def testFather(father,c1,c2,cpuW,memW):
    #init bag
    bagName=set(father)
    bag={}
    for ele in bagName:
        bag[ele]=[c1,c2]
    #test
    L=len(father)
    for i in range(L):
        bag[father[i]][0]-=cpuW[i]
        bag[father[i]][1]-=memW[i]
        if bag[father[i]][0]<0 or bag[father[i]][1]<0:
            return 0
    return 1
    
#get the first father
def Init_thing(L,bound,num,c1,c2,cpuW,memW):
    i=1
    first=[]
    while i<=num:
        oneFather=[]
        #set the father
        for k in range(L):
            oneFather.append(randint(1,bound))
        if testFather(oneFather,c1,c2,cpuW,memW)==1:
            i+=1
            first.append(oneFather)
    return first
    
    

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
