from tkinter import *
from robot.Graph import Graph


class Window:
    def __init__(self, name: str = "Future Lab App", width: int = 500, height: int = 500):
        self.root = Tk()
        self.root.title(name)
        self.root.geometry(f'{width}x{height}')

        self.graph = Graph(self.root)
        self.graph.add_graph()

        self.inc = 5

    def run(self):
        self.graph.plot_graph()

        buttons_data = [
            {"label": "Rotate theta0 +", "command": lambda: self.graph.theta_rotate(0, self.inc)},
            {"label": "Rotate theta0 -", "command": lambda: self.graph.theta_rotate(0, -self.inc)},
            {"label": "Rotate theta1 +", "command": lambda: self.graph.theta_rotate(1, self.inc)},
            {"label": "Rotate theta1 -", "command": lambda: self.graph.theta_rotate(1, -self.inc)},
            {"label": "Rotate theta2 +", "command": lambda: self.graph.theta_rotate(2, self.inc)},
            {"label": "Rotate theta2 -", "command": lambda: self.graph.theta_rotate(2, -self.inc)}
        ]

        for index, btn in enumerate(buttons_data):
            button = Button(self.root, text=btn["label"], command=btn["command"])
            button.pack(side=LEFT, padx=5, pady=5)

        self.root.mainloop()

    def update(self, angles, length):
        self.graph.update_values(angles, length)
