from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, title="Wizualizacja"):
        self.title = title

    def plot_graph(self, window):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.set_title('Wizualizacja')


        # PLOTTING
        # Data for a three-dimensional line
        zline = np.linspace(0, 15, 1000)
        xline = np.sin(zline)
        yline = np.cos(zline)
        ax.plot3D(xline, yline, zline, 'gray')

        # Data for three-dimensional scattered points
        zdata = 15 * np.random.random(100)
        xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
        ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
        ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens');

        # add graph to canvas
        self.show_graph(fig, window)

    @staticmethod
    def show_graph(fig, window):
        # plotting graph on tkinter canvas
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas, window)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack()
