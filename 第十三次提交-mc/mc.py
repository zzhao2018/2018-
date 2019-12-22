import random 
def cal_mc_matrix(data):
    data.append(0)
    m = len(data)
    back_up = list(set(data))
    back_up.sort()
    m = len(data)
    n = len(back_up)
    probability = []
    for i in range(n):
        temp = {}
        for k in back_up:
            temp[k] = 0
        num = data[:m-1].count(back_up[i])
        for j in range(m-1):
            if data[j]==back_up[i]:
                temp[data[j+1]] = temp[data[j+1]] + 1
        temp2 = []
        for k in back_up:
            temp2.append(temp[k]/float(num))
        probability.append(temp2)
    
    return probability,back_up

def rand_pick(seq , probabilities):  
    x = random.uniform(0 ,1)  
    cumprob = 0.0  
    for item , item_pro in zip(seq , probabilities):  
        cumprob += item_pro  
        if x < cumprob:  
            break  
    return item  

def mc_predict(data,length):
    probability,back_up = cal_mc_matrix(data)
    last = data[-2]
    pre_list = []
    while length>0:
        next_pro = probability[back_up.index(last)]
        item = rand_pick(back_up, next_pro)
        pre_list.append(item)
        last  = item
        length = length - 1
    return pre_list

if __name__=="__main__":
    data = [0,13,999,0, 0, 0,0, 0, 0, 0, 0, 0, 12, \
            2, 0, 1, 0, 3, 0, 0, 0, 0, 1, 1, 1, \
            0, 0, 0, 3, 1, 0, 3, 1, 0, 0, 0, 0, \
            1, 2, 0, 0, 0, 0, 10010,10010]
    mc_predict(data,100)
