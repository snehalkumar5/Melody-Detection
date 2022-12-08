import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3

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

        button1 = tk.Button(systemFrame, text="Play",
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
