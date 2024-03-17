from tkinter import *


def plot():
    print("SSSS")


class Window:
    def __init__(self, name: str = "Future Lab App", width: int = 500, height: int = 500):
        self.root = Tk()
        self.root.title(name)
        self.root.geometry(f'{width}x{height}')

    def __str__(self):
        return self

    def show(self):
        # button that displays the plot
        plot_button = Button(master=self.root,
                             command=plot,
                             height=2,
                             width=10,
                             text="Plot")

        plot_button.pack()

        self.root.mainloop()
