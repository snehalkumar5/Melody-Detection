import numpy as np

def weightedMedian(sig,W,order):
    nSig = len(sig)
    sig = np.reshape(sig,(sig.shape[0],1))
    W = np.reshape(W,(W.shape[0],1))

    if order%2 != 1:
        m = order/2
    else:
        m = (order-1)/2
        
    m = int(m)
    X = np.vstack(( np.zeros((m,1)), sig, np.zeros((m,1)) ))
    w = np.vstack(( np.zeros((m,1)), W, np.zeros((m,1)) ))
    out = np.zeros((nSig,1))
    tp = np.arange(0,order)
    indr = np.reshape(tp, (tp.shape[0],1))
    indc = np.arange(1,nSig+1)
    indc = np.reshape(indc,(1,indc.shape[0]))
    i1 = np.tile(indc[:nSig],(order,1))
    i2 = np.tile(indr[:],(1,nSig))
    ind = i1+i2
    xx = np.reshape(X[ind-1],(order,nSig))
    ww = np.reshape(w[ind-1],(order,nSig))
    for i in range(ww.shape[1]):
        out[i]= weightedMedian_chunk(xx[:,i],ww[:,i]+np.spacing(1))

    return out

def weightedMedian_chunk(D,W):
    if D.shape != W.shape:
        print("Error")
        return

    # normalize the weights, such that: sum ( w_ij ) = 1
    # (sum of all weights equal to one)
    WSum = np.sum(W)
    W = W / WSum

    # (line by line) transformation of the input-matrices to line-vectors
    d = D.flatten()
    w = W.flatten()
    dt = np.reshape(d,(d.shape[0],1))
    wt = np.reshape(w,(w.shape[0],1))
    A = np.hstack((dt,wt))
    ASort = A[A[:,0].argsort()]

    dSort = ASort[:,0]
    dSort = np.reshape(dSort, (1,dSort.shape[0]))
    wSort = ASort[:,1]
    wSort = np.reshape(wSort, (1,wSort.shape[0]))

    sumVec = np.array([])
    for i in range(wSort.shape[1]):
        sumVec = np.cumsum(wSort[:i])
    sumVec = np.reshape(sumVec, (1,sumVec.shape[0]))
    
    wMed = np.array([])
    j = 0
    while wMed.size == 0:
        if sumVec[:,j] >= 0.5:
            wMed = dSort[:,j]
        j+=1
    if (np.sum(wSort[:j-1])>0.5) and (np.sum(wSort[j:])>0.5):
        raise Exception('weightedMedian:unknownError The weighted median could not be calculated.')
    
    return wMed