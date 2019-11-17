import sounddevice as sd
import serial
import numpy as np
import matplotlib.pyplot as plt
import Chirp
v = 343
ch = Chirp.Chirp()

print("Start")
chirp_sig = ch.getChirp()

fs = 48000

n_start = fs*1
n_stop = fs*2

def createSound(chirp_sig, fs, n_start, n_stop):
    sound, s_time = [], []
    i = 0
    T = 800
    
    for k in range(0, 5*fs):
        s_time.append(k/fs)
        
        if(k >= n_start and k < n_stop and i < 6):
            kmod = k%T
            if(kmod == 0):
                i += 1
            if(kmod < len(chirp_sig)):
                sound.append(chirp_sig[kmod])
            else:
                sound.append(0.0)
        else:
            sound.append(0.0)
    return sound, s_time

def sendSoundAndRecord(sound, fs):
    myrecording_n = sd.playrec(sound, fs, channels=1)
    sd.wait()
    return myrecording_n

def correlationToDistance(myrecording, chirp_sig, fs):
    res_amplitude = []
    res_distance = []

    nrec = len(myrecording)
    nrec_stop = min(nrec, fs*10//v)

    k = 0
    while(k < nrec_stop):
        # print completion
        if(k%3000 == 0):
            print(k/nrec_stop)
        
        s = 0
        ns = len(chirp_sig)
        for j in range(ns):
            if(k + j < nrec_stop):
                s += abs(chirp_sig[j]*myrecording[j+k])
        s /= ns

        res_amplitude.append(s)
        res_distance.append(k/fs*v)
        k += 1
    return res_amplitude, res_distance

def getDistance(chirp_sig):

    sound, s_time = createSound(chirp_sig, fs, n_start, n_stop)
    myrecording_n = sendSoundAndRecord(sound, fs)

    delaystart = n_start
    myrecording = []

    for k in range(len(myrecording_n)):
        if(myrecording_n[k][0]>0.6 and delaystart == 0 and k >= n_start and False):
            delaystart = k

        myrecording.append(myrecording_n[k][0])

    # remove start

    s_time = s_time[n_start:n_stop]
    sound = sound[n_start:n_stop]
    myrecording = myrecording[delaystart:delaystart+n_stop-n_start]

    return correlationToDistance(myrecording, chirp_sig, fs)    

amplitude, distance = getDistance(chirp_sig)

#plt.plot(s_time, sound, label="Sound")
#plt.plot(s_time, myrecording, label="My recording")
#plt.legend()
#plt.show()

print("Done")

plt.plot(distance, amplitude, label="Sig2")
plt.legend()
plt.show()



