import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import app.ui as ui
from app.plot import Plot
from app.conn import Communicator
from robot.robot import Robot
from camera.capture import Camera

# COLUMNS_TEXT PROB NOT NEEDED
COLUMNS_TEXT = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
COLUMNS_HEADER = ["Id", "Voltage", "Current", "Temperature", "Position", "Load"]

class App:
    def __init__(self, camera_mode_width, camera_mode_height) -> None:
        ########################
        ############## GUI CONST
        ctk.set_appearance_mode("dark")  # Ustawienie ciemnego trybu
        ctk.set_default_color_theme("blue")  # Ustawienie domyślnego motywu kolorystycznego

        self.root = ctk.CTk()  # Użycie CTk zamiast Tk
        self.root.title("Robot Arm Inverse Kinematics")
        # self.root.geometry("1980x1080+0+0")

        ########################
        ################ NAVBAR AND FRAMES
        self.navbar = ctk.CTkFrame(self.root)
        self.navbar.grid(row=0, column=0, sticky="ew")

        self.main_frame = ctk.CTkFrame(self.root)
        self.camera_frame = ctk.CTkFrame(self.root)
        self.data_frame = ctk.CTkFrame(self.root)

        self.frames = {
            "main_frame": self.main_frame,
            "camera_frame": self.camera_frame,
            "data_frame": self.data_frame
        }

        ########################
        ################ OBJECTS
        self.communicator = Communicator()
        self.plot = Plot()
        self.robot = Robot()
        self.camera = Camera(camera_mode_width, camera_mode_height)
        self.camera.start()

        ########################
        ########## GUI VARIABLES
        self.sliders = []

        self.status_torque = ui.text_label(self.main_frame, "Status: " + str(self.communicator.toggle), "Helvetica", 20, 7, 5, 1, 10, "")
        self.status_torque.configure("Status: " + str(self.communicator.toggle))

        ########################
        ########## GRID POSITIONS

        ########################
        ########## camera

        self.frame_size = (300, 300)

        self.camera0 = ctk.CTkLabel(self.camera_frame, text="")
        self.camera0_contour = ctk.CTkLabel(self.camera_frame, text="")
        self.camera1 = ctk.CTkLabel(self.camera_frame, text="")
        self.camera1_contour = ctk.CTkLabel(self.camera_frame, text="")
        
        self.camera0.grid(column=1, row=1, rowspan=5)
        self.camera0_contour.grid(column=1, row=2, rowspan=5)

        self.camera1.grid(column=2, row=1, rowspan=5)
        self.camera1_contour.grid(column=2, row=2, rowspan=5)

        
        ########################
        ########## robot

        self.plot.plot_robot(self.robot, math.pi, -math.pi/2, 0, 0)

        self.entry_x = ui.text_gap(self.main_frame, 150, 0, 0, 25, 10 ,"e")
        self.entry_y = ui.text_gap(self.main_frame, 150, 1, 0, 25, 10 ,"e")
        self.entry_z = ui.text_gap(self.main_frame, 150, 2, 0, 25, 10 ,"e")

        self.label_coord = ctk.CTkLabel(self.main_frame, text="End-Effector Coordinates:\nX: 0.00 \nY: 0.00 \nZ: 0.00")
        self.label_coord.grid(row=3, column=0, rowspan=2, padx=10, pady=0, sticky="nsew")

        self.canvas = FigureCanvasTkAgg(self.plot.fig, master=self.main_frame)
        self.canvas.get_tk_widget().grid(column=1, row=0, rowspan=10, columnspan=2)

        ########################
        ########## connection

        self.com_ports = self.communicator.get_com_ports()
        self.btn_conn = ctk.StringVar()
        self.btn_refresh = ui.button(self.main_frame, None, self.btn_conn, self.refresh_connection_esp32, 1, 3, 10, 10)
        self.combo = ui.dropdown_list(self.main_frame, self.com_ports, "<<ComboboxSelected>>", self.on_combobox_select, 0, 3, 10, 10)
        self.combo.configure(self.com_ports)

        self.com_ports_arduino = self.communicator.get_com_ports()
        self.btn_conn_arduino = ctk.StringVar()
        self.btn_refresh_arduino = ui.button(self.main_frame, None, self.btn_conn_arduino, self.refresh_connection_arduino, 1, 5, 10, 10)
        self.combo_arduino = ui.dropdown_list(self.main_frame, self.com_ports_arduino, "<<ComboboxSelected>>", self.on_combobox_select_arduino, 0, 5, 10, 10)
        self.combo_arduino.configure(self.com_ports_arduino)

        ########################
        ########## positions
        self.positions = self.communicator.get_positions()

        # self.id_move_s = ui.text_gap(self.main_frame, 200, 9, 0, 25, 10 ,"w")
        # self.position_move_s = ui.text_gap(self.main_frame, 200, 11, 0, 25, 10 ,"w")

        ########################
        ########## data
        self.table = ui.table(self.data_frame, COLUMNS_TEXT, "headings", COLUMNS_HEADER, 160, 6, 16, 20, 20, 'nsew')

    def gui(self):
        "Allocate buttons and objects on window"

        ########################
        ########## CREATE FRAMES (TABS ON NAVBAR)
        def show_frame(frame):
            for f in self.frames.values():
                f.grid_forget()
            frame.grid(row=1, column=0, sticky="nsew")

        button1 = ctk.CTkButton(self.navbar, text="Program", command=lambda: show_frame(self.main_frame))
        button1.grid(row=0, column=0, padx=5, pady=10)
        button2 = ctk.CTkButton(self.navbar, text="Camera", command=lambda: show_frame(self.camera_frame))
        button2.grid(row=0, column=1, padx=5, pady=10)
        button3 = ctk.CTkButton(self.navbar, text="Dane", command=lambda: show_frame(self.data_frame))
        button3.grid(row=0, column=2, padx=5, pady=10)

        # show main frame by default
        show_frame(self.main_frame)

        ########################
        ########## MAIN FRAME

        nr_1 = ui.slider(self.main_frame, 3, 3, 0, 4096, 10, 10, "1", "Pos", 1, self.communicator)
        nr_2 = ui.slider(self.main_frame, 4, 3, 0, 4096, 10, 10, "2", "Pos", 1, self.communicator)
        nr_3 = ui.slider(self.main_frame, 5, 3, 0, 4096, 10, 10, "3", "Pos", 1, self.communicator)
        nr_4 = ui.slider(self.main_frame, 6, 3, 0, 4096, 10, 10, "4", "Pos", 1, self.communicator)
        nr_5 = ui.slider(self.main_frame, 7, 3, 0, 4096, 10, 10, "5", "Pos", 1, self.communicator)
        nr_6 = ui.slider(self.main_frame, 8, 3, 0, 4096, 10, 10, "6", "Pos", 1, self.communicator)
        self.sliders = [nr_1, nr_2, nr_3, nr_4, nr_5, nr_6]

        for slider, position in zip(self.sliders, self.positions):
            slider.slider.set(position)
            slider.update_label(position)

        self.offset_1 = ui.text_gap(self.main_frame, 120, 3, 5, 10, 10, "e")
        self.offset_2 = ui.text_gap(self.main_frame, 120, 4, 5, 10, 10, "e")
        self.offset_3 = ui.text_gap(self.main_frame, 120, 5, 5, 10, 10, "e")
        self.offset_4 = ui.text_gap(self.main_frame, 120, 6, 5, 10, 10, "e")
        ui.text_label(self.main_frame, "Offset 1:", "Helvetica", 12, 3, 5, 10, 10, "w")
        ui.text_label(self.main_frame, "Offset 2:", "Helvetica", 12, 4, 5, 10, 10, "w")
        ui.text_label(self.main_frame, "Offset 3:", "Helvetica", 12, 5, 5, 10, 10, "w")
        ui.text_label(self.main_frame, "Offset 4:", "Helvetica", 12, 6, 5, 10, 10, "w")

        btn_change_variable = ui.button(self.main_frame, "Toggle torque", None,
            lambda: self.communicator.toggle_and_send_command(self.status_torque), 8, 5, 10, 10)

        ########################
        ########## PLOT DISPLAY

        ui.text_label(self.main_frame, "X:", "Helvetica", 12, 0, 0, 10, 10, "w")
        ui.text_label(self.main_frame, "Y:", "Helvetica", 12, 1, 0, 10, 10, "w")
        ui.text_label(self.main_frame, "Z:", "Helvetica", 12, 2, 0, 10, 10, "w")
        # ui.text_label(self.main_frame,"ID","Helvetica", 12, 8, 0, 10, 0, None)
        # ui.text_label(self.main_frame,"Position","Helvetica", 12, 10, 0, 10, 0, None)

        btn_compute = ui.button(self.main_frame,"Oblicz", None, self.update_robot, 5, 0, 10, 10)
        # btn_move = ui.button(self.main_frame, "Wykonaj", None, lambda: self.communicator.test(self.id_move_s, self.position_move_s), 6, 0, 10, 10)
        btn_transport = ui.button(self.main_frame, "Transport", None, self.communicator.transport_mode, 6, 0, 10, 10)

        ########################
        ########## CAMERA SECTION

        # ID:       ZAKRES:       PARA:
        #   2 UP/DOWN   0-80        LEWA
        #   3 ROTATION  0-140       LEWA
        #   4 ROTATION  0-180       PRAWA
        #   5 UP/DOWN   0-80        PRAWA
       
        ##########################################
        # test camera movemenet
        ui.text_label(self.camera_frame, "Camera ID:", "Helvetica", 12, 1, 0, 10, 10, "w")
        ui.text_label(self.camera_frame, "Target pos:", "Helvetica", 12, 2, 0, 10, 10, "w")
        ui.text_label(self.camera_frame, "Step delay:", "Helvetica", 12, 3, 0, 10, 10, "w")
        ui.text_label(self.camera_frame, "Step size:", "Helvetica", 12, 4, 0, 10, 10, "w")
        self.entry_id        = ui.text_gap(self.camera_frame, 100, 1, 0, 25, 10, "e")
        self.target_position = ui.text_gap(self.camera_frame, 100, 2, 0, 25, 10, "e")
        self.step_delay      = ui.text_gap(self.camera_frame, 100, 3, 0, 25, 10, "e")
        self.step_size       = ui.text_gap(self.camera_frame, 100, 4, 0, 25, 10, "e")
       
        btn_send_camera = ui.button(self.camera_frame, "Send", None,
            lambda: self.communicator.driver.move_camera(
                id_camera=int(self.entry_id.get()),
                target_position=int(self.target_position.get()),
                step_delay=float(self.step_delay.get()),
                step_size=int(self.step_size.get())
            ), 8, 0, 10, 10
        )

        nr_1 = ui.slider(self.camera_frame, 1, 3, 0, 254, 10, 10, "1", "Threshold 1", 2, self.camera)
        nr_2 = ui.slider(self.camera_frame, 2, 3, 0, 254, 10, 10, "2", "Threshold 2", 2, self.camera)
        nr_3 = ui.slider(self.camera_frame, 3, 3, 0, 3000, 10, 10, "3", "Max area", 2, self.camera)
        nr_4 = ui.slider(self.camera_frame, 4, 3, 0, 3000, 10, 10, "4", "Min area", 2, self.camera)
        nr_5 = ui.slider(self.camera_frame, 5, 3, -100, 100, 10, 10, "5", "Brightness", 2, self.camera)
        nr_6 = ui.slider(self.camera_frame, 6, 3, 0, 20, 10, 10, "6", "Contrast", 2, self.camera)
        self.sliders_cam = [nr_1, nr_2, nr_3, nr_4, nr_5, nr_6]

        for slider, position in zip(self.sliders, self.camera.get_param()):
            slider.slider.set(position)
            slider.update_label(position)


        # button_showcase = ui.button(self.main_frame, "Showcase", None, self.communicator.showcase_camera, 11, 5, 10, 10)

        ########################
        ########## CONNECTION SECTION

        btn_refresh_com = ui.button(self.main_frame,"Refresh COM Ports", None, self.refresh_com_ports, 2, 3, 10, 10)
        btn_refresh_com_arduino = ui.button(self.main_frame, "Refresh Arduino Ports", None, self.refresh_arduino_ports, 2, 5, 10, 10)

        ########################
        ########## DATA FRAME
        # self.table

    def run(self):
        "Main run function, will start threads and functionality of app"

        # init gui
        self.gui()

        # display robot visualization and update label
        self.canvas.draw()

        # run threads to receive data from other devices
        self.communicator.start_receive_data_thread(self.update_display)

        # check for conenctions
        self.refresh_connections()

        # read images from camera process using redis
        self.read_camera()

        self.event_handler()
        # self.root.after(100, self.update_table)
        self.root.mainloop()

###################################
####### camera

    def read_camera(self):
        self.camera.start()

        img0, img1 = self.camera.get_image()
        img0_cnt, img1_cnt = self.camera.get_contour()

        self.camera0.configure(
            image=ctk.CTkImage(img0, size=(self.frame_size)))
        self.camera0_contour.configure(
            image=ctk.CTkImage(img0_cnt, size=(self.frame_size)))

        self.camera1.configure(
            image=ctk.CTkImage(img1, size=(self.frame_size)))
        self.camera1_contour.configure(
            image=ctk.CTkImage(img1_cnt, size=(self.frame_size)))

        self.camera0.after(1, self.read_camera)

###################################
####### robot

    def update_robot(self):
        theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4 = self.robot.update_robot(self.entry_x.get(), self.entry_y.get(), self.entry_z.get())

        self.plot.plot_robot(self.robot, theta1, theta2, theta3, theta4)
        self.communicator.move_to_position(pos1, pos2, pos3, pos4, self.offset_1, self.offset_2, self.offset_3, self.offset_4)

        self.label_coord.configure(text=f"End-Effector Coordinates:\nX: {self.robot.rx:.2f} \nY: {self.robot.ry:.2f} \nZ: {self.robot.rz:.2f}")
        self.update_table()
        self.plot.fig.canvas.draw_idle()

    ###################################
    ####### app updates

    def refresh_connections(self):
        self.refresh_connection_esp32()
        self.refresh_connection_arduino()

    def update_table(self):
        id, voltage, current, temp, pos, load = self.communicator.get_data()
        for i in range(len(id)):
            self.update_display(id[i], voltage[i], current[i], temp[i], pos[i], load[i])

    def update_display(self, servo_id, voltage, current, temperature, pos, load):
        data = (servo_id, f"{voltage:.1f}V", f"{current:.1f}A", f"{temperature:.1f}C", pos, f"{load:.1f}N")
        self.table.insert_or_update(servo_id, values=data)

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
            self.combo.set(self.com_ports[0] if self.com_ports else '')
            self.combo.configure(self.com_ports)

    def refresh_connection_esp32(self):
        connection_status = self.communicator.connect_esp32()
        if connection_status == 1:
            self.btn_conn.set("Connected")
            self.btn_refresh.change_color('green')
        else:
            self.btn_conn.set("Refresh connection")
            self.btn_refresh.change_color('red')
            print("Connection failed.")

    ####################################
    ######## arduino connection

    def on_combobox_select_arduino(self):
        selected_port = self.combo_arduino.get()
        print(f"Selected Arduino port: {selected_port}")
        self.communicator.set_selected_port(selected_port, "arduino")

    def refresh_arduino_ports(self):
        self.com_ports_arduino = self.communicator.get_com_ports()
        print(f"Available Arduino ports: {self.com_ports_arduino}")

        if len(self.com_ports_arduino) == 1:
            selected_port = self.com_ports_arduino[0]
            self.com_ports_arduino.set(selected_port)
            self.combo_arduino.set(selected_port)
            self.communicator.set_selected_port(selected_port, "arduino")
            print(f"Automatically selected Arduino port: {selected_port}")
            self.refresh_connection_arduino()
        else:
            self.combo_arduino.set(self.com_ports_arduino[0] if self.com_ports_arduino else '')
            self.combo_arduino.configure(self.com_ports_arduino)

    def refresh_connection_arduino(self):
        connection_status = self.communicator.connect_arduino()
        if connection_status == 1:
            self.btn_conn_arduino.set("Connected")
            self.btn_refresh_arduino.change_color('green')
        else:
            self.btn_conn_arduino.set("Refresh connection arduino")
            self.btn_refresh_arduino.change_color('red')
            print("Arduino connection failed.")

    ###################################
    ####### test

    def thetas_to_0(self):
        self.plot.plot_robot(self.robot, 0, -3.14, 1, 1)

    ####################################
    ######## app event handler

    def quit_app(self):
        self.root.destroy()
        # sys.exit(0)

    def event_handler(self):
        """Keyboard event handler - Q to quit, N/B to move between photos etc."""
        self.root.bind("q", lambda x: self.quit_app())
        self.root.bind("Q", lambda x: self.quit_app())
