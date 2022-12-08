
import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3
from pageEasy import PageEasy
from pageFinal import PageFinal
from pageGoAhead import PageGoAhead
from pageHard import PageHard
from pageMedium import PageMedium
from pageTryAgain import PageTryAgain
from pageStart import PageStart


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
        for F in (PageFinal, PageStart, PageEasy, PageGoAhead,
         PageMedium, PageHard, PageTryAgain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PageStart")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def return_frame(self, page_name):
        frame = self.frames[page_name]
        return frame

if __name__ == "__main__":
    app = SampleApp()
    app.configure(background='#c1ddc6')
    app.geometry("1055x780")
    app.mainloop()