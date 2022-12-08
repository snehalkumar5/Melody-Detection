import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from scipy.io import loadmat

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
                            command= self.next_level,padx=20,pady=15,bg='#ff99c8')
        button1.grid(row=0,column=0)

    def next_level(self):
        frame = self.controller.return_frame(self.next_frame)
        if frame.next_level() == True:
            self.controller.show_frame(self.next_frame)
        else:
            return

    def plot(self,spkrFileName, parentFrame):
        self.next_frame = parentFrame
        expertGraphDir= '../expertGraphs/'
        speakerGraphDir= '../results/'
        strr = str(expertGraphDir) + str(spkrFileName) + '.mat'
        styPch = loadmat(strr)
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
