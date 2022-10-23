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
    
    OTHER REQUIRED FUNCTIONS: constr_polyfit.m, polyfit.m, polyval.m
    """
    print()
    print("args")
    print(vin,K,P,W)
    vin = vin[:,np.newaxis]
    W = W[:,np.newaxis]
    # if len(argv) < 2:
    #     raise Exception('[Ns,p,y,E]=dp_weighted_optpolysegsfit(vin,K,P,W) --- provide the number of line segments (K) and polynomial order (P)') 

    # if len(sys.argv) < 3:
    #     raise Exception('[Ns,p,y,E]=dp_weighted_optpolysegsfit(vin,K,P,W) --- provide the polynomial order (P)') 

    # if len(sys.argv) < 4:
    #     raise Exception('[Ns,p,y,E]=dp_weighted_optpolysegsfit(vin,K,P,W) --- provide the weight vector (W)') 
    print(len(vin))
    if vin.shape[0] > vin.shape[1]:
        vin = np.reshape(vin, (vin.shape[1],vin.shape[0]))
    if W.shape[0] > W.shape[1]:
        W = np.reshape(W, (W.shape[1],W.shape[0]))

    Nin=max(vin.shape[1],vin.shape[0])
    print("nin",Nin)
    if Nin>10:
        ND=round(Nin/10) 
    else:
        ND= Nin 
    
    np.nan_to_num(W,copy=False,nan=0.0)
    p = {}


    #####
    # TODOOOO
    ######
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
        print(W.shape)
        #INITIALIZATION
        for i in range(P+1,Nin):  #i=2:Nin:
            tmp = np.reshape(vin.flatten(order='F')[0:i],(1,i))
            aa = np.arange(1,i+1)
            aa = np.reshape(aa,(1,len(aa)))
            tempW = np.reshape(W.flatten(order='F')[0:i],(1,i))
            p1, yy=constr_weighted_polyfit(aa/ND,tmp,tempW,P,np.array([]))
            p1=p1
            print(D[i][0].shape)
            print(i, W[0][0:i].shape)
            print(tmp.shape,yy.shape)
            D[i][0]=np.sum(np.multiply(W[0][0:i],np.power((tmp-yy),2)))
            v = yy[-1]
            vall[i][0] = v

        # bp = [[] for i in range(Nin)]
        bp=np.ones(shape=(Nin,K))
        #BACKPOINTER MATRIX
        print("Nin",Nin)
        #ITERATION
        for k in range(1,K):
            print('k',k)
            for l in range(k,Nin):  #l=k:Nin  
                print('l',l)
                tmp=np.array([])
                tmpv=np.array([])

                for i in range(l-P):
                    p1, yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l+1],W[i:l+1],P,vall[i][k-1]) 
                    cost=np.sum(np.multiply(W[i+1:l+1],np.power(vin[i+1:l+1]-yy[1:],2)))
                    v=yy[-1]
                    tmp=np.vstack((tmp,D[i][k-1]+cost))
                    tmpv=np.vstack((tmpv,v))

                val=np.min(tmp)
                ind = np.argmin(tmp) 
                D[l][k]=val 
                bp[l][k]=ind 
                vall[l][k]=tmpv[ind] 

        print('bp',bp)
        #TERMINATION AND BACKTRACKING
        Ns=np.array([])
        tmp=Nin-1
        print(Nin)
        at = np.arange(K-1,0,-1)
        for i in at:
            print(i)
            print(bp[tmp])
            Ns = np.vstack((bp[tmp][i],Ns))
            tmp=bp[tmp][i] 

        Ns = np.vstack((Ns,Nin))
        
        #RECONSTRUCTION
        cnt=1 
        y=[] 
        for i in range(len(Ns)-1):
            if i==1:
                p1, yy=constr_weighted_polyfit(np.arange(Ns[i],Ns[i+1])/ND,vin[Ns[i]:Ns[i+1]],W[Ns[i]:Ns[i+1]],P,np.array([]))
                y= yy 
                v = yy[-1]

            else:
                p1, yy=constr_weighted_polyfit(np.arange(Ns[i],Ns[i+1])/ND,vin[Ns[i]:Ns[i+1]],W[Ns(i):Ns(i+1)],P,v) 
                y = np.vstack((y,yy[1:]))
                v = yy[-1]

            p[cnt]=p1 
            cnt=cnt+1 
        E=np.mean(np.multiply(W, np.power(vin-y),2)) 

        
    return Ns,p,y,E

# dp_weighted_optpolysegsfit()