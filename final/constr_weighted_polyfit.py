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
    # l = np.reshape(l, (1,l.shape[0]))
    print(X.shape,W.shape)
    A1= 0 
    for i in range(P):
        if(i==0):
            A1 = np.multiply(np.sqrt(W),(pow(X,i)))
        else:
            A1 = np.vstack((A1,np.multiply(np.sqrt(W),(pow(X,i)))))
    print(A1.shape, np.transpose(A1))
    A = np.matmul(A1, np.transpose(A1))
    b = np.matmul(A1,np.transpose(np.multiply(np.sqrt(W),Y)))
    print(b.shape)
    print(ita)
    if ita:
        # print(X[0][0])
        # print(l)
        # print(np.power(X[0][0],l).shape)
        tmp = np.reshape(np.power(X[0][0],l), (np.power(X[0][0],l).shape[0],1))
        A = np.hstack((tmp,A))
        tmp1 = np.array([0, np.power(X[0][0],l)])
        A = np.vstack((A,tmp1))
        b = np.vstack((b, ita))

    tmp= np.matmul(np.linalg.pinv(A),b)
    if ita:
        p=tmp[1:]
    else:
        p = tmp
    out=np.polyval(np.flipud(p),X)
    return p, out