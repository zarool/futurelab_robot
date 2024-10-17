import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
        # offset_1, offset_2, offset_3, offset_4, position_move_s, id_move_s,
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

        self.status_torque = 0

        self.btn_refresh = 0
        self.btn_conn = ctk.StringVar()
        self.com_ports = self.communicator.get_com_ports()

        self.combo_arduino = 0
        self.btn_refresh_arduino = 0
        self.btn_conn_arduino = ctk.StringVar()
        self.com_ports_arduino = self.communicator.get_com_ports()

        # testing
        self.id_move_s = 0
        self.position_move_s = 0

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

        btn_change_variable = ui.button(main_frame, "Toggle torque", None, lambda: self.communicator.toggle_and_send_command(self.status_torque), 2, 3, 10, 10)
        self.combo = ui.dropdown_list(main_frame, self.com_ports, "<<ComboboxSelected>>", self.on_combobox_select, 1, 1, 10, 10)
        self.combo.configure(self.com_ports)

        self.status_torque = ui.text_label(main_frame, "Status: " + str(self.communicator.toggle), "Helvetica", 12, 3, 3, 10, 10, "w")
        self.status_torque.configure("Status: " + str(self.communicator.toggle))


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

        canvas = FigureCanvasTkAgg(self.plot.fig, master=main_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()

        btn_compute = ui.button(main_frame,"Oblicz", None, self.communicator.update_robot, 3, 0, 50, 10,'w', None)
        btn_move = ui.button(main_frame, "Wykonaj", None, self.communicator.test, 2, 2, 10, 10, None, None)
        btn_transport = ui.button(main_frame, "Transport", None, self.communicator.transport_mode, 0, 3, 10, 10, None, None)

        self.label_coord = ctk.CTkLabel(main_frame, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
        self.label_coord.grid(row=4, column=0, columnspan=2, padx=50, pady=10, sticky="w")
        
        ########################
        ########## CAMERA SECTION

        button_showcase = ui.button(main_frame, "Showcase", None, self.communicator.showcase_camera, 3, 4, 10, 10, None, None)

        ########################
        ########## CONNECTION SECTION

        self.id_move_s = ui.text_gap(main_frame, 200, 0, 2, 25, 10 ,"w")
        self.position_move_s = ui.text_gap(main_frame, 200, 1, 2, 25, 10 ,"w")

        refresh_button_ports_com = ui.button(main_frame,"Refresh COM Ports", None, self.refresh_com_ports, 2, 1, 10, 10, "w", None)
        self.btn_refresh = ui.button(main_frame, None, self.btn_conn, self.refresh_connection_esp32, 3, 1, 10, 10)

        self.combo_arduino = ui.dropdown_list(main_frame, self.com_ports_arduino, "<<ComboboxSelected>>", self.on_combobox_select_arduino, 1, 2, 10, 10)
        self.combo_arduino.configure(self.com_ports_arduino)
        arduino_refresh_button_ports_com = ui.button(main_frame, "Refresh Arduino Ports", None, self.refresh_arduino_ports, 2, 2, 10, 10, "w", None)
        self.btn_refresh_arduino = ui.button(main_frame, None, self.btn_conn_arduino, self.refresh_connection_arduino, 3, 2, 10, 10)

        ########################
        ########## DATA FRAME

        self.table = ui.table(data_frame, COLUMNS_TEXT, "headings", COLUMNS_HEADER, 160, 6, 16, 20, 20, 'nsew')

    def run(self):
        "Main run function, will start threads and functionality of app"

        self.gui()

        self.communicator.start_receive_data_thread(self.update_display)
        self.refresh_connection_esp32()
        
        self.label_coord.configure(text=f"End-Effector Coordinates:\nX: {self.plot.rx:.2f}, Y: {self.plot.ry:.2f}, Z: {self.plot.rz:.2f}")

        self.root.after(100, self.update_table)
        self.root.mainloop()

    def update_table(self):
        pass

    def update_display(self, servo_id, voltage, current, temperature, pos, load):
        data = (servo_id, f"{voltage:.1f}V", f"{current:.1f}A", f"{temperature:.1f}C", pos, f"{load:.1f}N")
        self.table.insert_or_update(servo_id, values=data)

###################################
####### test
    def thetas_to_0(self):
        self.plot.plot_robot(0,-3.14,1,1)

###################################
####### esp32 connection

    def on_combobox_select(self):
        selected_port = self.combo.get()
        print(f"Selected COM port: {selected_port}")
        self.communicator.set_selected_port(selected_port, "esp32")
    
    def refresh_com_ports(self):
        self.com_ports = self.communicator.get_com_ports()
        print(f"Available COM ports: {self.com_ports}")  # Dodaj logi debugujące

        if len(self.com_ports) == 1:
            selected_port = self.com_ports[0]
            self.com_ports.set(selected_port)
            self.combo.set(selected_port)
            self.communicator.set_selected_port(selected_port, "esp32")
            print(f"Automatically selected COM port: {selected_port}")
            self.refresh_connection_esp32()  # Automatyczne połączenie po wybraniu portu
        else:
            # com_ports_var.set(com_ports[0] if com_ports else '')
            self.combo.configure(self.com_ports)
    
    def refresh_connection_esp32(self):
        connection_status = self.communicator.connect_esp32()
        if connection_status == 1:
            self.btn_conn.set("Connected")
            self.btn_refresh.change_color('green')
        else:
            self.btn_conn.set("Refresh Connection")
            self.btn_refresh.change_color('red')
            print("Connection failed.")


####################################
######## arduino connection

    def on_combobox_select_arduino(self):
        selected_port = self.combo_arduino.get()
        print(f"Selected Arduino port: {selected_port}")
        self.communicator.set_selected_port(selected_port, "arduino")

    def refresh_arduino_ports(self):
        arduino_ports = self.communicator.get_com_ports()
        print(f"Available Arduino ports: {arduino_ports}")

        if len(arduino_ports) == 1:
            selected_port = arduino_ports[0]
            self.com_ports_arduino.set(selected_port)
            self.combo_arduino.set(selected_port)
            self.communicator.set_selected_port(selected_port, "arduino")
            print(f"Automatically selected Arduino port: {selected_port}")
            self.refresh_connection_arduino()
        else:
            self.combo_arduino.set(arduino_ports[0] if arduino_ports else '')
            self.combo_arduino.configure(arduino_ports)

    def refresh_connection_arduino(self):
        connection_status = self.communicator.connect_arduino()
        if connection_status == 1:
            self.btn_conn_arduino.set("Connected")
            self.btn_refresh_arduino.change_color('green')
        else:
            self.btn_conn_arduino.set("Refresh Connection")
            self.btn_refresh_arduino.change_color('red')
            print("Arduino connection failed.")

    def event_handler(self):
        """Keyboard event handler - Q to quit, N/B to move between photos etc."""
        pass
