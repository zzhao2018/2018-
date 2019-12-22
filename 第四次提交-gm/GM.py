# -*- coding: utf-8 -*-
"""


This is a temporary script file.
"""

import math
from mat import *

def gm(history_data,m):


    n = len(history_data)
    X0 = history_data
    #accumulation
    history_data_agg = [sum(history_data[:i+1]) for i in range(n)]
    
    X1 = history_data_agg
    #data B and vector Y
    B =[]
    Y =[]
    for i in range(n-1):
        
        B.append([-0.5*(X1[i] + X1[i+1]),1])

        Y.append([X0[i+1]])

    #calculate  GM(1,1) a,u
    #A = np.zeros([2,1])

    A = mulMat(mulMat(inv(mulMat(t(B),B)),t(B)),Y)
    a = A[0][0]
    u = A[1][0]
    #build GM
    XX0 = [[0]]*(n)
    XX0[0] = X0[0]
    for i in range(1,n):
        XX0[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i));
    #test 
    e = 0      #bias average
    for i in range(0,n):
        e += (X0[i] - XX0[i])
    e /= n
    #history average data
    aver = 0;     
    for i in range(0,n):
        aver += X0[i]
    aver /= n
    #average data variance
    s12 = 0;     
    for i in range(0,n):
        s12 =s12 + (X0[i]-aver)**2
        
    s12 =float(s12) / n
    #bias variance
    s22 = 0
    for i in range(0,n):
        s22 =s22 + ((X0[i] - XX0[i]) - e)**2;
    s22 =float(s22) / n
    #data variance / bias variance
    C = s22 / s12
    #Small error probability
    cout = 0
    for i in range(0,n):
        if abs((X0[i] - XX0[i]) - e) < 0.6754*math.sqrt(s12):
            cout = cout+1
        else:
            cout = cout
    P = cout / n
    '''if (C < 0.35 and P > 0.95):
        #precision level
        m = 10   #prediction times
        print('future data:')
        f = [[0]]*(m)
        for i in range(0,m):
            f[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i+n))
            print(f[i])
    else:
        print('GM is not good')'''
    
    
    f = [[0]]*(m)
    for i in range(0,m):
        f[i] = (X0[0] - u/a)*(1-math.exp(a))*math.exp(-a*(i+n))
    
    return sum(f)
if __name__== "__main__":
    data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
                     0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    m = 10
    gm(data,m)
