import sounddevice as sd
import serial
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker
from matplotlib import cm
import sonar

sn = sonar.sonar()
sn.setNumber(1)
sn.setSpacing(500)
myrecording, myrecording_time, amplitude, distance, start, end = sn.getDistance()


print("Done")

plt.ion()

fg, daxes = plt.subplots(3,1)

daxes[0].set_ylim([-1,1])

daxes[0].plot(myrecording_time, myrecording)
daxes[1].plot(myrecording_time[start:end], myrecording[start:end])
daxes[2].plot(distance, amplitude, label="Signal")

daxes[0].set_title("Recording")
daxes[1].set_title("Amplitude en fonction de la distance")
daxes[0].set_xlabel("Temps (s)")
daxes[1].set_xlabel("Temps (s)")
daxes[2].set_xlabel("Distance (s)")

daxes[0].legend()
daxes[1].legend()

img = [amplitude]



# image
cmap = "inferno"
fig, axes = plt.subplots()
image = axes.imshow(img, cmap=cmap, aspect="auto")
axes.set_title("Distance en  fonction du temps")
fig.colorbar(image, ax=axes, orientation='horizontal', fraction=.1)

d = max(distance)/len(amplitude)
ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * d))
axes.xaxis.set_major_formatter(ticks)

plt.show()
plt.pause(0.01)

for i in range(60):
    mrecord, mrecordtime, amplitude, distance, start, end = sn.getDistance()
    shouldPlot = False
    
    for k in range(len(amplitude)):
    	if(amplitude[k] != 0): 
            shouldPlot = True
    
    if(shouldPlot):
        img.append(amplitude)
        axes.imshow(img, cmap, aspect="auto")
        daxes[0].clear()
        daxes[0].plot(mrecordtime, mrecord)
        daxes[1].clear()
        daxes[1].plot(mrecordtime[start:end], mrecord[start:end])
        daxes[2].clear()
        daxes[2].plot(distance, amplitude)

        plt.draw()
        plt.pause(0.01)
    else:
        print("Should not")

print("End")
sleep(3)


