
import os
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
import pandas as pd
import numpy as np
import scipy.io
import subprocess
from sys import platform
import queue, threading, sys, time
import sounddevice as sd
import soundfile as sf
from playsound import playsound
import signal
from scipy.io.wavfile import write, read
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from createSpeakerGraph import createSpeakerGraph
from computeScore import computeScore

q = queue.Queue()
recorder = False
difficulty = "NULL"
subtype = 'PCM_16'
dtype = 'int16' 

def rec(f):
    with sf.SoundFile(f, mode='w', samplerate=16000, 
                      subtype=subtype, channels=1) as file:
        with sd.InputStream(samplerate=16000.0, dtype=dtype, 
                            channels=1, callback=save):
            while getattr(recorder, "record", True):
                file.write(q.get())

def save(indata, frames, time, status):
    q.put(indata.copy())

def start(f):
    global recorder
    recorder = threading.Thread(target=rec(f))
    recorder.record = True
    recorder.start()

def stop():
    global recorder
    recorder.record = False
    recorder.join()
    recorder = False

def getNum(difficulty, flag=False):
    print(difficulty)
    df = pd.read_csv(difficulty+'.csv')
    a=len(df)
    i = 1
    if(a==20):
        b = np.random.permutation(4)
    else:
        b= np.random.permutation(6)
    if b[0]==0 :
        i = 0
    else:
        if b[0]==1:
            i = 5
        else:
            if b[0]==2:
                i=10
            else:
                if b[0]==3:
                    i=15
                else:
                    if b[0]==4:
                        i=20
                    else:
                        i=25
    if flag:
        return str(df.loc[i+1,'sysFileName']),df.loc[i+1,'sysText'],str(df.loc[i+1,'spkrFileName']),df.loc[i+1,'spkrText']
    else:
        return str(df.loc[i,'sysFileName']),df.loc[i,'sysText'],str(df.loc[i,'spkrFileName']),df.loc[i,'spkrText']
        

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='arial', size=30, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self,bg='#c1ddc6')
        container.pack(expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.container = container
        self.frames = {}
        for F in (PageFinal, StartPage, PageEasy, PageGoAhead
        #  PageMedium, PageHard, 
        #  PageTryAgain
         ):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def return_frame(self, page_name):
        frame = self.frames[page_name]
        return frame

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="SPEAK TO ME IN THE RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: controller.show_frame("PageEasy"),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=2,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=lambda: controller.show_frame("PageEasy"),width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: controller.show_frame("PageEasy"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=1)


        buttonFrame = tk.Frame(main)
        buttonFrame.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame.grid(row=2,column=0)
        label = tk.Label(buttonFrame, text="Choose Level", font=tkfont.Font(family='arial', size=20, weight="bold"),pady=30,bg='#c1ddc6')
        label.grid(row=0,column=3)
        button1 = tk.Button(buttonFrame, text="EASY",
                            command=lambda: controller.show_frame("PageEasy"),padx=20,pady=15,bg='#bad4f4')
        button1.grid(row=1,column=1)
        button2 = tk.Button(buttonFrame, text="MEDIUM",
                            command=lambda: controller.show_frame("PageMedium"),padx=20,pady=15,bg='#bad4f4')
        button2.grid(row=1,column=3)
        button3 = tk.Button(buttonFrame, text="HARD",
                            command=lambda: controller.show_frame("PageHard"),padx=20,pady=15,bg='#bad4f4')
        button3.grid(row=1,column=5)

        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

class PageEasy(tk.Frame):

    def submit(self,window):
        frame = self.controller.return_frame("PageGoAhead")
        frame.plot(self.spkrFileName)
        # self.spkrFileName = "141"
        self.controller.show_frame("PageGoAhead")
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')


        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        # if platform == "linux" or platform == "linux2":
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        # else:
            # self.p = subprocess.Popen(["python","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        # if platform == "linux" or platform == "linux2":
        p.send_signal(signal.SIGINT)
        # else:
            # p.send_signal(signal.CTRL_C_EVENT)
        p.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        # print(a.shape)
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)
    
    def getNum(self, difficulty, flag=False):
        # print(difficulty)
        df = pd.read_csv(difficulty+'.csv')
        a=len(df)
        i = 1
        if(a==20):
            b = np.random.permutation(4)
        else:
            b= np.random.permutation(6)
        if b[0]==0 :
            i = 0
        else:
            if b[0]==1:
                i = 5
            else:
                if b[0]==2:
                    i=10
                else:
                    if b[0]==3:
                        i=15
                    else:
                        if b[0]==4:
                            i=20
                        else:
                            i=25
        if flag:
            self.level+=1
        else:
            self.level = i
            self.startlevel = i
        return str(df.loc[self.level,'sysFileName']),df.loc[self.level,'sysText'],str(df.loc[self.level,'spkrFileName']),df.loc[self.level,'spkrText']
    
    def next_level(self):
        print(self.level)
        self.plot(self.graphFrame)
        if self.level - self.startlevel == 5:
            self.controller.show_frame("PageFinal")
            return
        
        self.sysFileName, self.sysText, self.spkrFileName, self.spkrText = self.getNum("EASY", True)
        print(self.sysText)
        self.syslabel.config(text = self.sysText)
        self.spkrlabel.config(text = self.spkrText)
        self.controller.show_frame("PageEasy")
    
    def __init__(self, parent, controller):
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = self.getNum("EASY")
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        self.syslabel = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        self.syslabel.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        self.graphFrame = tk.Frame(baseFrame)
        self.graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        self.graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame111, text="PLAY",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame112, text="SUBMIT",
                            command=lambda: self.submit(self.graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="EXIT",
                            command=lambda:  controller.show_frame("StartPage"),width=10,height=2,bg='#bad4f4')
                            # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                            command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=0)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=self.next_level
                                ,width=10,height=2,bg='#c91616')
            button1.grid(row=1,column=0)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        self.spkrlabel = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        self.spkrlabel.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(self.graphFrame)

class PageMedium(tk.Frame):
   
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')


        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
      
      
    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    
    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        # print(a.shape)
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)


    def __init__(self, parent, controller):
        global difficulty
        difficulty = "MEDIUM"
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("MEDIUM", 0)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.score = 100
        self.recorded = False
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame111, text="PLAY",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame112, text="SUBMIT",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="EXIT",
                            command=lambda:  controller.show_frame("StartPage"),width=10,height=2,bg='#bad4f4')
                            # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                            command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=1)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig1"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=1)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)
        # button.pack()
class PageHard(tk.Frame):
    def submit(self,window):
        # self.spkrFileName = "141"
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')


        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        # try:
        os.remove("../results/"+self.spkrFileName+".wav")
        # except:
            # pass
        if platform == "linux" or platform == "linux2":
            self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        else:
            self.p = subprocess.Popen(["python","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        if platform == "linux" or platform == "linux2":
            p.send_signal(signal.SIGINT)
        else:
            p.send_signal(signal.CTRL_C_EVENT)
        p.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        # print(a.shape)
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)
        
    def __init__(self, parent, controller):
        global difficulty
        difficulty = "HARD"
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("HARD", 0)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame111, text="PLAY",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame112, text="SUBMIT",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame22, text="EXIT",
                            command=lambda:  controller.show_frame("StartPage"),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                            command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=1)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig1"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=1)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)
        # button.pack()

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        # print(a.shape)
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

class PageFinal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        main = tk.Frame(self)
        main.configure(width=1055,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6',padx=70,pady=100)
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)

        titleFrame2 = tk.Frame(main)
        titleFrame2.configure(width=500,height=100,background='#e4f0e6',pady=50)
        titleFrame2.grid(row=1,column=0)

        label = tk.Label(titleFrame2, text="CONGRATS !!!!! YOU'RE AN", font=tkfont.Font(family='arial', size=40, weight="bold"),bg='#e4f0e6',fg='black',)
        label.grid(row=0,column=0)

        titleFrame3 = tk.Frame(main)
        titleFrame3.configure(width=500,height=100,background='#e4f0e6',pady=25,padx=150)
        titleFrame3.grid(row=2,column=0)

        label = tk.Label(titleFrame3, text="EXPERT NOW :)", font=tkfont.Font(family='arial', size=40, weight="bold"),bg='#e4f0e6',fg='black',)
        label.grid(row=0,column=0)

        buttonFrame = tk.Frame(main)
        buttonFrame.configure(width=500,height=300,background='#c1ddc6',pady=65)
        buttonFrame.grid(row=3,column=0)
        label = tk.Label(buttonFrame, text="WANT TO PLAY AGAIN ??", font=tkfont.Font(family='arial', size=20, weight="bold"),pady=30,bg='#c1ddc6')
        label.grid(row=0,column=2)
        button1 = tk.Button(buttonFrame, text="YES",
                            command=lambda: controller.show_frame("PageEasy"),padx=20,pady=15,bg='#ff99c8')
        button1.grid(row=1,column=1)
        button2 = tk.Button(buttonFrame, text="NO",
                            command=lambda: controller.show_frame("PageMedium"),padx=20,pady=15,bg='#ff99c8')
        button2.grid(row=1,column=3)

class PageTryAgain(tk.Frame):
    def update_file(self, filename):
        self.spk

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.spkrFileName = ""
        self.controller = controller
        self.recorded = False
        main = tk.Frame(self)
        main.configure(width=1055,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6',padx=70,pady=50)
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)

        titleFrame2 = tk.Frame(main)
        titleFrame2.configure(width=500,height=100,background='#e4f0e6',pady=30)
        titleFrame2.grid(row=1,column=0)
        
        label = tk.Label(titleFrame2, text="OOPS !! TRY AGAIN :(", font=tkfont.Font(family='arial', size=30, weight="bold"),bg='#e4f0e6',fg='black',)
        label.grid(row=0,column=0)

        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)
        
        buttonFrame = tk.Frame(main)
        buttonFrame.configure(width=500,height=300,background='#c1ddc6',pady=20)
        buttonFrame.grid(row=2,column=0)
        # ax.plot(styPch, color='blue', label="Expert")
        
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What you have said (Red)")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='red', label="Expert")

        self.canvas = FigureCanvasTkAgg(fig, master=buttonFrame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        buttonFrame = tk.Frame(main)
        buttonFrame.configure(width=500,height=300,background='#c1ddc6',pady=60)
        buttonFrame.grid(row=3,column=0)
        button1 = tk.Button(buttonFrame, text="OK",
                            command=lambda: controller.show_frame("PageEasy"),padx=20,pady=15,bg='#ff99c8')
        button1.grid(row=0,column=0)

class PageGoAhead(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        main = tk.Frame(self)
        main.configure(width=1055,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6',padx=70,pady=50)
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)

        titleFrame2 = tk.Frame(main)
        titleFrame2.configure(width=500,height=100,background='#e4f0e6',pady=30)
        titleFrame2.grid(row=1,column=0)
        
        label = tk.Label(titleFrame2, text="GO AHEAD !!!", font=tkfont.Font(family='arial', size=30, weight="bold"),bg='#e4f0e6',fg='black',)
        label.grid(row=0,column=0)

        self.graphFrame = tk.Frame(main)
        self.graphFrame.configure(width=500,height=300,background='#c1ddc6',pady=20)
        self.graphFrame.grid(row=2,column=0)
        # ax.plot(styPch, color='blue', label="Expert")

        buttonFrame = tk.Frame(main)
        buttonFrame.configure(width=500,height=300,background='#c1ddc6',pady=60)
        buttonFrame.grid(row=3,column=0)
        button1 = tk.Button(buttonFrame, text="OK",
                            command=lambda: controller.show_frame("PageEasy"),padx=20,pady=15,bg='#ff99c8')
        button1.grid(row=0,column=0)

    def plot(self,spkrFileName):
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0
        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 

        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=self.graphFrame)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

class Gamefig1(tk.Frame):

    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)
    def next_frame(self):
        controller.show_frame("Gamefig2")
    def __init__(self, parent, controller, difficulty):
        self.level = 0
        self.difficulty = "EASY"
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("EASY", 1)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=0)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("Gamefig2"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=1)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=self.next_frame(),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=1)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig1Medium(tk.Frame):

    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("MEDIUM", 1)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=0)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("Gamefig2"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=1)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig2"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=1)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)
class Gamefig1Hard(tk.Frame):

    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("HARD", 1)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=0)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("Gamefig2"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=1)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig2"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=1)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig2(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("EASY", 2)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig3"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)


class Gamefig2(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("MEDIUM", 2)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig3"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)


class Gamefig2(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("HARD", 2)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig3"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)


class Gamefig3(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("EASY", 3)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig4"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig3(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("MEDIUM", 3)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig4"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig3(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("HARD", 3)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("Gamefig4"),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)


class Gamefig4(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("EASY", 4)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("PageFinal"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig4(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("MEDIUM", 4)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("PageFinal"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)

class Gamefig4(tk.Frame):
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'

        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')

        expertPattern= styPch
    
        strr = str(speakerGraphDir) + str(self.spkrFileName) + '.npy'
        styPch = np.load(strr)
        maxPer= np.max(styPch)
        minPer= np.amin(styPch)
        normPch= 0

        speakerPattern= styPch

        expertPattern = expertPattern[np.logical_not(np.isnan(expertPattern))]
        maxPerEx= np.max(expertPattern)
        minPerEx= np.amin(expertPattern)
        speakerPattern = speakerPattern[np.logical_not(np.isnan(speakerPattern))]
        
        yticks = np.array([minPer,normPch, maxPer, minPerEx, maxPerEx])
        yticks = sorted(yticks)
        fig = Figure(figsize=(5, 4), dpi=70)
        ax = fig.add_subplot(111)

        
        ax.plot(styPch, color='blue', label="Expert")
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(expertPattern, color='blue', label="Expert")
        ax.plot(speakerPattern, color='green', label="Speaker")
        ax.set_title("What you said (Green)")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = scipy.io.loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        # yticks = np.array([minPerEx,0, maxPerEx])
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def recordVoice(self):
        self.recorded = True
        fs=16000
        try:
            os.remove("../results/"+self.spkrFileName+".wav")
        except:
            pass
        self.p = subprocess.Popen(["python3","./soundrec.py", "../results/"+str(self.spkrFileName)+".wav"])
        sd.wait()

    def stopRecordVoice(self):
        p = self.p
        p.send_signal(signal.SIGINT)
        sd.wait()
        s,a = read("../results/"+self.spkrFileName+".wav")
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)

    def __init__(self, parent, controller):
        global difficulty
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = getNum("HARD", 4)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        self.score = 100
        main = tk.Frame(self)
        main.configure(width=1000,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6')
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)
        
        dialogueFrame = tk.Frame(main)
        dialogueFrame.configure(width=1000,height=400,bg='#c1ddc6')
        dialogueFrame.grid(row=1,column=0)
        
        systemFrame = tk.Frame(dialogueFrame)
        systemFrame.configure(background='#e4f0e6',width=500,height=400,pady=10)
        systemFrame.grid(row=0,column=0)
        label = tk.Label(systemFrame, text="System", font=tkfont.Font(family='arial', size=10, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=0,column=0)

        label = tk.Label(systemFrame, text=self.sysText, font=tkfont.Font(family='arial', size=13, weight="bold"),bg='#e4f0e6',width=50, height=5)
        label.grid(row=1,column=0)

        baseFrame = tk.Frame(main)
        baseFrame.configure(width=1000,height=300,bg='#c1ddc6')
        baseFrame.grid(row=2,column=0)
        buttonFrame22 = tk.Frame(baseFrame)
        buttonFrame22.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame22.grid(row=0,column=2)
        graphFrame = tk.Frame(baseFrame)
        graphFrame.configure(width=700,height=300,bg='#c1ddc6',padx=20)
        graphFrame.grid(row=0,column=1)
        buttonFrame11 = tk.Frame(baseFrame)
        buttonFrame11.configure(width=100,height=300,bg='#c1ddc6')
        buttonFrame11.grid(row=0,column=0)
        buttonFrame111 = tk.Frame(buttonFrame11)
        buttonFrame111.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame111.grid(row=0,column=0)
        buttonFrame112 = tk.Frame(buttonFrame11)
        buttonFrame112.configure(width=50,height=120,bg='#c1ddc6',pady=20)
        buttonFrame112.grid(row=1,column=0)
        button1 = tk.Button(buttonFrame22, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#2cfc03')
        button1.grid(row=0,column=1)

        button1 = tk.Button(buttonFrame22, text="Submit",
                            command=lambda: self.submit(graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=2,column=1)

        if self.score < 0.01:
            button1 = tk.Button(buttonFrame22, text="Try Again",
                                command=lambda:  controller.show_frame("PageTryAgain"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#c91616')
            button1.grid(row=2,column=2)
        else:
            button1 = tk.Button(buttonFrame22, text="Next",
                                command=lambda:  controller.show_frame("PageFinal"),width=10,height=2,bg='#c91616')
                                # command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4')
            button1.grid(row=2,column=2)
        button1 = tk.Button(systemFrame, text="PLAY",
                            command=lambda: playsound('../wav/'+self.sysFileName+'.wav'),width=10,height=2,bg='#bad4f4',pady=3)
        button1.grid(row=3,column=0)

        spaceFrame = tk.Frame(dialogueFrame)
        spaceFrame.configure(background='#c1ddc6',width=20,height=360)
        spaceFrame.grid(row=0,column=1)

        youFrame = tk.Frame(dialogueFrame)
        youFrame.configure(background='#e4f0e6',width=480,height=400,pady=10)
        youFrame.grid(row=0,column=3)
        label = tk.Label(youFrame, text="You", font=tkfont.Font(family='arial', size=10, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=0,column=0)

        label = tk.Label(youFrame, text=self.spkrText, font=tkfont.Font(family='arial', size=13, weight="bold"),width=50, height=5,bg='#e4f0e6')
        label.grid(row=1,column=0)

        buttonFrame1 = tk.Frame(youFrame)
        buttonFrame1.configure(width=500,height=300,bg='#e4f0e6')
        buttonFrame1.grid(row=3,column=0)
        buttonFrame12 = tk.Frame(buttonFrame1)
        buttonFrame12.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame12.grid(row=0,column=0)
        buttonFrame11 = tk.Frame(buttonFrame1)
        buttonFrame11.configure(width=120,height=300,bg='#e4f0e6',padx=10)
        buttonFrame11.grid(row=0,column=1)
        button1 = tk.Button(buttonFrame12, text="Start Recording",
                            command=self.recordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        button1 = tk.Button(buttonFrame12, text="Stop Recording",
                            command=self.stopRecordVoice,width=12,height=2,bg='#bad4f4')
        button1.grid(row=0,column=1)
        button2 = tk.Button(buttonFrame11, text="Listen",
                            command=lambda: playsound("../results/"+self.spkrFileName+".wav"),width=10,height=2,bg='#bad4f4')
        button2.grid(row=0,column=2)


        buttonFrame4 = tk.Frame(main)
        buttonFrame4.configure(width=1000,height=300,bg='#c1ddc6')
        buttonFrame4.grid(row=3,column=0)

        self.plot(graphFrame)


if __name__ == "__main__":
    app = SampleApp()
    app.configure(background='#c1ddc6')
    app.geometry("1055x780")
    app.mainloop()