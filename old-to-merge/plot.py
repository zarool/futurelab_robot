import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk, ImageSequence
import kinematics as k
import communication as com
import servo
import tkinter as tk
from tkinter import ttk
import forgui as fg
from communication import positions
import math
import time

# Globalne zmienne dla rysunku i interfejsu
fig = None
ax = None
coordinates_label = None
entry_x = 100
entry_y = 100
entry_z = 250
tree = None
combobox = None
com_ports_var = None
refresh_button = None
button_connection = None
root = None
gif_label = None  # Dodane dla GIF-u





def plot_robot(theta1, theta2, theta3, theta4):
    global ax, coordinates_label

    a3 = 152.794
    a4 = 157.76
    a5 = 90

    rx, ry, rz = k.compute_end_effector_position(theta1, theta2, theta3, theta4, a3, a4, a5)

    ax.cla()

    ax.plot([0], [0], [0], 'go', label='Base')

    T1_end = k.T1(theta1)
    T2_end = np.dot(T1_end, k.T2(theta2))
    T3_end = np.dot(T2_end, k.T3(theta3, a3))
    T4_end = np.dot(T3_end, k.T4(theta4, a4))
    T5_end = np.dot(T4_end, k.T5(a5))

    points = np.array([
        [0, 0, 0],
        T1_end[:3, 3],
        T2_end[:3, 3],
        T3_end[:3, 3],
        T4_end[:3, 3],
        T5_end[:3, 3]
    ])

    ax.plot(points[:, 0], points[:, 1], points[:, 2], 'bo-', label='Links')
    ax.plot(rx, ry, rz, 'ro', label='End-Effector')

    ax.set_xlim(-200, 200)
    ax.set_ylim(-200, 200)
    ax.set_zlim(-200, 200)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Robot Arm')
    ax.legend()

    coordinates_label.configure(text=f"End-Effector Coordinates:\nX: {rx:.2f}, Y: {ry:.2f}, Z: {rz:.2f}")

def init_plot():
    global fig, ax
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    plot_robot(math.pi, -math.pi/2, 0, 0)

def update_display(servo_id, voltage, current, temperature, pos, load):
    data = (servo_id, f"{voltage:.1f}V", f"{current:.1f}A", f"{temperature:.1f}C", pos, f"{load:.1f}N")
    table.insert_or_update(servo_id, values=data)

def update_robot():
    global entry_x, entry_y, entry_z

    try:
        x = entry_x.get()
        y = entry_y.get()
        z = entry_z.get()

        theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4, valid_position = k.inverse_kinematics(x, y, z)
        
        if theta1 is not None:
            plot_robot(theta1, theta2, theta3, theta4)
            servo.move_to_position(pos1, pos2, pos3, pos4)
            update_table()
            fig.canvas.draw_idle()
    except ValueError:
        print("ValueError")

def update_table():
    ids = com.id
    voltages = com.voltage
    currents = com.current
    temperatures = com.temperature
    positions = com.positions
    loads = com.load
    
    for i in range(len(ids)):
        update_display(ids[i], voltages[i], currents[i], temperatures[i], positions[i], loads[i])

def on_combobox_select(event):
    selected_port = combobox.get()
    print(f"Selected COM port: {selected_port}")  # Dodaj logi debugujące
    com.set_selected_port(selected_port, "esp32")

def refresh_com_ports():
    com_ports = com.get_com_ports()
    print(f"Available COM ports: {com_ports}")  # Dodaj logi debugujące

    if len(com_ports) == 1:
        selected_port = com_ports[0]
        com_ports_var.set(selected_port)
        combobox.set(selected_port)
        com.set_selected_port(selected_port)
        print(f"Automatically selected COM port: {selected_port}")
        update_refresh_connection_esp32()  # Automatyczne połączenie po wybraniu portu
    else:
        # com_ports_var.set(com_ports[0] if com_ports else '')
        combobox.configure(com_ports)

def update_refresh_connection_esp32():
    connection_status = com.connect_esp32()
    if connection_status == 1:
        button_connection.set("Connected")
        refresh_button.change_color('green')
    else:
        button_connection.set("Refresh Connection")
        refresh_button.change_color('red')
        print("Connection failed.")


def thetas_to_0():
    plot_robot(0,-3.14,1,1)

def test():
    print("czesc")
    if(id_move_s.get() is None and position_move_s.get() is None):
        print("uzupełnij luke")
    else:
        com.move(int(id_move_s.get()),int(position_move_s.get()))

def uptd_offset():
    off_1 = offset_1.get()
    off_2 = offset_2.get()
    off_3 = offset_3.get()
    off_4 = offset_4.get()
    return off_1, off_2, off_3, off_4

toggle_var = False

def toggle_and_send_command():
    global toggle_var
    toggle_var = not toggle_var
    if toggle_var:
        com.send_command("T,1")
        status_torque.configure("Status: " + str(toggle_var))
    else:
        com.send_command("T,0")
        status_torque.configure("Status: " + str(toggle_var))

def showcase_camera():
    com.move_camera(1, 80)
    com.move_camera(2, 0)
    com.move_camera(3, 80)
    com.move_camera(4, 0)
    time.sleep(2)
    com.move_camera(1, 0)
    com.move_camera(2, 150)
    com.move_camera(3, 0)
    com.move_camera(4, 150)
    time.sleep(2)

def on_combobox_select_arduino(event):
    selected_port = arduino_combobox.get()
    print(f"Selected Arduino port: {selected_port}")
    com.set_selected_port(selected_port, "arduino")

def refresh_arduino_ports():
    arduino_ports = com.get_com_ports()
    print(f"Available Arduino ports: {arduino_ports}")

    if len(arduino_ports) == 1:
        selected_port = arduino_ports[0]
        arduino_ports_var.set(selected_port)
        arduino_combobox.set(selected_port)
        com.set_selected_arduino_port(selected_port)
        print(f"Automatically selected Arduino port: {selected_port}")
        update_refresh_connection_arduino()
    else:
        arduino_combobox.set(arduino_ports[0] if arduino_ports else '')
        arduino_combobox.configure(arduino_ports)

def update_refresh_connection_arduino():
    connection_status = com.connect_arduino()
    if connection_status == 1:
        arduino_button_connection.set("Connected")
        arduino_refresh_button.change_color('green')
    else:
        arduino_button_connection.set("Refresh Connection")
        arduino_refresh_button.change_color('red')
        print("Arduino connection failed.")






def gui():
    global status_torque, offset_1, offset_2, offset_3, offset_4, sliders, position_move_s, id_move_s, table, coordinates_label, entry_x, entry_y, entry_z, tree, combobox, com_ports_var, refresh_button, button_connection, root, gif_label, gif_frames, gif_current_frame, arduino_combobox, arduino_ports_var, arduino_refresh_button, arduino_button_connection
    
    ctk.set_appearance_mode("dark")  # Ustawienie ciemnego trybu
    ctk.set_default_color_theme("blue")  # Ustawienie domyślnego motywu kolorystycznego

    root = ctk.CTk()  # Użycie CTk zamiast Tk
    root.title("Robot Arm Inverse Kinematics")
    root.geometry("1980x480+0+0")

    button_connection = ctk.StringVar()
    com_ports_var = com.get_com_ports()

    arduino_button_connection = ctk.StringVar()
    arduino_ports_var = com.get_com_ports()

    # Pasek na górze
    top_frame = ctk.CTkFrame(root)
    top_frame.grid(row=0, column=0, sticky="ew")

    def show_frame(frame):
        for f in frames.values():
            f.grid_forget()
        frame.grid(row=1, column=0, sticky="nsew")

    # Przyciski zmieniające okna
    button1 = ctk.CTkButton(top_frame, text="Sterowanie", command=lambda: show_frame(control_frame))
    button1.grid(row=0, column=0, padx=5, pady=5)

    button2 = ctk.CTkButton(top_frame, text="Tabela", command=lambda: show_frame(table_frame))
    button2.grid(row=0, column=1, padx=5, pady=5)

    button3 = ctk.CTkButton(top_frame, text="Wykres", command=lambda: show_frame(plot_frame))
    button3.grid(row=0, column=2, padx=5, pady=5)

    button4 = ctk.CTkButton(top_frame, text="Komunikacja", command=lambda: show_frame(communication_frame))
    button4.grid(row=0, column=3, padx=5, pady=5)

    button5 = ctk.CTkButton(top_frame, text="Serwo kamera", command=lambda: show_frame(servo_camera_frame))
    button5.grid(row=0, column=4, padx=5, pady=5)
    # Ramki
    frames = {}

    control_frame = ctk.CTkFrame(root)
    frames[control_frame] = control_frame

    communication_frame = ctk.CTkFrame(root)
    frames[communication_frame] = communication_frame

    table_frame = ctk.CTkFrame(root)
    frames[table_frame] = table_frame

    plot_frame = ctk.CTkFrame(root)
    frames[plot_frame] = plot_frame

    servo_camera_frame = ctk.CTkFrame(root)
    frames[servo_camera_frame] = servo_camera_frame

    # Zawartość ramki control_frame
    nr_1 = fg.new_slider(control_frame, 0, 5, 0, 4096, 10, 10, "1", "Pos", 1)
    nr_2 = fg.new_slider(control_frame, 1, 5, 0, 4096, 10, 10, "2", "Pos", 1)
    nr_3 = fg.new_slider(control_frame, 2, 5, 0, 4096, 10, 10, "3", "Pos", 1)
    nr_4 = fg.new_slider(control_frame, 3, 5, 0, 4096, 10, 10, "4", "Pos", 1)
    nr_5 = fg.new_slider(control_frame, 4, 5, 0, 4096, 10, 10, "5", "Pos", 1)
    nr_6 = fg.new_slider(control_frame, 5, 5, 0, 4096, 10, 10, "6", "Pos", 1)
    
    sliders = [nr_1, nr_2, nr_3, nr_4, nr_5, nr_6]
    
    for slider, position in zip(sliders, positions):
        slider.slider.set(position)
        slider.update_label(position)

    offset_1 = fg.new_text_gap(control_frame, 200, 0, 6, 60, 10, "e")
    offset_2 = fg.new_text_gap(control_frame, 200, 1, 6, 60, 10, "e")
    offset_3 = fg.new_text_gap(control_frame, 200, 2, 6, 60, 10, "e")
    offset_4 = fg.new_text_gap(control_frame, 200, 3, 6, 60, 10, "e")

    fg.new_text_label(control_frame, "Offset 1:", "Helvetica", 12, 0, 6, 10, 10, "w")
    fg.new_text_label(control_frame, "Offset 2:", "Helvetica", 12, 1, 6, 10, 10, "w")
    fg.new_text_label(control_frame, "Offset 3:", "Helvetica", 12, 2, 6, 10, 10, "w")
    fg.new_text_label(control_frame, "Offset 4:", "Helvetica", 12, 3, 6, 10, 10, "w")

    button_change_variable = fg.new_button(control_frame, "Toggle torque", None, toggle_and_send_command, 2, 3, 10, 10, None, None)
    
    combobox = fg.new_dropdown_list(communication_frame, com_ports_var, "<<ComboboxSelected>>", on_combobox_select, 1, 1, 10, 10)
    combobox.configure(com_ports_var)
    
    status_torque = fg.new_text_label(control_frame, "Status: " + str(toggle_var), "Helvetica", 12, 3, 3, 10, 10, "w")
    status_torque.configure("Status: " + str(toggle_var))
    
    fg.new_text_label(control_frame, "X:", "Helvetica", 12, 0, 0, 10, 10, "w")
    fg.new_text_label(control_frame, "Y:", "Helvetica", 12, 1, 0, 10, 10, "w")
    fg.new_text_label(control_frame, "Z:", "Helvetica", 12, 2, 0, 10, 10, "w")
    fg.new_text_label(control_frame,"ID","Helvetica", 12, 1, 2, 10, 10, None)
    fg.new_text_label(control_frame,"Position","Helvetica", 12, 1, 2, 10, 10, None)
    
    entry_x = fg.new_text_gap(control_frame, 200, 0, 0, 25, 10 ,"w")
    entry_y = fg.new_text_gap(control_frame, 200, 1, 0, 25, 10 ,"w")
    entry_z = fg.new_text_gap(control_frame, 200, 2, 0, 25, 10 ,"w")

    id_move_s = fg.new_text_gap(control_frame, 200, 0, 2, 25, 10 ,"w")
    position_move_s = fg.new_text_gap(control_frame, 200, 1, 2, 25, 10 ,"w")

    
    button_compute = fg.new_button(control_frame,"Oblicz", None, update_robot, 3, 0, 50, 10,'w', None)
    button_move_to = fg.new_button(control_frame, "Wykonaj", None, test, 2, 2, 10, 10, None, None)
    button_transport = fg.new_button(control_frame, "Transport", None, servo.transport_mode, 0, 3, 10, 10, None, None)

    button_showcase = fg.new_button(servo_camera_frame, "Showcase", None, showcase_camera, 3, 4, 10, 10, None, None)

    refresh_button_ports_com = fg.new_button(communication_frame,"Refresh COM Ports", None, refresh_com_ports, 2, 1, 10, 10, "w", None)
    refresh_button = fg.new_button(communication_frame, None, button_connection, update_refresh_connection_esp32, 3, 1, 10, 10, None, None)

    arduino_combobox = fg.new_dropdown_list(communication_frame, arduino_ports_var, "<<ComboboxSelected>>", on_combobox_select_arduino, 1, 2, 10, 10)
    arduino_combobox.configure(arduino_ports_var)
    arduino_refresh_button_ports_com = fg.new_button(communication_frame, "Refresh Arduino Ports", None, refresh_arduino_ports, 2, 2, 10, 10, "w", None)
    arduino_refresh_button = fg.new_button(communication_frame, None, arduino_button_connection, update_refresh_connection_arduino, 3, 2, 10, 10, None, None)

    update_refresh_connection_esp32()

    coordinates_label = ctk.CTkLabel(control_frame, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
    coordinates_label.grid(row=4, column=0, columnspan=2, padx=50, pady=10, sticky="w")

    init_plot()

    # Zawartość ramki table_frame
    columns = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
    texts = ["Id", "Voltage", "Current", "Temperature", "Position", "Load"]
    table = fg.new_table(table_frame, columns, "headings", texts, 160, 6, 16, 20, 20, 'nsew')

    # Zawartość ramki plot_frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    com.start_receive_data_thread(update_display)

    root.after(100, update_table)
    root.mainloop()

