# plot libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk, ImageSequence

# GUI libraries
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

from src.robot import Robot
import firmware.servo as servo

class GUI:
    def __init__(self, root) -> None:
        # plot variables
        self.fig = plt.figure(figsize=(8, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')

        self.button_connection = ctk.StringVar()
        self.com_ports_var = ctk.StringVar()

        self.combobox = ctk.CTkComboBox(root, variable=self.com_ports_var)
        self.refresh_button = ctk.CTkButton(root, textvariable=self.button_connection, fg_color='red')
        self.refresh_com_button = ctk.CTkButton(root, text="Refresh COM Ports")
        self.button_compute = ctk.CTkButton(root, text="Compute", command=self.update_robot)

        self.entry_x = ctk.CTkEntry(root, width=200)
        self.entry_y = ctk.CTkEntry(root, width=200)
        self.entry_z = ctk.CTkEntry(root, width=200)

        # table
        self.coordinates_label = ctk.CTkLabel(root, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
        self.columns = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")

        self.robot = Robot()

        self.init(root)

    def init(self, root):
        # set window title
        root.title("Robot Arm Inverse Kinematics")
        # app theme
        ctk.set_appearance_mode("dark")  # Ustawienie ciemnego trybu
        ctk.set_default_color_theme("blue")  # Ustawienie domyślnego motywu kolorystycznego

        self.combobox.grid(row=1, column=1, padx=10, pady=10)
        self.refresh_button.grid(row=3, column=1, padx=10, pady=10)
        self.refresh_com_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # create input boxes
        ctk.CTkLabel(root, text="X:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_x.grid(row=1, column=0, padx=25, pady=10, sticky="w")
        ctk.CTkLabel(root, text="Y:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_y.grid(row=2, column=0, padx=25, pady=10, sticky="w")
        ctk.CTkLabel(root, text="Z:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.entry_z.grid(row=3, column=0, padx=25, pady=10, sticky="w")

        self.button_compute.grid(row=4, column=0, padx=50, pady=10, sticky="w")
        self.coordinates_label.grid(row=5, column=0, columnspan=2, padx=50, pady=10, sticky="w")

        # table with information about servos
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.grid(row=1, column=6, rowspan=5, columnspan=2, padx=10, pady=10, sticky='nsew')

        # plot for matplotlib
        canvas = FigureCanvasTkAgg(self.fig, master=root)
        canvas.get_tk_widget().grid(row=7, column=2, columnspan=10, padx=10, pady=10)
        canvas.draw()

    def init_plot(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.plot_robot(0, 0, 0, 0)

    def update_table_row(self, servo_id, voltage, current, temperature, pos, load):
        for row in self.tree.get_children():
            if int(self.tree.item(row, 'values')[0]) == servo_id:
                self.tree.item(row, values=(servo_id, voltage, current, temperature, pos, load))
                return
        self.tree.insert("", "end", values=(servo_id, voltage, current, temperature, pos, load))

    # ROBOT FUNCTIONS
    def update_robot(self, com):
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            z = float(self.entry_z.get())

            theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4 = self.robot.inverse_kinematics(x, y, z)

            if theta1 is not None:
                self.plot_robot(theta1, theta2, theta3, theta4)
                servo.move_to_position(com, pos1, pos2, pos3, pos4)
                self.fig.canvas.draw_idle()
        except ValueError:
            # NEED CORRECTION - THROWS ERROR:
                # `_tkinter.TclError: bad screen distance "100.0"`
            # CTkMessagebox(master=self.root,
            #             title="Error",
            #             message="Invalid input. Please enter valid numerical values.",
            #             icon="cancel",
            #             option_1="OK")
            print("Error occured, enter valid inputs.")

    def plot_robot(self, theta1, theta2, theta3, theta4):
        self.ax.cla()

        # calculate robot position
        points = self.robot.calc_pos(theta1, theta2, theta3, theta4)

        # draw lines for each arm
        self.ax.plot(points[:, 0], points[:, 1], points[:, 2], 'bo-', label='Links')
        self.ax.plot(self.robot.rx, self.robot.ry, self.robot.rz, 'ro', label='End-Effector')

        # color base
        self.ax.plot([0], [0], [0], 'go', label='Base')

        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_zlim(-200, 200)

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('3D Robot Arm')
        self.ax.legend(loc='lower left')

        # update label with new coordinates
        self.coordinates_label.configure(text=f"End-Effector Coordinates:\nX: {self.robot.rx:.2f}, Y: {self.robot.ry:.2f}, Z: {self.robot.rz:.2f}")
