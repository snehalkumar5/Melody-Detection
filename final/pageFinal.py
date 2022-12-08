import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3

class PageFinal(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recorded = False
        main = tk.Frame(self)
        main.configure(width=1055,height=1080,background='#c1ddc6')
        main.grid(row=0,column=0)

        titleFrame = tk.Frame(main)
        titleFrame.configure(width=500,height=100,background='#c1ddc6',padx=70,pady=80)
        titleFrame.grid(row=0,column=0)

        label = tk.Label(titleFrame, text="LET'S DO THE CONVERSATION IN RIGHT TONE", font=controller.title_font,bg='#c1ddc6',fg='#993300')
        label.grid(row=0,column=0)

        titleFrame2 = tk.Frame(main)
        titleFrame2.configure(width=500,height=100,background='#e4f0e6',pady=40)
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
                            command=lambda: controller.show_frame("PageStart"),padx=20,pady=15,bg='#ff99c8')
        button1.grid(row=1,column=1)
        button2 = tk.Button(buttonFrame, text="NO",
                            command=lambda: exit(),padx=20,pady=15,bg='#ff99c8')
        button2.grid(row=1,column=3)
