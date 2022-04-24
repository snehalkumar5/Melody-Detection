import numpy as np
import math

def constr_weighted_polyfit(X,Y,W,P,ita):
    if X.shape[0]>X.shape[1]:
        X = np.reshape(X, (X.shape[1],X.shape[0]))
    if Y.shape[0]>Y.shape[1]:
        Y = np.reshape(Y, (Y.shape[1],Y.shape[0]))
    if W.shape[0]>W.shape[1]:
        W = np.reshape(W, (W.shape[1],W.shape[0]))
    l = np.arange(0,P)
    l = np.reshape(l, (1,l.shape[0]))
    A1 = np.array([])
    for i in range(P+1):
        A1 = np.vstack(A1,math.sqrt(W)*(pow(X,i)))
    A = A1*np.transpose(A1)
    b = A1*(math.sqrt(W)*Y)

    if not ita:
        A = np.hstack(X[0]**l,A)
        A = np.vstack(A,np.transpose(X[0]**l))
        b = np.vstack(b, ita)

    tmp=np.pinv(A)*b
    if  not ita:
        p=tmp[1:]
    else:
        p = tmp
    out=np.polyval(np.flipud(p),X)
    return p, out