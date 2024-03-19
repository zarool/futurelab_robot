from tkinter import *


class Window:
    def __init__(self, name: str = "Future Lab App", width: int = 500, height: int = 500):
        self.root = Tk()
        self.root.title(name)
        self.root.geometry(f'{width}x{height}')

    def __str__(self):
        return self

    def run(self):
        self.root.mainloop()
