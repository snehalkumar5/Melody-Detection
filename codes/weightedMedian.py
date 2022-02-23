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
    indr = np.arange(0,order-1).T
    indc = np.arange(0,nSig)
    ind = indc[np.ones((1,order),int) :nSig] + indr[:,np.ones((1,nSig),int)]
    xx = np.reshape(X[ind],(order,nSig))
    ww = np.reshape(W[ind],(order,nSig))
    for i in range(ww.shape[1]):
        out[i]= weightedMedian_chunk(xx[:,i],ww[:,i]+np.spacing(1))

