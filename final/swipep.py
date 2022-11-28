# coding: utf-8
"""SWIPE' pitch extraction."""

import math
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from numpy import matlib
from scipy.io import wavfile
from scipy import signal
from scipy import interpolate
from specgrama import specgrama
from decimal import *

def interpolation(f, X, fERBs):
    interpol = np.array([])
    for i in range(0,X.shape[1]):
            func = interpolate.interp1d(f,np.abs(X[:,i]),kind='cubic')
            xnew = fERBs 
            ip = func(xnew)
            ip = ip.reshape((ip.shape[0],1))
            if len(interpol) == 0:
                interpol = ip
            else:
                interpol = np.hstack((interpol,ip))
    interpol = interpol.reshape((fERBs.shape[0],X.shape[1]))
    return interpol

def swipep(x, fs, plim, dt, dlog2p, dERBs, woverlap, sTHR):
    np.seterr(divide='ignore', invalid='ignore')
    """Swipe pitch estimation method.

    It estimates the pitch of the vector signal X with sampling frequency Fs
     (in Hertz) every DT seconds. The pitch is estimated by sampling the spectrum
     in the ERB scale using a step of size DERBS ERBs. The pitch is searched
     within the range [PMIN PMAX] (in Hertz) sampled every DLOG2P units in a
    base-2 logarithmic scale of Hertz. The pitch is fine tuned by using parabolic
     interpolation with a resolution of 1/64 of semitone (approx. 1.6 cents).
    Pitches with a strength lower than STHR are treated as undefined.
    """
    if not plim:
        plim = [30, 5000]
    if not dt:
        dt = 0.001
    if not dlog2p:
        dlog2p = 1.0 / 96.0
    if not dERBs:
        dERBs = 0.1
    if not sTHR:
        sTHR = -float('Inf')
    if not woverlap:
        woverlap = 0.5

    t = np.arange(0.0, (len(x) / float(fs)), dt)    # Times
    dc = round(8*(1-woverlap))  # Hop size (in cycles)
    K = 2   # Parameter k for Hann window
    # Define pitch candidates
    log2pc = np.arange(np.log2(plim[0]), np.log2(plim[1]), dlog2p)
    pc = np.power(2, log2pc)

    S = np.zeros(shape=(len(pc), len(t)))   # Pitch strength matrix

    # Determine P2-WSs
    logWs = np.round_(np.log2(np.multiply(4 * K, (np.divide(float(fs), plim)))))
    ws = np.power(2, np.arange(logWs[1 - 1], logWs[2 - 1] - 1, -1))   # P2-WSs
    pO = 4 * K * np.divide(fs, ws)   # Optimal pitches for P2-WSs
    # Determine window sizes used by each pitch candidate
    d = 1 + log2pc - np.log2(np.multiply(4 * K, (np.divide(fs, ws[1 - 1]))))
    # Create ERBs spaced frequencies (in Hertz)
    fERBs = erbs2hz(np.arange(hz2erbs(pc[1 - 1] / 4), hz2erbs(fs / 2), dERBs))

    for i in range(0, len(ws)):
        # for i in range(0, 1):
        dn = int(round(dc * fs / pO[i]))  # Hop size (in samples)
        # Zero pad signal
        will = np.zeros((int(ws[i]/2),1))
        learn = np.reshape(x, -1, order='F')[:, np.newaxis]
        mir = np.zeros((dn + int(ws[i]/ 2), 1))
        xzp = np.vstack((will, learn, mir))
        xk = np.reshape(xzp, len(xzp), order='F')
        # Compute spectrum
        w = np.hanning(ws[i])  # Hann window
        o = max(0, round(ws[i] - dn))  # Window overlap
        # [X, f, ti, im] = plt.specgram(xk, NFFT=int(ws[i]), Fs=fs, window=w, noverlap=int(o))
        X, fa, tia = specgrama(xk,int(ws[i]),fs,w, int(o))
        f, ti, _ = signal.spectrogram(xk, nfft=int(ws[i]), fs=fs, window=w, noverlap=int(o), mode='complex')

        # Interpolate at equidistant ERBs steps
        f = np.array(f)
        j=0
        # Select candidates that use this window size
        if i == (len(ws) - 1):
            j = np.where(d - (i + 1) > -1)
            k = np.where(d[j] - (i + 1) < 0)
        elif i == 0:
            j = np.where(d - (i + 1) < 1)
            k = np.where(d[j] - (i + 1) > 0)
        else:
            j = np.where(abs(d - (i + 1)) < 1)
            k1 = np.arange(0, len(j))  # transpose added by KG
            k = np.transpose(k1)
        fERBs = fERBs[np.where(fERBs > pc[j[0][0]]/4)[0][0]:]
        ip = interpolation(f, X, fERBs)

        # ip = interpolate.interp1d(f, abs(X1), kind='cubic')(fERBs[:, np.newaxis])
        # ip = interpolate.splrep(f, abs(X1))(fERBs[:, np.newaxis])
        # ip = interpolate.CubicSpline(f, abs(X))(fERBs[:, np.newaxis])
        # ip = interpolate.interp1d(tmpf, tmpX, kind='cubic')(fERBs[:, np.newaxis])
        # interpol = ip.transpose(2, 0, 1).reshape(-1, ip.shape[1])
        # interpol1 = np.transpose(interpol)
        # interpol1 = np.transpose(ip)
        M = np.maximum(0, ip)  # Magnitude
        L = np.sqrt(M)  # Loudness
        L=np.real(L)
        fERBs = np.real(fERBs)

        Si = pitchStrengthAllCandidates(fERBs, L, pc[j])
        # Interpolate at desired times
        if Si.shape[1] > 1:
            Si = interpolate.interp1d(tia, Si, 'linear', fill_value=np.nan)(t)
        else:
            Si = matlib.repmat(np.NaN, len(Si), len(t))
        lambda1 = np.take(d,np.take(j,k)) - (i + 1)
        mu = np.ones(size(j))
        mu[k] = 1 - abs(lambda1)
        S[j, :] += np.multiply(np.matmul(mu.reshape(mu.shape[0],1),np.ones((1,Si.shape[1]))), Si)

    S = np.real(S)
    # Fine-tune the pitch using parabolic interpolation
    p = np.empty((S.shape[1],1))
    p[:][:] = np.NAN
    s = np.empty((S.shape[1],1))
    s[:][:] = np.NAN
    for j in range(S.shape[1]):
        s[j] = np.max(S[:,j])
        id = np.argmax(S[:,j])
        if s[j] < sTHR:
            continue
        if id == 0:
            p[j] = pc[id]
        elif id == len(pc) - 1:
            p[j] = pc[id]
        else:
            I = np.arange(id - 1, id + 2)
            tc = np.divide(1, pc[I])
            ntc = ((tc / tc[1]) - 1) * 2 * np.pi
            c = np.polyfit(ntc, (S[I, j]), 2)
            ftc = np.divide(1, np.power(2, np.arange(np.log2(pc[I[0]]), np.log2(pc[I[2]])+1/1200 , 1/1200)))
            nftc = ((ftc / tc[1]) - 1) * 2 * np.pi
            s[j] = (np.polyval(c, nftc)).max(0)
            k = np.argmax(np.polyval(c, nftc))
            p[j] = np.power(2,(np.log2(pc[I[0]]) + (k - 1)/1200))
    # p[np.isnan(s) - 1] = float('NaN')  # added by KG for 0s
    return p, t, s


def pitchStrengthAllCandidates(f, L, pc):
    """Normalize loudness."""
    # Create pritch strength matrix
    S = np.zeros((pc.shape[0], L.shape[1]))
	# Define integration regions
    k = np.zeros((pc.shape[0] + 1,1), dtype='int')
    for j in range(0, k.shape[0]-1):
        k[j+1][0] = k[j][0] + np.argmax(f[k[j][0]:] > pc[j]/4)
    k = k[1:]

    # Create loudness normalization matrix
    N = np.sqrt(np.flipud(np.cumsum(np.flipud(L*L), 0)))

    for j in range(0, pc.size):
        # Normalize loudness
        n = N[k[j][0]][:]
        n[n == 0] = -np.inf # to make zero-loudness equal zero after normalization
        NL = L[k[j][0] :] / np.matlib.repmat(n, L.shape[0] - k[j][0], 1)

        # Compute pitch strength
        S[j] = pitchStrengthOneCandidate(f[k[j][0] :], NL, pc[j])

    return S
    
numArr = []

def is_prime(n):
    """Function to check if the number is prime or not."""
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def primes_method5(n):
    out = list()
    sieve = [True] * (n+1)
    for p in range(2, n+1):
        if (sieve[p]):
            out.append(p)
            for i in range(p, n+1, p):
                sieve[i] = False
    return out


def primeArr(n):
    """Return a list containing only prime numbers."""
    for num in range(1, n + 2):
        if is_prime(num):
            numArr.append(num)
    return numArr


def pitchStrengthOneCandidate(f, L, pc):
    """Normalize the square root of spectrum "L" by applying normalized cosine kernal decaying as 1/sqrt(f)."""
    f = f.reshape((f.shape[0],1))
    f = np.real(f)
    L = np.real(L)
   
    n = np.fix(f[-1] / pc - 0.75)[0]
    if n==0:
        return np.NaN

    k = np.zeros(size(f))
    q = f[:,0] / pc

    primes = [1] + primes_method5(int(n))
    for i in (primes):
        a = abs(q - i)
        p = a < .25
        k[np.where(p)] = np.cos(2 * math.pi * q[np.where(p)])
        v = np.logical_and(.25 < a, a < .75)
        k[np.where(v)] += np.cos(2 * np.pi * q[np.where(v)]) / 2

    ff = np.divide(1, f)
    k = k.reshape((k.shape[0],1))
    k = np.multiply(k, np.sqrt(ff))
    k = k / np.linalg.norm(k[np.where(k>0.0)])
    S = np.matmul(k.T, L)
    return S


def hz2erbs(hz):
    """Converting hz to erbs."""
    erbs = 6.44 * (np.log2(229 + hz ) - 7.84)
    return erbs


def erbs2hz(erbs):
    """Converting erbs to hz."""
    hz = np.power(2, np.divide(erbs, 6.44) + 7.84) - 229
    return hz