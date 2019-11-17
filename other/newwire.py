import sounddevice as sd
import Chirp
import numpy as np
import matplotlib.pyplot as plt

duration = 0.5  # seconds

chip = Chirp.Chirp()
chirpList = chip.getChirp2()
zer = np.zeros((4000,2)) 
i = 0
L = []
def callback(indata, outdata, frames, time, status):
    global i, chirpList, zer, L
    print(frames)
    outdata[:] = zer[:frames]
    if status:
        print(status)
    if(i < len(chirpList)):
        nmin = min(frames, len(chirpList))
        outdata[i:nmin] = chirpList[i:nmin]
    i += frames
    if(i > 20000 and False):
        i = 0
    
    for d in indata:
        L.append(d)

with sd.Stream(channels=2, callback=callback):
    sd.sleep(int(duration * 1000))
    plt.plot(L)
    plt.show()