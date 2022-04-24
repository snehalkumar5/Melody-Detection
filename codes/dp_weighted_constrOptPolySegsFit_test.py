import numpy as np
import math
from constr_weighted_polyfit import constr_weighted_polyfit
from createPatterns import createPatterns
import itertools

def dp_weighted_constrOptPolySegsFit_test(vin, W, nSyls):
    if vin.shape[0] > vin.shape[1]:
        vin = np.reshape(vin, (vin.shape[1],vin.shape[0]))

    if W.shape[0]>W.shape[1]:
        W = np.reshape(W, (W.shape[1],W.shape[0]))

    patterns = createPatterns()

    E_all = 10^12 * np.ones((1,len(patterns)))
    Ns_all = {}
    for i in range(len(patterns)):
        Ns_all[i] = []
    p_all= Ns_all 
    y_all= Ns_all
    for iterPattern in range(0,len(patterns)):
        currPattern = patterns[iterPattern]
        if len(currPattern)<=nSyls:
            if currPattern[-1]==5 and (len(currPattern)==1 and nSyls>1):
                E_all[iterPattern] = 999999999999
            else:
                [Ns_all[iterPattern],p_all[iterPattern],y_all[iterPattern],E_all[iterPattern]]= currOptPolysegFit(vin,W,currPattern)

    optPattern = np.argmin(E_all)
    Ns= Ns_all[optPattern]
    p= p_all[optPattern]
    y= y_all[optPattern]
    E= E_all[optPattern]

def currOptPolysegFit(vin,W,currPattern):
    P = 1
    if not W:
        temp_in = vin
        temp_W = W

    minW= min(temp_W)
    maxIn= max(temp_in(temp_W>(0.5*(range(temp_W))+minW)))
    minIn= min(temp_in(temp_W<(0.5*(range(temp_W))+minW)))
    thLowHigh_prev= 0.5*(maxIn-minIn)+minIn
    thLowHigh= thLowHigh_prev
    iterContinue= 1
    while iterContinue:
        highInInds= np.argwhere(temp_in>=thLowHigh_prev)[0]
        lowInInds= np.argwhere(temp_in<thLowHigh_prev)[0]
        maxIn= np.sum(np.multiply(temp_W[highInInds],temp_in[highInInds]))/np.sum(temp_W[highInInds])
        minIn= np.sum(np.multiply(temp_W[lowInInds],temp_in[lowInInds]))/np.sum(temp_W[lowInInds])
        thLowHigh= 0.5*(maxIn-minIn)+minIn
        if abs(thLowHigh_prev-thLowHigh)>0.01:
            thLowHigh_prev = thLowHigh
        else:
            iterContinue = 0

    th_w = 0.5*range(temp_W)+minW
    if not W:
        W=0

    Nin=len(vin)
    if Nin>10:
        ND=round(Nin/10)
    else:
        ND= Nin

    isDiveEnd= 0
    if currPattern[-1]==5:
        isDiveEnd = 1
        currPattern = [currPattern[0:-2],3,4]
    K= len(currPattern)

    if K==1: # ONE LINE SEGMENT IS TRIVIAL
        Ns=np.array([1, Nin])
        if currPattern == 3:
            p1,yy=constr_weighted_polyfit(np.arange(0,Nin),vin,W,P,np.array([]))
            if p1[1]>0:
                p1,yy= constr_weighted_polyfit(np.arange(0,Nin),vin,W,0,np.array([]))
            else:
                rangeCovered= abs(yy[-1]-yy[0])
                if rangeCovered < (thLowHigh-minIn):
                    p1,yy= constr_weighted_polyfit(np.arange(0,Nin),vin,W,0,np.array([]))
        if currPattern == 4:
            p1,yy=constr_weighted_polyfit(np.arange(0,Nin),vin,W,P,np.array([]))
            if p1[1]<0:
                p1,yy= constr_weighted_polyfit(np.arange(0,Nin),vin,W,0,np.array([]))
            else:
                rangeCovered= abs(yy[-1]-yy[0])
                if rangeCovered < (thLowHigh-minIn):
                    p1,yy= constr_weighted_polyfit(np.arange(0,Nin),vin,W,0,np.array([]))
        p = {}
        p[1]=p1
        y= yy
        E=np.sum(np.multiply((W),np.power((vin-y),2)))/len(y)
        
    else:
        D=999999999999*np.ones(shape=(Nin,K)); #COST MATRIX (999999999999 used for some arbitrarily large number)
        vall=999999999999*np.ones(shape=(Nin,K)); #CONTINUITY CONSTRAINTS VALUE MATRIX
        bp = [[] for _ in Nin]
        #INITIALIZATION
        bp[0]= np.ones(Nin,1) #BACKPOINTER MATRIX
        for i in range(P+1,Nin):
            tmp1=[]
            tmpv=[]
            for l in 1:
                if np.max(W[l:i])>th_w:
                    tmp=vin[l:i]
                    if currPattern[0] == 1:
                        p1,yy=constr_weighted_polyfit(np.arange(l,i)/ND,tmp,W[l:i],0,np.array([]))
                        if p1>thLowHigh:
                            p1,yy=constr_weighted_polyfit(np.arange(l,i)/ND,tmp,W[l:i],0,thLowHigh)
                    if currPattern[0] == 2:
                        p1,yy=constr_weighted_polyfit(np.arange(l,i)/ND,tmp,W[l:i],0,np.array([]))
                        if p1<=thLowHigh:
                            p1,yy=constr_weighted_polyfit(np.arange(l,i)/ND,tmp,W[l:i],0,thLowHigh)
                    if currPattern[0] == 3:
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vtm[,W(]:i[,P,]]
                            if p1(2)>0:
                                [p1,yy]= constr_weighted_polyfit([l:i]/ND,tmp,W(l:i),0,[])
                            else:
                                rangeCovered= abs(yy[-1]-yy[0]);
                                if rangeCovered < (thLowHigh-minIn):
                                    [p1,yy]= constr_weighted_polyfit([l:i]/ND,tmp,W(l:i),0,[])
                    if currPattern[0] == 4:
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vtm[,W(]:i[,P,]]
                            if p1(2)<0:
                                [p1,yy]= constr_weighted_polyfit([l:i]/ND,tmp,W(l:i),0,[]);
                            else
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    [p1,yy]= constr_weighted_polyfit([l:i]/ND,tmp,W(l:i),0,[]);
                    cost=sum((W(l:i)).*((tmp-yy).^2));v= yy[:];
                    tmp1=[tmp1 cost]
                    tmpv=[tmpv v]
                else:
                    cost=10^12
                    tmp1=np.vstack((tmp1, cost))
                    tmpv=np.vstack((tmpv, 10^12))
            [val,ind]=min(tmp1)
            D[i][0]=val
            bp[i][0]= 1
            vall[i][0]=tmpv(ind)
        
        #ITERATION
        for k in range(1,K):
            for l= P+1+(k-1)*P:Nin #%searchInds(searchInds>=P+1+(k-1)*P) %P+1+(k-1)*P:Nin  %l=k:Nin
                tmp=[] 
                tmpv=[]
                for i in range(l-P):
                    if np.max(W[i:l])>th_w:
                        if currPattern[k] == 1:
                            if currPattern[k-1]==2:
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,[])
                                if p1>thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,thLowHigh)
                            else
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,vall(i,k-1))
                                if p1>thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,-10^12); -
                            -1
                        if currPattern[k] == 2:
                            if currPattern[k-1]==1:
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,[])
                                if p1<thLowHigh:
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,thLowHigh)
                            else:
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],P,vall(i,k-1))
                                if p1>thLowHigh:
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,10^12)
                            -1
                        if currPattern[k] == 3:
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],P,vall(i,k-1))
                            if p1(2)>0;
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,vall(i,k-1))
                            else
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,vall(i,k-1))
                                -1
                            -1
                        if currPattern[k] == 4:
                            p1,yy=constr_weighted_polyfit([i:l]/ND,in(i:l),W(i:l),P,vall(i,k-1));
                            if p1(2)<0:
                                p1,yy=constr_weighted_polyfit([i:l]/ND,in(i:l),W(i:l),0,vall(i,k-1));
                            else:
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)/ND,vin[i:l],W[i:l],0,vall(i,k-1))
                        cost=sum((W(i+1:l)).*((in(i+1:l)-yy(2:-1)).^2));v=yy[:];
                        tmp=[tmp D(i,k-1)+cost];
                        tmpv=[tmpv v];
                    else
                        cost=10^12;
                        tmp=[tmp D(i,k-1)+cost];
                        tmpv=[tmpv 10^12];

                val = np.min(tmp)
                ind = np.argmin(tmp)
                D[l][k]=val
                bp[l][k]= ind
                vall[l][k]=tmpv(ind)
        
        #TERMINATION AND BACKTRACKING
        Ns=[]
        tmp=Nin
        at = np.arange(K,0,-1)
        for i in at:
            Ns=[bp[tmp][i],Ns]
            tmp=bp[tmp][i]
        Ns=[Ns,Nin]

        #RECONSTRUCTION
        cnt=1;y=[];
        for i=1:len(Ns)-1
            tmpX= [Ns(i):Ns(i+1)]/ND;
            tmpIn= in(Ns(i):Ns(i+1)); tmpX(isnan(tmpIn))= [];tmpIn(isnan(tmpIn))= [];
            tmpW= W(Ns(i):Ns(i+1)); tmpW(isnan(tmpW))= [];
            if max(tmpW)>th_w
                if i==1
                    switch(currPattern(i))
                        case 1
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                            if p1>thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[hLo]High); -
                        case 2
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                            if p1<thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[hLo]High); -
                        case 3
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]P,[]);]                            if p1(2)>0
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                            els
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                                -
                            -1
                        case 4
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]P,[]);]                            if p1(2)<0
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                            els
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                                -
                            -1
                    -1
                    p1=p1';
                    y= yy; v= yy[:];
                else
                    switch currPattern(i)
                        case 1
                            if currPattern(i-1)==2
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                                if p1>thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[hLo]High); -
                            else
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                               if p1>thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[10^]2); -
                            -1
                            
                        case 2
                            if currPattern(i-1)==1
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[]);]                                if p1<thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[hLo]High); -
                            else
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                               if p1<thLowHigh; p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[0^1]); -
                            -1
                        case 3
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]P,[);
]                           if p1(2)>0
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                           els
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                               -
                            -1
                        case 4
                            p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]P,[);
]                           if p1(2)<0
                                p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                           els
                                rangeCovered= abs(yy[:]-yy(1));
                                if rangeCovered < (thLowHigh-minIn)
                                    p1,yy=constr_weighted_polyfit(np.arange(i,l+1)tmpIvn,[mpW]0,[);
]                   y=[y yy(2:-1)];v=yy[:]
            else:
                if i==1:
                    p1=10^12;
                    yy= np.ones((1,len(tmpIn)))*10^12;
                    y=yy;v=yy[:];
                else:
                    p1=10^12;
                    yy= np.ones((1,len(tmpIn)))*10^12;
                    y=[y,yy[2:]]
                    v=yy[-1]
            p{cnt}=p1; cnt=cnt+1;
        E=np.sum(np.multiply(W(Ns(1):Ns[:]),np.power((vin(Ns(1):Ns[:])-y)),2)))/len(y)
    return Ns, p, y, E