#DONE
import numpy as np
import numpy.matlib

def reVal(num):
    if (num >= 0 and num <= 9):
        return chr(num + ord('0'))
    else:
        return chr(num - 10 + ord('A'))

def dec2base(inputNum, base, pad):
    res= [[] for i in range(len(inputNum))]
    for idx,val in enumerate(inputNum):
        tmp = []
        while val>0:
            tmp.append(str(reVal(val%base)))
            val = int(val/base)
        n = len(tmp)
        while n < pad:
            tmp.append('0')
            n+=1
        tmp = tmp[::-1]
        res[idx] = tmp
    return np.array(res)

def getremoverows(arr,indx,value,matcharr, combarr):
    remrows = np.array([], dtype=int)
    for rrow in matcharr:
        if arr[rrow][indx] == value:
            remrows = np.append(remrows, rrow)
    combarr = np.hstack((combarr,remrows))
    return combarr

def createPatterns():
    # 1==> low, 2==> high, 3==> fall, 4==> rise, 5==> dive
    num = pow(4,5)
    rr = np.arange(num)
    outString = dec2base(rr, 4, 5)

    out = np.zeros(shape=outString.shape, dtype=int)
    for i in range(outString.shape[0]):
        for j in range(outString.shape[1]):
            out[i][j] = int(outString[i][j])

    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i][j] += 1

    # High should not be at the end.
    n = len(out)
    tmp= []
    for i in range(n):
        if out[i][-1] == 2:
            tmp.append(i)
    out = np.delete(out,tmp,axis=0)

    # fall, high, low should not followed by rise
    for i in range(out.shape[1]):
        refInds = np.nonzero(out[:,i]==4)[0]
        removeInds= np.array([], dtype=int)
        for j in range(i+1, out.shape[1]):
            removeInds = getremoverows(out,j,3,refInds,removeInds)
            removeInds = getremoverows(out,j,2,refInds,removeInds)
            removeInds = getremoverows(out,j,1,refInds,removeInds)
        out = np.delete(out, removeInds, axis=0)

    # high should not be followed by fall
    for i in range(out.shape[1]):
        refInds= np.nonzero(out[:,i]==3)[0]
        removeInds= np.array([], dtype=int)
        for j in range(i+1,out.shape[1]):
            removeInds = getremoverows(out,j,2,refInds,removeInds)
        
        out = np.delete(out, removeInds, axis=0)

    patterns = {0:[[]],1:[[]],2:[[]],3:[[]],4:[[]]}
    for i in range(out.shape[0]):
        currPattern= np.array(out[i,:])
        removeInds= np.array([], dtype=int)
        dd = np.diff(currPattern)
        for idx,val in enumerate(dd):
            if val == 0:
                removeInds = np.append(removeInds,idx)
        currPattern = np.delete(currPattern, removeInds)
        temp = np.unique(np.sort(currPattern))
        
        notAdd = 0
        if (len(temp)==1 and (temp[0]==1 or temp[0]==2)):
            notAdd= 1
        elif len(temp) == 2:
            if temp[0]==1 and temp[1]==2:
                notAdd= 1
        
        if notAdd==0:
            patlength = len(currPattern)-1
            if len(patterns[patlength][0])==0:
                patterns[patlength] = [currPattern]
            else:
                patterns[patlength].append(currPattern)

    for iterPattern in range(len(patterns)):
        currPattern= np.array(patterns[iterPattern], dtype=object)

    for iterPattern in range(len(patterns)):
        currPattern= np.array(patterns[iterPattern])
        rows, cols = currPattern.shape
        temp = np.sum(np.multiply(currPattern,(np.matlib.repmat(np.power(4,np.arange(cols-1,-1,-1)),rows,1))),axis=1)
        _,inds= np.unique(temp, return_index=True)
        currPattern1 = np.empty_like(currPattern[0])
        for idx in inds:
            tm = currPattern[idx]
            currPattern1 = np.vstack((currPattern1,tm))
        currPattern = currPattern1[1:]
        remInds = np.array([],dtype=int)
        for idx,v in enumerate(currPattern):
            unique,cnts = np.unique(v,return_counts=True)
            tmp = dict(zip(unique,cnts))
            if (2 in tmp and tmp[2]>1) or (3 in tmp and tmp[3]>1) or (4 in tmp and tmp[4]>1):
                remInds = np.append(remInds,idx)
        currPattern = np.delete(currPattern,remInds,axis=0)
        
        # occurrence of low after the tones other than low is always preceeded by rise.
        temp = np.array(currPattern[:,1:])
        
        for i in range(temp.shape[1]):
            refInds= np.nonzero(temp[:,i]==1)[0]
            removeInds= np.array([], dtype=int)
            for j in range(i+1,temp.shape[1]):
                removeInds= getremoverows(temp,j,2,refInds,removeInds)
                removeInds= getremoverows(temp,j,3,refInds,removeInds)
        
            currPattern = np.delete(currPattern, removeInds, axis=0)
            temp= currPattern[:,1:]
        
        if cols==1:
            temp= 5
        else:
            highInds= np.nonzero(currPattern[:,-2]==2)[0]
            currPattern1 = np.empty_like(currPattern[0])
            for idx in highInds:
                tm = currPattern[idx]
                currPattern1 = np.vstack((currPattern1,tm))
            if highInds.any():
                temp = currPattern1[1:]
            if temp[0].shape != currPattern[0].shape:
                temp = np.array([[0]*currPattern.shape[1]]*1)
            if not temp.any():
                temp = temp
            else:
                temp[:,-1]= 5
            rows = temp.shape[0]
            cols = temp.shape[1]
            temp1 = np.sum(np.multiply(temp,(np.matlib.repmat(np.power(4,np.arange(cols-1,-1,-1)),rows,1))),axis=1)
            _,inds= np.unique(temp1, return_index=True)
            temp2 = np.empty_like(temp[0])
            for idx in inds:
                tm = temp[idx]
                temp2 = np.vstack((temp2,tm))
            temp = temp2[1:]
        currPattern= np.vstack((currPattern,temp))
        patterns[iterPattern]= currPattern

    outPatterns= {0:[[]]}
    for iterPattern in range(len(patterns)):
        currPattern = np.array(patterns[iterPattern])
        for i in range(currPattern.shape[0]):
            if not currPattern[i].any():
                continue
            print(currPattern[i])
            outPatterns[0].append(currPattern[i,:])

    return outPatterns

createPatterns()