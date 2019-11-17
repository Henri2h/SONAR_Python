import sounddevice as sd
from time import sleep
import numpy as np
import Chirp

class sonar:
    def __init__(self):
        # variable
        # constante
        self.v = 343 #vitesse du son dans l'air
        self.fs = 48000 # fréquence d'enregistrement

        self.n_start = self.fs//4
        self.n_stop = self.n_start + self.fs//4
        self.dmax = 4
        self.chirp_sig = self.getChirp()

        self.chirp_number = 1
        self.chirp_spacing = 500
        self.debug = False

        print("Sonar object created")
    
    def setNumber(self, i):
        self.chirp_number = i

    def setSpacing(self, i):
        self.chirp_spacing = i


    def getChirp(self):
        ch = Chirp.Chirp()
        return ch.getChirp()

    def createSound(self):
        sound, s_time = [], []
        i = 0
        
        
        for k in range(0, self.n_stop): # buffer
            s_time.append(k/self.fs)
            
            if(k >= self.n_start and k < self.n_stop and i < 1 + self.chirp_number):
                kmod = k%self.chirp_spacing
                if(kmod == 0):
                    i += 1
                if(kmod < len(self.chirp_sig)):
                    sound.append(self.chirp_sig[kmod])
                else:
                    sound.append(0.0)
            else:
                sound.append(0.0)
        return sound, np.array(s_time)

    def sendSoundAndRecord(self, sound):
        myrecording_n = sd.playrec(sound, self.fs, channels=1)
        sd.wait()
        return myrecording_n

    def correlationToDistance(self, recording):
        res_amplitude = []
        res_distance = []

        nrec = len(recording)
        ns = len(self.chirp_sig)

        k = 0
        
        while(k < nrec):
            s = 0
            j = 0
            while(j < ns*self.chirp_number):
                kmod = j//ns
                j_mod = j%ns
                if(k + j + kmod < nrec):
                    s += abs(self.chirp_sig[j_mod]*recording[j+k+kmod])
                j += 1
            s /= ns
            s = s*k#*k*k # compensation de la distance
            res_amplitude.append(s)
            res_distance.append(k/self.fs*self.v/2)
            k += 1
        
        return res_amplitude, res_distance

    def getDistance(self):
        sound, s_time = self.createSound()
        myrecording_n = self.sendSoundAndRecord(sound)
    
        if(self.debug):
            print("n_start :" , self.n_start)
        
        delaystart = self.n_start + 2500 # + 700
        myrecording = []
        s = 0
        a = 0.8
        S = []
        for k in range(len(myrecording_n)):
            s = myrecording_n[k][0] * a + (1-a)*s
            S.append(s)
            if(s>0.4 and delaystart == self.n_start + 2500 and k >= self.n_start): # valuer arbitraires après avoir regardé sur un graph
                delaystart = k - 50
                #print("true", k)

            myrecording.append(myrecording_n[k][0])
        if(self.debug):
            print("Delaystart", delaystart)
        #plt.plot(S)
        #plt.show()


        # remove start
        # on vas modifier l'enregistrement pour commencer au lancement du signal et jusqu'à 10m donc tmax = d/2v
        sample_max = min(int(2*self.dmax/self.v*self.fs), self.n_stop-self.n_start) # avoid going out
        myrecording_cor = myrecording[delaystart:delaystart+sample_max]
        
        #myrecording_time = s_time[delaystart:delaystart+sample_max] - s_time[delaystart]
        myrecording_time = s_time - s_time[delaystart]

        s_time = s_time[self.n_start:self.n_stop]
        sound = sound[self.n_start:self.n_stop]
        
        amplitude, distance = self.correlationToDistance(myrecording_cor) 
        # return
        if(self.debug):
            print("len Amplitude : ", len(amplitude), "recording :", len(myrecording), self.n_stop,self.n_start, self.n_stop-self.n_start)
        return myrecording, myrecording_time, amplitude, distance, delaystart, delaystart+sample_max

   

   
