from tkinter import *
from tkinter import ttk

# Main Screen GUII
class MainScreen:
    def __init__(self, root) :
        # # Window Title
        root.title("Tyro GUI")
        mainframe = ttk.Frame(root, padding="5 5 10 10")
        root.columnconfigure(0,weight=1)
        root.rowconfigure(0, weight=1)



root = Tk()
MainScreen(root)
root.mainloop()