from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.interactive(True)


class Graph:

    def __init__(self, window, title="3D"):
        self.title = title
        self.angles = np.array([0, 0, 0])
        self.length = np.array([0, 0, 0])

        self.window = window

        # CANVAS
        self.fig = plt.figure(facecolor='none')
        self.ax = plt.axes(projection='3d')

        self.init_graph()

        self.fig.set_figwidth(7)
        self.fig.set_figheight(7)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.window)

    def init_graph(self):
        self.ax.set_xlabel('OX')
        self.ax.set_ylabel('OY')
        self.ax.set_zlabel('OZ')

        self.ax.set_xlim3d(left=-0.5, right=2)
        self.ax.set_ylim3d(bottom=-2, top=2)
        self.ax.set_zlim3d(bottom=0, top=3)
        self.ax.invert_zaxis()

        # stretching axes (change value (x, y, z))
        self.ax.set_box_aspect(aspect=(1, 1, 1))

    def plot_graph(self):
        # COORDINATES OF AXIS POINTS TO DRAW THEM
        p0 = np.array([0, 0, 0])

        p1 = np.array([0, 0, self.length[0]])
        p1 = p1 + p0

        p2 = self.convert(self.length[1], self.angles[0], self.angles[1])
        p2 = p2 + p1

        p3 = self.convert(self.length[2], self.angles[0], self.angles[2])
        p3 = p3 + p2

        # ax.plot([START_X, END_X], [START_Y, END_Y], zs=[START_Z, END_Z])
        self.ax.plot([p0[0], p1[0]], [p0[1], p1[1]], zs=[p0[2], p1[2]], color='black')
        self.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], zs=[p1[2], p2[2]], color='black')
        self.ax.plot([p2[0], p3[0]], [p2[1], p3[1]], zs=[p2[2], p3[2]], color='black')

        self.ax.scatter(p0[0], p0[1], p0[2], c='blue', marker='D')
        self.ax.scatter([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], [p1[2], p2[2], p3[2]], c='black', marker='h')

        # todo PLOT A GRIPPER

    def update_graph(self):
        self.ax.clear()
        self.init_graph()

        self.canvas.draw()
        self.toolbar.update()

    def add_graph(self):
        self.canvas.get_tk_widget().pack()
        self.canvas.get_tk_widget().pack()

    def update_values(self, angles, length):
        self.angles = angles
        self.length = length

    def theta_rotate(self, theta_index, angle):
        self.angles[theta_index] += angle
        self.update_graph()
        self.plot_graph()

    @staticmethod
    def convert(r, alpha, polar):
        # r is the Radius
        # alpha is the horizontal angle from the X axis
        # polar is the vertical angle from the Z axis

        point_x = r * np.sin(np.deg2rad(polar)) * np.cos(np.deg2rad(alpha))
        point_y = r * np.sin(np.deg2rad(polar)) * np.sin(np.deg2rad(alpha))
        point_z = r * np.cos(np.deg2rad(polar))

        return np.array([point_x, point_y, point_z])
