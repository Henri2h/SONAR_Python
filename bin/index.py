import sounddevice as sd
import serial
import numpy as np
import matplotlib.pyplot as plt

def f(t):
    print(t)
    return np.sin(2*3.14*t*4*480)*np.sin(2*3.14*t*40)
    return np.sin((2**t-1)/np.log(t))

fmin = 4*10**3
fmax = 16*10**3
T = 2*10**-3

def C(t):
    a = np.exp(((-1)*(3*t-T/2)**2)/T)
    b = np.sin(2*np.pi*(fmin*t + ((fmax-fmin)*t**2)/(2*T)))
    return b*a

file = open("Chirp.csv")
lines = file.readlines()

chirp, time = [], []
for i in range(1, len(lines)):
    lsplit = lines[i].split(",")
    chirp.append(float(lsplit[1]))
    time.append(float(lsplit[0]))

print("Hello, starting ...")
fs = 48000

# chrip
#er = np.linspace((-0.05,-0.05),(0.05,0.05), fs)
#chrip = C(er)

T = 100000
sound, s_time = [], []
for k in range(0, fs):
    s_time.append(k/fs)
    kmod = k%T
    
    if(kmod < len(chirp) and k//T < 5):
        sound.append(chirp[kmod])
    else:
        sound.append(0)

myrecording = sd.playrec(sound, fs, channels=1)
sd.wait()

print(len(s_time), len(sound))
print("Starting autocorelation")
sig = []

for k in range(len(myrecording)):
    s = []

    # print completion
    if(k%30 == 0):
        print(k/len(myrecording))

    for j in range(len(chirp)):
        if(j+k < len(myrecording)):
            s += abs(myrecording[j+k]*chirp[j])
    s /= len(chirp)
    sig.append(s)

plt.plot(s_time, sound)
plt.plot(s_time, myrecording)
plt.show()

print("Done")
plt.plot(s)
plt.show()