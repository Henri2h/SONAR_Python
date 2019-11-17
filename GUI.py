# coding: utf-8
import matplotlib
matplotlib.use('TkAgg')
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
from matplotlib import cm

from tkinter import ttk
from tkinter import * 

import sonar

import time
import threading
import queue as Queue

class GUI:
    def __init__(self, master):
        self.master = master
        self.master['bg']='white'

        self.label = Label(self.master, text="SONAR")
        self.label.pack()

        self.p = PanedWindow(self.master, orient=HORIZONTAL)
        self.p.pack(side=TOP, expand=Y, fill=BOTH, pady=2, padx=2)
        #p.add(Label(p, text='Volet 1', background='blue', anchor=CENTER))


        # plot
        self.sn = sonar.sonar()
        myrecording, myrecording_time, amplitude, distance, n_start, n_stop = self.sn.getDistance()

        self.sn.setNumber(1)
        self.sn.setSpacing(500)

        self.fg = Figure()

        self.daxes_0 = self.fg.add_subplot(311)
        self.daxes_1 = self.fg.add_subplot(312)
        self.daxes_2 = self.fg.add_subplot(313)
        


        self.daxes_0.plot(myrecording_time, myrecording, label="Signal")
        self.daxes_0.set_ylim([-1,1])
        
        self.daxes_1.plot(myrecording_time[n_start:n_stop], myrecording[n_start:n_stop], label="Signal")
        self.daxes_1.set_ylim([-1,1])

        self.daxes_2.plot(distance, amplitude, label="Signal")

        self.daxes_0.set_title("Recording")
        self.daxes_0.set_xlabel("Temps (s)")

        self.daxes_1.set_title("Enregistrement (entre 0 et d mètres)")
        self.daxes_1.set_xlabel("Temps (s)")

        self.daxes_2.set_title("Amplitude en fonction de la distance")
        self.daxes_2.set_xlabel("Temps (s)")

        self.daxes_0.legend()
        self.daxes_1.legend()
        self.daxes_2.legend()

        self.fg.subplots_adjust(hspace=0.6)

        # create data array
        self.img = [amplitude]

        frameplot_signal = Frame(self.p, bg = "white")
        frameplot_signal.pack()
        self.p.add(frameplot_signal)


        self.canvas1 = FigureCanvasTkAgg(self.fg, master=frameplot_signal)
        self.toolbar1 = NavigationToolbar2Tk(self.canvas1, frameplot_signal)
        self.canvas1.get_tk_widget().pack()
        self.canvas1.draw()


        # image
        self.cmap = "inferno"
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        image = self.axes.imshow(self.img, cmap=self.cmap, aspect="auto")

        self.axes.set_title("Distance en  fonction du temps")
        self.axes.set_xlabel("Distance (m)")

        self.figure.colorbar(image, ax=self.axes, orientation='horizontal', fraction=.1)

        d = max(distance)/(len(amplitude)-1)
        print(d)
        ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x * d))
        self.axes.xaxis.set_major_formatter(ticks)

        frameplot = Frame(self.p, bg="white")
        frameplot.pack()
        self.p.add(frameplot)

        self.canvas2 = FigureCanvasTkAgg(self.figure, master=frameplot)
        self.toolbar2 = NavigationToolbar2Tk(self.canvas2, frameplot)
        self.canvas2.get_tk_widget().pack()
        self.canvas2.draw()


        self.p.pack()

        self.btRun = Button(self.master, text ='Lancer', command = self.run_exp)
        self.btRun.pack(side=LEFT, padx=5, pady=5)

        self.btRunOnce = Button(self.master, text ='Run once', command = self.run_exp_once)
        self.btRunOnce.pack(side=LEFT, padx=5, pady=5)

        Button(self.master, text ='Stoper').pack(side=RIGHT, padx=5, pady=5)

        self.shouldRecord = False
        self.btRun["bg"] = "red"

        self.started = False
        self.shouldUpdate = False


        # background client

        self.queue = Queue.Queue()
        self.threaded_task = ThreadedTask(self.queue, self.sn)
        self.threaded_task.start()

    # destroy the threaded task
    def kill(self):
        self.threaded_task.shouldRun = False
    
    def run_exp(self):
        if self.shouldRecord == False: # should update
            self.btRun["bg"] = "green"
            self.btRun["text"] = "Stop recording"
            self.shouldRecord = True
            self.threaded_task.changeState(True)
            self.shouldUpdate = True

            # check if update ui is launched
            if(self.started == False):
                self.update_ui()
                self.started =  True
        else:
            self.btRun["bg"] = "red"
            self.btRun["text"] = "Start recording"
            self.shouldRecord = False
            self.threaded_task.changeState(False)
            self.shouldUpdate = False
    
    def run_exp_once(self):
        data = self.sn.getDistance()
        self.queue.put(data)
        self.update_ui()

    # get distance and print it
    def getDistance(self):
        shouldPlot = False
        while(self.queue.empty() == False):
            data = self.queue.get(0)
            mrecord, mrecordtime, amplitude, distance, n_start, n_stop = data[0], data[1], data[2], data[3], data[4], data[5]
            
            shouldPlot = False # reset for the last one
            for k in range(len(amplitude)):
                if(amplitude[k] != 0): 
                    shouldPlot = True
                    self.img.append(amplitude) # should append only if different from 0
        
        
        
        if(shouldPlot): # if data is not empty (occur sometimes due to low level errors)

            self.axes.imshow(self.img, self.cmap, aspect="auto")
            
            self.daxes_0.clear()
            self.daxes_0.plot(mrecordtime, mrecord)
            self.daxes_1.clear()
            self.daxes_1.plot(mrecordtime[n_start:n_stop], mrecord[n_start:n_stop])

            self.daxes_2.clear()
            self.daxes_2.plot(distance, amplitude)
            
            self.canvas2.draw()
            self.canvas1.draw()
        else:
            print("Should not")

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            print("msg")
            # Show result of the task if needed
            self.prog_bar.stop()
        except Queue.Empty:
            self.master.after(100, self.process_queue)

    def update_ui(self):
        if(self.queue.empty() == False):
            self.getDistance()
            self.master.after(10, self.update_ui) # in anycase we want to empty the queue
        elif(self.shouldUpdate):
            self.master.after(10, self.update_ui)

        if(self.queue.full() == True):
            print("QUEUE FULL !!!!")


class ThreadedTask(threading.Thread):
    def __init__(self, queue, sn):
        threading.Thread.__init__(self)
        self.queue = queue
        self.sn = sn
        self.shouldRun = True
        self.shouldSend = False

    def changeState(self, shouldRun):
        self.shouldSend = shouldRun

    def run(self):
        while(self.shouldRun):
            # active state
            if(self.shouldSend):
                data = self.sn.getDistance()  # Simulate long running process
                if(self.queue.full() == True):
                    print("[ THEADED TASK ] : Queue full !!")
                else:
                    self.queue.put(data)

root = Tk()
root.title("Test Button")
main_ui = GUI(root)
root.mainloop()

main_ui.kill()
print("Program ended")