import numpy as np

def dtw(x,y,addD):
    X = np.copy(x)
    Y = np.copy(y)
    N1= np.size(X,1)
    N2= np.size(Y,1)
    if addD==1:
        newmat = 0.5*(np.hstack(X[:,1:N1],X[:,N1-1:N1])-np.hstack(X[:,0:1],X[:,0:N1-1]))
        X = np.vstack((X, 0.5*newmat))
        newmat = 0.5*(np.hstack(Y[:,1:N2],Y[:,N2-1:N2])-np.hstack(Y[:,0:1],Y[:,0:N2-1]))
        Y = np.vstack((Y, 0.5*newmat))
    d = np.zeros(N1,N2)
    for n1 in range(N1):
        for n2 in range(N2):
            d[n1,n2] = np.sqrt(np.sum(np.square(X[:,n1] - Y[:,n2])))
    
    #auxiliary matrix for backtracking
    m = np.zeros((N1,N2),dtype=np.int8)
    #viterbi
    for n1 in range(N1):
        for n2 in range(N2):
            if n1==0 and n2==0:
                # no possible movements
                m[n1,n2]=0
            elif n1==1:
                # only reachable from a lower n2
                m[n1,n2] = 1
                d[n1,n2] = d[n1,n2-1]+d[n1,n2]
            elif n2==1:
                # only reachable from a lower n1
                m[n1,n2] = 10
                d[n1,n2] = d[n1-1,n2]+d[n1,n2]
            else:
                # reachable from 3 different points: vertical, horizontal, diagonal
                dbackup = d[n1,n2]
                d[n1,n2] = np.inf
                dtry = d[n1,n2-1] + dbackup
                if dtry < d[n1,n2]:
                    m[n1,n2] = 0
                    d[n1,n2] = dtry
                dtry = d[n1-1,n2] + dbackup
                if dtry<d[n1,n2]:
                    m[n1,n2] = 10
                    d[n1,n2] = dtry
                dtry = d[n1-1,n2-1] + 1.5*dbackup
                if dtry < d[n1,n2]:
                    m[n1,n2]=11
                    d[n1,n2]=dtry
    # global distance
    avd=d[N1-1,N2-1]
    # free space
    d=[]
    # backtracking
    ind1 = []
    ind2 = []
    n1 = N1-1
    n2 = N2-1
    while n1>0 or n2>0:
        ind1 = [n1] + ind1
        ind2 = [n2] + ind2
        if m[n1,n2]==1:
            n2 = n2-1
        elif m[n1,n2]==10:
            n1 = n1-1
        elif m[n1,n2]==11:
            n1 = n1-1
            n2 = n2-1 

    ind1 = [1] + ind1
    ind2 = [1] + ind2

    return ind1,ind2,avd
