import copy

#split the data
def splitDataList(data,dateList,Len):
    L=len(dateList)
    LL=L-Len
    Set=[]
    result=[]
    for i in range(LL,L):
        Set.append(dateList[i])
    for ele in Set:
        result.append(data[ele])
    return float(sum(result))/float(Len)
