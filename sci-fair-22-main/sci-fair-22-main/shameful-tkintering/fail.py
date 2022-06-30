#Import the required Libraries

from tkinter import *
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

class Window:
    def __init__(self, title='CalligraphyCoin'):
        root = Tk()
        root.title(title)
        root.geometry('300x200+50+50')
        root.resizable(False, False)
        root.iconbitmap(r'C:\Users\trist\OneDrive\Documents\Code\sci-fair-22\shameful-tkintering\logo.ico')
        self.root = root
    def display_text(self, text2):
        Label(self.root, text=text2, wrap=WORD).pack()
    def go(self):
        self.root.mainloop()

bobby = Window()
bobby.display_text("hello, this is a lot of text that's really badly formatted")
bobby.go()
    