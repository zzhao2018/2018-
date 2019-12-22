import copy
import bag
import random
import math
import copy
#SA
  #the more,the better
def SA(father,beginT,endT,num,delta,pm,bagName,bagWeight,VmList,allCpu,allMem):
    #init value
    t=beginT
    bestPack=[]
    bestLoc=[]
    bestCost=-1
    #get father
    data=init_thing(father,num)  
    #begin
    while t>endT:
        for i in range(num):            
            #create new data
            newData=createNewSAData(data[i],pm) 
            #evalue
            value,bestPack,bestLoc,bestCost=evalue(data[i],bagName,bagWeight,VmList,allCpu,allMem,bestPack,bestLoc,bestCost)
            newValue,bestPack,bestLoc,bestCost=evalue(newData,bagName,bagWeight,VmList,allCpu,allMem,bestPack,bestLoc,bestCost)
            #exchange
            if (newValue-value)>0:
                data[i]=newData
            else:
                p=math.exp((newValue-value)/float(t))
                if random.random()<p:
                    data[i]=newData
        t=t*delta
    print bestCost
    return bestPack,bestLoc

#create new data
def createNewSAData(oneData,pm):
    L=len(oneData)
    changeList=[]
    newList=copy.deepcopy(oneData)
    #get the change list
    for i in range(L):
        if random.random()<pm:
            changeList.append(i)
    changeL=len(changeList)
    if changeL%2!=0:
        del changeList[changeL-1]
        changeL-=1
    #create new list
    begin=0
    while begin<changeL:
        loc1=changeList[begin]
        loc2=changeList[begin+1]
        mid=newList[loc1]
        newList[loc1]=newList[loc2]
        newList[loc2]=mid
        begin+=2
    return newList


#init the father
def init_thing(father,num):
    child=[copy.deepcopy(father)]
    N=1
    while N<num:
        mid=copy.deepcopy(father)
        random.shuffle(mid)
        child.append(mid)
        N+=1
    return child


#evalue the data
def evalue(itemName,bagName,bagWeight,VmList,allCpu,allMem,bestPack,bestLoc,bestCost):
    #init evalue parameter
    allBagCpu=0
    allBagMem=0
    copyBestPack=copy.deepcopy(bestPack)
    copyBestLoc=copy.deepcopy(bestLoc)
    #init bag
    resultSet={}
    resultLoc={}
    bagTypeLen=len(bagName)
    for i in range(bagTypeLen):
        resultSet[bagName[i]]=[]
        resultLoc[bagName[i]]=-1
    #copy the parameter
    copyItemName=copy.deepcopy(itemName)
    copyBagName=copy.deepcopy(bagName)
    #open the first bag
    allPara=nameGetAllPara(itemName,VmList) 
    bagType,bagPara,bCpu,bMem=bag.openBag(bagWeight,bagName,allPara)
    resultSet[bagType].append({})
    resultLoc[bagType]=0
    bagLoc=0
    end=0
    itemL=len(copyItemName)
    #init evalue
    allBagCpu+=bCpu
    allBagMem+=bMem
    while itemL>0 and end==0:
        flag=0
        i=0
        while i<itemL:
            Name=copyItemName[i]
            itemCpu,itemMem=bag.changeToData(Name,VmList)
            if bCpu>=itemCpu and bMem>=itemMem:
                #put item in bag
                if Name in resultSet[bagType][bagLoc]:
                    resultSet[bagType][bagLoc][Name]+=1
                else:
                    resultSet[bagType][bagLoc][Name]=1
                #update bag weight
                bCpu-=itemCpu
                bMem-=itemMem
                #update item
                del copyItemName[i]
                #update flag
                flag=1
                #update itemL
                itemL-=1
            else:
                i+=1
        #open new bag
        if flag==0:
            bagType,bCpu,bMem=nameCanPutOne(bagWeight,bagName,copyItemName,VmList)
            #the item can put in one bag
            if bagType!='no':
                resultSet[bagType].append({})
                resultLoc[bagType]+=1
                bagLoc=resultLoc[bagType]
                namePutAllInBag(resultSet,bagType,bagLoc,copyItemName)
                end=1
                #init evalue
                allBagCpu+=bCpu
                allBagMem+=bMem
                break
            #the item can not put in one bag
            allPara=nameGetAllPara(copyItemName,VmList)      #
            bagType,bagPara,bCpu,bMem=bag.openBag(bagWeight,bagName,allPara)
            resultSet[bagType].append({})
            resultLoc[bagType]+=1
            bagLoc=resultLoc[bagType]
            #init evalue
            allBagCpu+=bCpu
            allBagMem+=bMem
    #evalue
    useValue=((float(allCpu)/float(allBagCpu)+float(allMem)/float(allBagMem))*0.5)*100
    #get the best result
    if useValue>bestCost:
        return useValue,resultSet,resultLoc,useValue
    return useValue,bestPack,bestLoc,bestCost

#put all the item into bag
def namePutAllInBag(resultSet,bagType,bagLoc,copyItemName):
    #get len
    Len=len(copyItemName)
    bag=resultSet[bagType][bagLoc]
    for i in range(Len):
        if copyItemName[i] not in bag:
            bag[copyItemName[i]]=1
        else:
            bag[copyItemName[i]]+=1

    
def nameGetAllPara(itemName,VmList):
    cpu=0
    mem=0
    L=len(itemName)
    for i in range(L):
        itemCpu,itemMem=bag.changeToData(itemName[i],VmList)
        cpu+=itemCpu
        mem+=itemMem
    return float(cpu)/float(mem)


def nameCanPutOne(bagWeight,bagName,copyItemName,VmList):
    #get len
    bagL=len(bagName)
    itemL=len(copyItemName)
    #cal all item weight
    allItemCpu=0
    allItemMem=0
    #init para
    bagType='no'
    for i in range(itemL):
        itemCpu,itemMem=bag.changeToData(copyItemName[i],VmList)
        allItemCpu+=itemCpu
        allItemMem+=itemMem
    #test
    for i in range(bagL):
        if bagWeight[i][0]>=allItemCpu and bagWeight[i][1]>=allItemMem:
            return bagName[i],bagWeight[i][0],bagWeight[i][1]
    return bagType,0,0
