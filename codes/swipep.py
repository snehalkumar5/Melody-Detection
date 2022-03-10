import math
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from numpy import matlib
from scipy.io import wavfile
from matplotlib import mlab
from scipy import signal
from scipy import interpolate

WAVE_OUTPUT_FILENAME = '../../followTones/codes/114.wav'  # Provide here the path to an audio

def swipep(x,fs,plim,dt,dlog2p,dERBs,woverlap,sTHR):
    """
    Swipe pitch estimation method.
    It estimates the pitch of the vector signal X with sampling frequency Fs
     (in Hertz) every DT seconds. The pitch is estimated by sampling the spectrum
     in the ERB scale using a step of size DERBS ERBs. The pitch is searched
     within the range [PMIN PMAX] (in Hertz) sampled every DLOG2P units in a
    base-2 logarithmic scale of Hertz. The pitch is fine tuned by using parabolic
     interpolation with a resolution of 1/64 of semitone (approx. 1.6 cents).
    Pitches with a strength lower than STHR are treated as undefined.
    :param x:
    :param fs:
    :param plim:
    :return: [P,T,S] returns the times T at which the pitch was estimated and the pitch 
    strength S of every pitch estimate.
    """
    if not plim:
        plim = np.array([30, 5000])
    if not dt:
        dt = 0.001
    if not dlog2p:
        dlog2p = 1.0 / 48.0
    if not dERBs:
        dERBs = 0.1
    if not woverlap:
        woverlap = 0.5
    elif woverlap>1 or woverlap<0:
        raise Exception("Window overlap must be between 0 and 1.")
    if not sTHR:
        sTHR = -float('Inf')
    # t = np.transpose(np.arange(0, len(x) / float(fs)+dt, dt))    # Times
    t = np.arange(0, len(x) / float(fs), dt)    # Times
    # Define pitch candidates
    plim = np.array(plim)
    # log2pc = np.transpose(np.arange(np.log2(plim[0]), np.log2(plim[1]), dlog2p))
    log2pc = np.arange(np.log2(plim[0]), np.log2(plim[1]), dlog2p)
    pc = np.power(2, log2pc)
    S = np.zeros(shape=(len(pc), len(t)))   # Pitch strength matrix

    # Determine P2-WSs
    logWs = np.round_(np.log2(np.multiply(8,np.divide(float(fs),plim))))
    ws = np.power(2, np.arange(logWs[0], logWs[1]-1, -1))   # P2-WSs
    pO = 8* np.divide(fs, ws)   # Optimal pitches for P2-WSs

    # Determine window sizes used by each pitch candidate
    d = 1 + log2pc - np.log2(np.multiply(8, (np.divide(fs, ws[1 - 1]))))
    # print(d)
    # Create ERB-scale uniformly-spaced frequencies (in Hertz)
    fERBs = erbs2hz(np.arange(hz2erbs(min(pc) / 4), hz2erbs(fs / 2), dERBs))
    # fERBs = erbs2hz(np.transpose(np.arange(hz2erbs(min(pc) / 4), hz2erbs(fs / 2), dERBs)))
    for i in range(0, ws.size):
        dn = max(1, round( 8*(1-woverlap) * fs / pO[i])) # Hop size
        # Zero pad signal
        xzp = np.hstack((np.zeros((int(ws[i]/2))), x, np.zeros((int(dn + ws[i]/2)))))
        # Compute spectrum
        w = np.hanning(ws[i])  # Hann window
        o = int(max(0, round(ws[i] - dn)))  # Window overlap

        # [X, f, ti, im] = plt.specgram(xzp, NFFT=int(ws[i]), Fs=fs, window=w, noverlap=int(o), mode='psd')
        [X, f, ti] = mlab.specgram(xzp, NFFT=int(ws[i]), Fs=fs, window=w, noverlap=int(o), mode='psd')
        with open('temp.txt','w') as wr:
            print('X:',X,file=wr)
        # print('X:',X)
        # print('f:',f)
        # print('ti:',ti)
        # quit()
        # Select candidates that use this window size
        if ws.size == 1:
            j = np.transpose(pc)
            k = np.array([])
        else:
            if i == ws.size:
                j = np.nonzero(d - (i+1) > -1.)[0]
                k = np.nonzero(d[j] - (i + 1) < 0.)[0]
            else:
                if i == 0:
                    j = np.nonzero(d - (i + 1) < 1.)[0]
                    k = np.nonzero(d[j] - (i + 1) > 0.)[0]
                else:
                    j = np.nonzero(abs(d - (i + 1)) < 1.)[0]
                    k = np.arange(0, j[0].size)  # transpose added by KG
                    # k = np.transpose(k1)

        # Interpolate at equidistant ERBs steps
        f = np.array(f)
        X1 = np.transpose(X)
        fERBs = fERBs[np.argmax(fERBs > pc[j[0]]/4) : ]
        # print(fERBs.shape)
        ip = interpolate.interp1d(f, abs(X1), kind='cubic', bounds_error=False, fill_value=0.0)(fERBs[:, np.newaxis])
        interpol = ip.transpose(2, 0, 1).reshape(-1, ip.shape[1])
        interpol1 = np.transpose(interpol)
        M = np.maximum(0, interpol1)  # Magnitude
        L = np.sqrt(M)  # Loudness
        # Compute pitch strength
        Si = pitchStrengthAllCandidates(fERBs, L, pc[j])
        # Interpolate pitch strength at desired times
        if Si.shape[1] > 1:
            tf = []
            tf = ti.tolist()
            tf.insert(0, 0)
            del tf[-1]
            ti = np.asarray(tf)
            Si = interpolate.interp1d(ti, Si, 'linear', fill_value=nan)(t)
        else:
            Si = matlib.repmat(float('NaN'), len(Si), len(t))
        # Add pitch strength to combination
        lambda1 = d[j[k]] - (i + 1)
        mu = ones(size(j))
        mu[k] = 1 - abs(lambda1)
        # print(mu[k])
        # S[j, :] = S[j, :] + np.multiply(((np.kron(np.ones((Si.shape[1], 1)), mu)).transpose()), Si)
        S[j] = S[j] + np.tile(mu, (Si.shape[1], 1)).T * Si

    # Fine-tune the pitch using parabolic interpolation
    p = np.empty((S.shape[1]))
    p[:] = np.nan
    s = np.empty((S.shape[1]))
    s[:] = np.nan
    for j in range(0, S.shape[1]):
        s[j] = (S[:, j]).max(0)
        i = np.argmax(S[:, j])
        if s[j] < sTHR:
            continue
        if i == 0 or i == pc.size-1:
            p[j] = pc[0]
        else:
            I = np.arange(i - 1, i + 2)
            tc = np.divide(1, pc[I])
            ntc = ((tc / tc[1]) - 1) * 2 * np.pi
            c = polyfit(ntc, (S[I, j]), 2)
            ftc = 1 / 2 ** np.arange(np.log2(pc[I[0]]), np.log2(pc[I[2]]), 1./12./100.)
            # ftc = np.divide(1, np.power(2, np.arange(np.log2(pc[I[0]]), np.log2(pc[I[2]]), (1/12)/100)))
            nftc = ((ftc / tc[1]) - 1) * 2 * np.pi
            s[j] = np.nanmax(polyval(c, nftc))
            k = np.argmax(polyval(c, nftc))
            p[j] = 2 ** (np.log2(pc[I[0]])) + (k - 1) / 12. / 100.
    return p, t, s


def pitchStrengthAllCandidates(f, L, pc):
    # print('l',L)
    """Normalize loudness."""
    # Create pitch strength matrix
    S = np.zeros((pc.size, L.shape[1]))
    # Define integration regions
    k = np.ones(len(pc)+1, int)
    print('fshape',f.shape)
    for j in range(0,len(k)-1):
        k[j+1] = k[j] + np.argmax(f[np.int16(k[j]):] > pc[j]/4)
    k = k[1:]
    # Create loudness normalization matrix
    N = np.sqrt(flipud(cumsum(flipud(np.multiply(L,L)),axis=1)))
    for j in range(0, len(pc)):
        n = N[k[j],:]
        n[n==0] = -np.inf
        l1 = L[k[j]:,:]
        l2 = matlib.repmat(n,L.shape[0]-k[j],1)
        NL = np.divide(l1, l2)
        S[j, :] = pitchStrengthOneCandidate(f[k[j]:], NL, pc[j])
    return S

numArr = []


def is_prime(n):
    """Function to check if the number is prime or not."""
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def primeArr(n):
    """Return a list containing only prime numbers."""
    for num in range(1, n + 2):
        if is_prime(num):
            numArr.append(num)
    jg = (np.expand_dims(numArr, axis=1)).transpose()
    return numArr


def pitchStrengthOneCandidate(f, NL, pc):
    # print('shapes:',f.shape, NL.shape, pc.shape)

    n = fix(f[-1] / pc - 0.75) # Number of harmonics
    if n == 0:
        return NaN
    k = np.zeros(size(f))
    # Normalize frequency w.r.t. candidate
    q = f / pc
    # Create kernel
    for i in (primeArr(int(n))):
        a = abs(q - i)
        # Peak's weigth
        p = a < .25
        k[p] = np.cos(2 * math.pi * q[p])
        # Valleys' weights
        v = np.logical_and(.25 < a, a < .75)
        k[v] += np.cos(2 * np.pi * q[v]) / 2

    # Apply envelope
    ff = np.divide(1, f)
    k = np.multiply(k, np.sqrt(ff))
    # K+-normalize kernel
    k = k / norm(k[k > 0])
    # Compute pitch strength
    # print("yesss")
    S = np.dot((k[:, np.newaxis]).transpose(), NL)
    return S


def hz2erbs(hz):
    """Converting hz to erbs."""
    erbs = 6.44 * (np.log2(229 + hz) - 7.84)
    return erbs


def erbs2hz(erbs):
    """Converting erbs to hz."""
    hz = (np.power(2, np.divide(erbs, 6.44) + 7.84)) - 229
    return hz


def swipe(audioPath):
    """Read the audio file and output the pitches and pitch contour."""
    print("Swipe running", audioPath)
    fs, x = wavfile.read(audioPath)
    # np.seterr(divide='ignore', invalid='ignore')
    p, t, s = swipep(x, fs, [75, 500], 0.01, [], 1/20, 0.5, 0.2)
    print("Pitches: ", p)
    fig = plt.figure()
    plt.plot(1000*t,p)
    fig.savefig('output.png')
    plt.show()  # show in a window of contour on UI

swipe(WAVE_OUTPUT_FILENAME)