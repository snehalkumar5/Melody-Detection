import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import os
import numpy as np
import pandas as pd
import signal
import sounddevice as sd
from scipy.io.wavfile import read
from scipy.io import loadmat
from playsound import playsound
from createSpeakerGraph import createSpeakerGraph
from computeScore import computeScore

class PageMedium(tk.Frame):
    def __init__(self, parent, controller):
        self.sysFileName,self.sysText,self.spkrFileName,self.spkrText = self.getNum("MEDIUM")
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
        button1 = tk.Button(buttonFrame111, text="Expert Audio",
                            command=lambda: playsound('../wav/'+self.spkrFileName+'.wav'),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame112, text="Submit",
                            command=lambda: self.submit(self.graphFrame),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)

        button1 = tk.Button(buttonFrame22, text="Exit",
                            command=lambda:  controller.show_frame("PageStart"),width=10,height=2,bg='#bad4f4')
        button1.grid(row=0,column=0)
        
        button1 = tk.Button(systemFrame, text="Play",
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

    def recordVoice(self):
        self.recorded = True
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
        c = np.reshape(np.array(a,dtype=np.float16),(1,a.shape[0]))
        np.save("../results/"+self.spkrFileName+".npy", c)
    
    def submit(self,window):
        done = createSpeakerGraph(self.spkrFileName+".wav")
        if done == 0:
            score = 0
        else:
            score = computeScore(self.spkrFileName+".wav")
        print('score:',score)
        self.score = score
        if score<0.01:
            frame = self.controller.return_frame("PageTryAgain")
            frame.plot(self.spkrFileName, "PageMedium")
            self.controller.show_frame("PageTryAgain")
        else:
            frame = self.controller.return_frame("PageGoAhead")
            frame.plot(self.spkrFileName, "PageMedium")
            self.controller.show_frame("PageGoAhead")

    def getNum(self, difficulty, flag=False):
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
        print(self.level - self.startlevel)
        if self.level - self.startlevel == 4:
            self.controller.show_frame("PageFinal")
            return False
        else:        
            self.sysFileName, self.sysText, self.spkrFileName, self.spkrText = self.getNum("MEDIUM", True)
            self.plot(self.graphFrame)
            self.syslabel.config(text = self.sysText)
            self.spkrlabel.config(text = self.spkrText)
            self.controller.show_frame("PageMedium")
            return True

    def plot(self,window):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass 
        expertGraphDir= '../expertGraphs/'
        strr = str(expertGraphDir) + str(self.spkrFileName) + '.mat'
        styPch = loadmat(strr)
        styPch = styPch['styPch']
        styPch = styPch[~np.isnan(styPch)]
        styPch = np.array(styPch).astype('float64')
        fig = Figure(figsize=(5, 4), dpi=70)
        maxPerEx= np.max(styPch)
        minPerEx= np.amin(styPch)
        yticks = np.array([minPerEx, maxPerEx])
        yticks = sorted(yticks)
        ax = fig.add_subplot(111)
        ax.set_title("What would be expected")
        ax.set_yticks(yticks, minor=False)
        print([str(round(t,2)) + 'x' for t in yticks])
        ax.set_yticklabels([str(round(t,2)) + 'x' for t in yticks], fontdict=None, minor=False)
        ax.plot(styPch, color='blue', label="Expert")
        self.canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)