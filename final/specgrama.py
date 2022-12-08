import numpy as np
from scipy.fftpack import fft as fft

def matlabfft(arr,n):
        if arr.shape[0] < n :
                arr = np.vstack((arr,np.zeros((n - arr.shape[0],arr.shape[1]))))
        elif arr.shape[0] > n :
                arr = arr[:n,:]
        ans = np.zeros(arr.shape,dtype=complex)
        for j in range(arr.shape[1]):
                ans[:,j] = fft(arr[:,j])
        return ans

def specgrama(x,nfft,Fs,window,noverlap):
    nx = x.shape[0]
    nwind = window.shape[0]
    if nx < nwind:
        x[nwind-1] = 0
        nx = nwind

    ncol = int(np.fix((nx-noverlap)/(nwind-noverlap)))
    colindex = 1+ np.arange(ncol)*(nwind-noverlap)
    rowindex = np.reshape(np.arange(nwind), (nwind,1))
    if len(x)<(nwind+colindex[-1]-1):
        x[nwind+colindex[ncol]-1] = 0
    
    y = np.zeros((nwind,ncol))
    temprow = np.multiply(rowindex,np.ones((1,ncol)))
    temprow = np.array(temprow, dtype='int')
    tempcol = np.multiply(np.ones((nwind,1)),colindex.reshape(1,colindex.shape[0]))
    tempcol = np.array(tempcol, dtype='int')
    
    f = lambda indc:x[indc]
    tempind = np.array(temprow+tempcol-1,dtype='int')
    y[:] = f(tempind)

    # % Apply the window to the array of offset signal segments.
    y = np.multiply(window.reshape(window.shape[0],1),np.ones((1,ncol))) * y

    y = matlabfft(y,nfft)
    if np.any(np.isreal(x)):
        if nfft % 2 == 1:
            select = np.arange((nfft+1)/2, dtype='int')
        else:
            select = np.arange((nfft/2)+1, dtype='int')
        y = y[select,:]
    else:
        select = np.arange(nfft, dtype='int')
  
    f = select * Fs/nfft
    t = (colindex-1)/Fs
    return y,f,t


