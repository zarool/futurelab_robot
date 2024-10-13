import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk, ImageSequence

import app.ui as ui
from app.plot import Plot
from app.conn import Communicator

COLUMNS_TEXT = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
COLUMNS_HEADER = ["Id", "Voltage", "Current", "Temperature", "Position", "Load"]

class App:
    def __init__(self) -> None:
        ########################
        ############## GUI CONST
        ctk.set_appearance_mode("dark")  # Ustawienie ciemnego trybu
        ctk.set_default_color_theme("blue")  # Ustawienie domyślnego motywu kolorystycznego

        self.root = ctk.CTk()  # Użycie CTk zamiast Tk
        self.root.title("Robot Arm Inverse Kinematics")
        self.root.geometry("1980x480+0+0")

        # navbar
        self.navbar = ctk.CTkFrame(self.root)
        self.navbar.grid(row=0, column=0, sticky="ew")

        ########################
        ################ OBJECTS
        self.communicator = Communicator()
        self.plot = Plot()

        ########################
        ########## GUI VARIABLES
        # status_torque, offset_1, offset_2, offset_3, offset_4, position_move_s, id_move_s,
        # com_ports_var
        # arduino_ports_var
        self.positions = self.communicator.get_positions()

        self.entry_x = 0
        self.entry_y = 0
        self.entry_z = 0

        self.tree = 0
        self.combo = 0
        self.frames = {}

        self.sliders = 0
        self.table = 0
        self.label_coord = 0

        self.btn_refresh = 0
        self.btn_conn = ctk.StringVar()
        self.com_ports = self.communicator.get_com_ports()

        self.combo_arduino = 0
        self.btn_refresh_arduino = 0
        self.btn_conn_arduino = ctk.StringVar()
        self.com_ports_arduino = self.communicator.get_com_ports()

    def gui(self):
        "Allocate buttons and objects on window"

        ########################
        ########## CREATE FRAMES (TABS ON NAVBAR)

        main_frame = ctk.CTkFrame(self.root)
        self.frames[main_frame] = main_frame

        data_frame = ctk.CTkFrame(self.root)
        self.frames[data_frame] = data_frame

        def show_frame(frame):
            for f in self.frames.values():
                f.grid_forget()
            frame.grid(row=1, column=0, sticky="nsew")

        button1 = ctk.CTkButton(self.navbar, text="Program", command=lambda: show_frame(main_frame))
        button1.grid(row=0, column=0, padx=5, pady=5)
        button2 = ctk.CTkButton(self.navbar, text="Dane", command=lambda: show_frame(data_frame))
        button2.grid(row=0, column=1, padx=5, pady=5)


        ########################
        ########## MAIN FRAME

        nr_1 = ui.slider(main_frame, 0, 5, 0, 4096, 10, 10, "1", "Pos", 1, self.communicator)
        nr_2 = ui.slider(main_frame, 1, 5, 0, 4096, 10, 10, "2", "Pos", 1, self.communicator)
        nr_3 = ui.slider(main_frame, 2, 5, 0, 4096, 10, 10, "3", "Pos", 1, self.communicator)
        nr_4 = ui.slider(main_frame, 3, 5, 0, 4096, 10, 10, "4", "Pos", 1, self.communicator)
        nr_5 = ui.slider(main_frame, 4, 5, 0, 4096, 10, 10, "5", "Pos", 1, self.communicator)
        nr_6 = ui.slider(main_frame, 5, 5, 0, 4096, 10, 10, "6", "Pos", 1, self.communicator)
        self.sliders = [nr_1, nr_2, nr_3, nr_4, nr_5, nr_6]

        for slider, position in zip(self.sliders, self.positions):
            slider.slider.set(position)
            slider.update_label(position)

        offset_1 = ui.text_gap(main_frame, 200, 0, 6, 60, 10, "e")
        offset_2 = ui.text_gap(main_frame, 200, 1, 6, 60, 10, "e")
        offset_3 = ui.text_gap(main_frame, 200, 2, 6, 60, 10, "e")
        offset_4 = ui.text_gap(main_frame, 200, 3, 6, 60, 10, "e")
        ui.text_label(main_frame, "Offset 1:", "Helvetica", 12, 0, 6, 10, 10, "w")
        ui.text_label(main_frame, "Offset 2:", "Helvetica", 12, 1, 6, 10, 10, "w")
        ui.text_label(main_frame, "Offset 3:", "Helvetica", 12, 2, 6, 10, 10, "w")
        ui.text_label(main_frame, "Offset 4:", "Helvetica", 12, 3, 6, 10, 10, "w")

        btn_change_variable = ui.button(main_frame, "Toggle torque", None, self.communicator.toggle_and_send_command, 2, 3, 10, 10)
        self.combo = ui.dropdown_list(main_frame, self.com_ports, "<<ComboboxSelected>>", self.on_combobox_select, 1, 1, 10, 10)
        self.combo.configure(self.com_ports)

        status_torque = ui.text_label(main_frame, "Status: " + str(self.communicator.toggle), "Helvetica", 12, 3, 3, 10, 10, "w")
        status_torque.configure("Status: " + str(self.communicator.toggle))


        ########################
        ########## PLOT DISPLAY

        ui.text_label(main_frame, "X:", "Helvetica", 12, 0, 0, 10, 10, "w")
        ui.text_label(main_frame, "Y:", "Helvetica", 12, 1, 0, 10, 10, "w")
        ui.text_label(main_frame, "Z:", "Helvetica", 12, 2, 0, 10, 10, "w")
        ui.text_label(main_frame,"ID","Helvetica", 12, 1, 2, 10, 10, None)
        ui.text_label(main_frame,"Position","Helvetica", 12, 1, 2, 10, 10, None)

        self.entry_x = ui.text_gap(main_frame, 200, 0, 0, 25, 10 ,"w")
        self.entry_y = ui.text_gap(main_frame, 200, 1, 0, 25, 10 ,"w")
        self.entry_z = ui.text_gap(main_frame, 200, 2, 0, 25, 10 ,"w")


        # canvas = FigureCanvasTkAgg(fig, master=main_frame)
        # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # canvas.draw()

        btn_compute = ui.button(main_frame,"Oblicz", None, update_robot, 3, 0, 50, 10,'w', None)
        btn_move = ui.button(main_frame, "Wykonaj", None, test, 2, 2, 10, 10, None, None)
        btn_transport = ui.button(main_frame, "Transport", None, servo.transport_mode, 0, 3, 10, 10, None, None)

        coordinates_label = ctk.CTkLabel(main_frame, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
        coordinates_label.grid(row=4, column=0, columnspan=2, padx=50, pady=10, sticky="w")

        ########################
        ########## CAMERA SECTION

        button_showcase = ui.button(main_frame, "Showcase", None, showcase_camera, 3, 4, 10, 10, None, None)

        ########################
        ########## CONNECTION SECTION

        id_move_s = ui.text_gap(main_frame, 200, 0, 2, 25, 10 ,"w")
        position_move_s = ui.text_gap(main_frame, 200, 1, 2, 25, 10 ,"w")

        refresh_button_ports_com = ui.button(main_frame,"Refresh COM Ports", None, refresh_com_ports, 2, 1, 10, 10, "w", None)
        refresh_button = ui.button(main_frame, None, self.btn_conn, self.communicator.refresh_connection_esp32, 3, 1, 10, 10)

        arduino_combobox = ui.dropdown_list(main_frame, self.com_ports_arduino, "<<ComboboxSelected>>", on_combobox_select_arduino, 1, 2, 10, 10)
        arduino_combobox.configure(self.com_ports_arduino)
        arduino_refresh_button_ports_com = ui.button(main_frame, "Refresh Arduino Ports", None, refresh_arduino_ports, 2, 2, 10, 10, "w", None)
        arduino_refresh_button = ui.button(main_frame, None, self.btn_conn_arduino, self.communicator.refresh_connection_arduino, 3, 2, 10, 10)


        ########################
        ########## DATA FRAME

        table = ui.table(data_frame, COLUMNS_TEXT, "headings", COLUMNS_HEADER, 160, 6, 16, 20, 20, 'nsew')

    def run(self):
        "Main run function, will start threads and functionality of app"

        self.gui()

        self.communicator.start_receive_data_thread(update_display)
        self.communicator.refresh_connection_esp32()
        self.plot.init_plot()

        self.root.after(100, self.update_table)
        self.root.mainloop()

    def update_table(self):
        pass

    def on_combobox_select(self):
        pass

    def event_handler(self):
        pass
