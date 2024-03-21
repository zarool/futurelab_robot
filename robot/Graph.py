from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, title="3D"):
        self.title = title
        self.angles = np.array([75, 45, 35])
        self.length = np.array([1, 1, 1])

        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        self.ax.set_title(title)

        self.ax.set_xlabel('OX')
        self.ax.set_ylabel('OY')
        self.ax.set_zlabel('OZ')

        self.ax.set_xlim3d(left=-0.5, right=2)
        self.ax.set_ylim3d(bottom=-2, top=2)
        self.ax.set_zlim3d(bottom=-1, top=4)
        self.ax.invert_zaxis()

        # stretching axes (change value (x, y, z))
        self.ax.set_box_aspect(aspect=(1, 1, 1))

    @staticmethod
    def convert(angle, length):
        point_x = length * np.cos(np.deg2rad(angle))
        point_y = length * np.sin(np.deg2rad(angle))

        return np.array([point_x, point_y])

    def plot_graph(self, window):

        # TODO
        # 1 - DO BETTER HANDLING WITH POINTS
        # 2 - ADD 3D CONVERSION TO ADD ROTATION AROUND Z-AXIS
        # 3 - CONNECT ROBOT POSITION WITH GRAPH

        p0 = np.array([0, 0])
        p1 = self.convert(self.angles[0], self.length[0])
        p1 = p1 + p0
        p2 = self.convert(self.angles[1], self.length[1])
        p2 = p2 + p1
        p3 = self.convert(self.angles[2], self.length[2])
        p3 = p3 + p2

        # ax.plot([START_X, END_X], [START_Y, END_Y], zs=[START_Z, END_Z])
        self.ax.plot([p0[0], p1[0]], [0, 0], zs=[p0[1], p1[1]], color='black')
        self.ax.plot([p1[0], p2[0]], [0, 0], zs=[p1[1], p2[1]], color='black')
        self.ax.plot([p2[0], p3[0]], [0, 0], zs=[p2[1], p3[1]], color='black')

        # add graph to canvas
        self.show_graph(window)

    def show_graph(self, window):
        # plotting graph on tkinter canvas
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(self.fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
