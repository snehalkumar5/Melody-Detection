import numpy as np

def constr_weighted_polyfit(X,Y,W,P,ita):
    if X.shape[0]>X.shape[1]:
        X = np.reshape(X, (X.shape[1],X.shape[0]))
    if Y.shape[0]>Y.shape[1]:
        Y = np.reshape(Y, (Y.shape[1],Y.shape[0]))
    if W.shape[0]>W.shape[1]:
        W = np.reshape(W, (W.shape[1],W.shape[0]))
    l = np.arange(0,P+1)
    A1= 0 
    for i in range(P+1):
        if i==0:
            A1 = np.multiply(np.sqrt(W),(pow(X,i)))
        else:
            A1 = np.vstack((A1,np.multiply(np.sqrt(W),(pow(X,i)))))
    A = np.matmul(A1, np.transpose(A1))
    b = np.matmul(A1,np.transpose(np.multiply(np.sqrt(W),Y)))
    if ita:
        tmp = np.reshape(np.power(X[0][0],l), (np.power(X[0][0],l).shape[0],1))
        A = np.hstack((tmp,A))
        tmpw = np.hstack((np.array([0]), np.power(X[0][0],l)))
        tmp1 = np.reshape(tmpw, (1,tmpw.shape[0]))
        A = np.vstack((A,tmp1))
        b = np.vstack((b, ita))

    tmp= np.matmul(np.linalg.pinv(A),b)
    if ita:
        p=tmp[1:]
    else:
        p = tmp
    out=np.polyval(np.flipud(p),X)
    return p, out