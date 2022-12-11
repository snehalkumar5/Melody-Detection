import sys
import numpy as np
import math
from constr_weighted_polyfit import constr_weighted_polyfit

def dp_weighted_optpolysegsfit(vin,K,P,W):
    """
    [Ns,p,y,E]=dp_optpolysegsfit(vin,K,P)
    
    GIVEN A ONE-DIMENSIONAL DATA VECTOR 'vin', 'K' (scaler), AND 'P' (scaler),
    THIS PROGRAM FINDS K PIECEWISE OPTIMUM Pth ORDER POLYNOMIAL SEGMENTS FIT
    WHICH MINIMIZES THE MSE. IT RETURNS K-1 OPTIMUM BREAK POINTS 'Ns', AND
    POLYNOMIAL PARAMETERS 'p' OF THE K LINE SEGMENTS AND THE BEST FIT
    PIECEWISE POLYNOMIAL SEGMENTS 'y' AND ALSO THE TOTAL MSE 'E' 
    
    """
    vin = vin[:,np.newaxis]
    W = W[:,np.newaxis]
   
    if vin.shape[0] > vin.shape[1]:
        vin = np.reshape(vin, (vin.shape[1],vin.shape[0]))
    if W.shape[0] > W.shape[1]:
        W = np.reshape(W, (W.shape[1],W.shape[0]))

    Nin=max(vin.shape[1],vin.shape[0])
    if Nin>10:
        ND=round((Nin+1)/10) 
    else:
        ND= Nin
    
    np.nan_to_num(W,copy=False,nan=0.0)
    p = {}

    if K==1: # ONE LINE SEGMENT IS TRIVIAL
        Ns = np.array([1,Nin])
        aa = np.arange(1,Nin+1)
        aa = np.reshape(aa,(1,len(aa)))
        p1, yy = constr_weighted_polyfit(aa,vin,W,P,np.array([]))
        p[0]=p1 
        y = yy 
        E=np.mean(np.multiply(W,np.power((vin-y),2))) 

    else:
        D=999999999999*np.ones(shape=(Nin,K))
         #COST MATRIX (999999999999 used for some arbitrarily large number):
        vall=999999999999*np.ones(shape=(Nin,K)) 
         #CONTINUITY CONSTRAINTS VALUE MATRIX
        #INITIALIZATION
        for i in range(P,Nin):  #i=1:Nin:
            tmp = np.reshape(vin.flatten(order='F')[0:i+1],(1,i+1))
            aa = np.arange(1,i+2)
            aa = np.reshape(aa,(1,len(aa)))
            tempW = np.reshape(W.flatten(order='F')[0:i+1],(1,i+1))
            p1, yy=constr_weighted_polyfit(aa/ND,tmp,tempW,P,np.array([]))
            D[i][0]=np.sum(np.multiply(W[0][0:i+1],np.power((tmp-yy),2)))
            v = yy[0][-1]
            vall[i][0] = v

        bp=np.zeros(shape=(Nin,K))
        #BACKPOINTER MATRIX
        #ITERATION
        for k in range(1,K):
            for l in range(P+1+(k-1)*P,Nin):  #l=k*P+1:Nin  
                tmp=np.array([])
                tmpv=np.array([])

                for i in range(0,l-P+1): 
                    tmpVin = np.reshape(vin.flatten(order='F')[i:l+1],(1,l+1-i))
                    tempW = np.reshape(W.flatten(order='F')[i:l+1],(1,l+1-i))
                    p1, yy=constr_weighted_polyfit(np.arange(i+1,l+2).reshape(l+1-i,1)/ND,tmpVin,tempW,P,vall[i][k-1]) 
                    cost=np.sum(np.multiply(W[0][i+1:l+1],np.power(vin[0][i+1:l+1]-yy[0][1:],2)))
                    v=yy[0][-1]
                    if tmp.size == 0:
                        tmp = np.array([D[i][k-1]+cost])
                    else:
                        tmp=np.vstack((tmp,D[i][k-1]+cost))
                    if tmpv.size == 0:
                        tmpv = np.array([v])
                    else:
                        tmpv=np.vstack((tmpv,v))

                val=np.amin(tmp)
                ind = np.argmin(tmp) 
                D[l][k]=val     
                bp[l][k]=ind 
                vall[l][k]=tmpv[ind] 

        #TERMINATION AND BACKTRACKING
        Ns=np.array([])
        tmp=Nin-1
        at = np.arange(K-1,-1,-1)
        for i in at:
            if Ns.size==0:
                Ns = np.array([bp[tmp][i]])
            else:
                Ns = np.vstack((bp[tmp][i],Ns))
            tmp=int(bp[tmp][i])
        if Ns.size==0:
            Ns = np.array([Nin])
        else:
            Ns = np.vstack((Ns,Nin-1))
    
        #RECONSTRUCTION
        cnt=1 
        y=[] 
        for i in range(len(Ns)-1):
            st = int(Ns[i])
            ed = int(Ns[i+1])
            tmpVin = np.reshape(vin.flatten(order='F')[st:ed+1],(1,ed+1-st))
            tempW = np.reshape(W.flatten(order='F')[st:ed+1],(1,ed+1-st))
            if i==0:
                p1, yy=constr_weighted_polyfit(np.arange(st+1,ed+2).reshape(ed+1-st,1)/ND,tmpVin,tempW,P,np.array([]))
                y= yy 
                v = yy[0][-1]

            else:
                p1, yy=constr_weighted_polyfit(np.arange(st+1,ed+2).reshape(ed+1-st,1)/ND,tmpVin,tempW,P,v) 
                tempYY = np.reshape(yy.flatten(order='F')[1:],(1,yy.size-1))
                y = np.hstack((y,tempYY))
                v = yy[0][-1]

            p[cnt]=p1 
            cnt=cnt+1 
        E = np.mean(np.multiply(W, np.power((vin-y),2))) 
    return Ns,p,y,E