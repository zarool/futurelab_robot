import customtkinter as ctk
import tkinter as ttk
from tkinter import ttk

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk, ImageSequence

import app.ui as ui


class App:
    def __init__(self, com) -> None:
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
        self.communicator = com


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
        self.com_ports = com.get_com_ports()

        self.combo_arduino = 0
        self.btn_refresh_arduino = 0
        self.btn_conn_arduino = ctk.StringVar()
        self.com_ports_arduino = com.get_com_ports()

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


        ########################
        ########## PLOT DISPLAY

        # canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # canvas.draw()

        # self.com.start_receive_data_thread(update_display)


        ########################
        ########## DATA FRAME
        # Zawartość ramki table_frame
        columns = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
        texts = ["Id", "Voltage", "Current", "Temperature", "Position", "Load"]
        table = ui.table(data_frame, columns, "headings", texts, 160, 6, 16, 20, 20, 'nsew')

    def run(self):
        "Main run function, will start threads and functionality of app"

        self.gui()

        self.root.after(100, self.update_table)
        self.root.mainloop()

    def update_table(self):
        pass


    def event_handler(self):
        pass



#     button_change_variable = fg.new_button(control_frame, "Toggle torque", None, toggle_and_send_command, 2, 3, 10, 10, None, None)

#     combobox = fg.new_dropdown_list(communication_frame, com_ports_var, "<<ComboboxSelected>>", on_combobox_select, 1, 1, 10, 10)
#     combobox.configure(com_ports_var)

#     status_torque = fg.new_text_label(control_frame, "Status: " + str(toggle_var), "Helvetica", 12, 3, 3, 10, 10, "w")
#     status_torque.configure("Status: " + str(toggle_var))

#     fg.new_text_label(control_frame, "X:", "Helvetica", 12, 0, 0, 10, 10, "w")
#     fg.new_text_label(control_frame, "Y:", "Helvetica", 12, 1, 0, 10, 10, "w")
#     fg.new_text_label(control_frame, "Z:", "Helvetica", 12, 2, 0, 10, 10, "w")
#     fg.new_text_label(control_frame,"ID","Helvetica", 12, 1, 2, 10, 10, None)
#     fg.new_text_label(control_frame,"Position","Helvetica", 12, 1, 2, 10, 10, None)

#     entry_x = fg.new_text_gap(control_frame, 200, 0, 0, 25, 10 ,"w")
#     entry_y = fg.new_text_gap(control_frame, 200, 1, 0, 25, 10 ,"w")
#     entry_z = fg.new_text_gap(control_frame, 200, 2, 0, 25, 10 ,"w")

#     id_move_s = fg.new_text_gap(control_frame, 200, 0, 2, 25, 10 ,"w")
#     position_move_s = fg.new_text_gap(control_frame, 200, 1, 2, 25, 10 ,"w")


#     button_compute = fg.new_button(control_frame,"Oblicz", None, update_robot, 3, 0, 50, 10,'w', None)
#     button_move_to = fg.new_button(control_frame, "Wykonaj", None, test, 2, 2, 10, 10, None, None)
#     button_transport = fg.new_button(control_frame, "Transport", None, servo.transport_mode, 0, 3, 10, 10, None, None)

#     button_showcase = fg.new_button(servo_camera_frame, "Showcase", None, showcase_camera, 3, 4, 10, 10, None, None)

#     refresh_button_ports_com = fg.new_button(communication_frame,"Refresh COM Ports", None, refresh_com_ports, 2, 1, 10, 10, "w", None)
#     refresh_button = fg.new_button(communication_frame, None, button_connection, update_refresh_connection_esp32, 3, 1, 10, 10, None, None)

#     arduino_combobox = fg.new_dropdown_list(communication_frame, arduino_ports_var, "<<ComboboxSelected>>", on_combobox_select_arduino, 1, 2, 10, 10)
#     arduino_combobox.configure(arduino_ports_var)
#     arduino_refresh_button_ports_com = fg.new_button(communication_frame, "Refresh Arduino Ports", None, refresh_arduino_ports, 2, 2, 10, 10, "w", None)
#     arduino_refresh_button = fg.new_button(communication_frame, None, arduino_button_connection, update_refresh_connection_arduino, 3, 2, 10, 10, None, None)

#     update_refresh_connection_esp32()

#     coordinates_label = ctk.CTkLabel(control_frame, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
#     coordinates_label.grid(row=4, column=0, columnspan=2, padx=50, pady=10, sticky="w")

#     init_plot()
