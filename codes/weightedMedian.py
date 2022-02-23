import numpy as np

def weightedMedian(sig,W,order):
    nSig = len(sig)
    if nSig%2 == 0:
        m = order/2
    else:
        m = (order-1)/2
    X = np.hstack( np.zeros((m,1)), sig, np.zeros((m,1)) )
    w = np.hstack( np.zeros((m,1)), W, np.zeros((m,1)) )
    out = np.zeros((nSig,1))
    tp = np.arange(0,order-1)
    indr = np.reshape(tp, (tp.shape[0],1))
    indc = np.arange(0,nSig)
    ind = indc[np.ones((1,order),int) :nSig] + indr[:,np.ones((1,nSig),int)]
    xx = np.reshape(X[ind],(order,nSig))
    ww = np.reshape(W[ind],(order,nSig))
    for i in range(ww.shape[1]):
        out[i]= weightedMedian_chunk(xx[:,i],ww[:,i]+np.spacing(1))

def weightedMedian_chunk(D,W):

    dSort = ASort[:,0]
    dSort = np.reshape(dSort, (dSort.shape[0],1))
    wSort = ASort[:,1]
    wSort = np.reshape(wSort, (wSort.shape[0],1))


    sumVec = np.array([])
    for i in range(len(wSort)):
        sumVec[i] = np.sum(wSort[:i])

    wMed = np.array([])
    j = 0
    while wMed.size == 0:
        j+=1
        if sumVec[j] >= 0.5:
            wMed = dSort[j]


    if (np.sum(wSort[:j-1])>0.5) and (np.sum(wSort[j:])>0.5):
        raise Exception('weightedMedian:unknownError', ...
            'The weighted median could not be calculated.')