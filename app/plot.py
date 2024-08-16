import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk, ImageSequence
import src.kinematics as k
import firmware.communication as com
import firmware.servo
import tkinter as tk
from tkinter import ttk

# Globalne zmienne dla rysunku i interfejsu
fig = None
ax = None
coordinates_label = None
entry_x = None
entry_y = None
entry_z = None
tree = None
combobox = None
com_ports_var = None
refresh_button = None
button_connection = None
root = None
gif_label = None  # Dodane dla GIF-u

# Funkcja do zmiany rozmiaru klatek GIF-u
def resize_gif_frames(gif_frames, size):
    resized_frames = []
    for frame in gif_frames:
        # Resize na obiekcie Image
        resized_frame = frame.resize(size, Image.LANCZOS)
        resized_frames.append(ImageTk.PhotoImage(resized_frame))
    return resized_frames

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
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    plot_robot(0, 0, 0, 0)

def update_display(servo_id, voltage, current, temperature, pos, load):
    for row in tree.get_children():
        if int(tree.item(row, 'values')[0]) == servo_id:
            tree.item(row, values=(servo_id, voltage, current, temperature, pos, load))
            return
    tree.insert("", "end", values=(servo_id, voltage, current, temperature, pos, load))

def update_robot():
    global entry_x, entry_y, entry_z

    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())

        theta1, theta2, theta3, theta4, pos1, pos2, pos3, pos4 = k.inverse_kinematics(x, y, z)

        if theta1 is not None:
            plot_robot(theta1, theta2, theta3, theta4)
            servo.move_to_position(pos1, pos2, pos3, pos4)
            update_table()
            fig.canvas.draw_idle()
    except ValueError:
        ctk.CTkMessageBox.show_error("Error", "Invalid input. Please enter valid numerical values.")

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
    selected_port = com_ports_var.get()
    print(f"Selected COM port: {selected_port}")  # Dodaj logi debugujące
    com.set_selected_port(selected_port)

def refresh_com_ports():
    com_ports = com.get_com_ports()
    print(f"Available COM ports: {com_ports}")  # Dodaj logi debugujące

    if len(com_ports) == 1:
        selected_port = com_ports[0]
        com_ports_var.set(selected_port)
        combobox.set(selected_port)
        com.set_selected_port(selected_port)
        print(f"Automatically selected COM port: {selected_port}")
        update_refresh_connection()  # Automatyczne połączenie po wybraniu portu
    else:
        com_ports_var.set(com_ports[0] if com_ports else '')
        combobox.configure(values=com_ports)

def update_refresh_connection():
    connection_status = com.connect()
    if connection_status == 1:
        button_connection.set("Connected")
        refresh_button.configure(fg_color='green')
    else:
        button_connection.set("Refresh Connection")
        refresh_button.configure(fg_color='red')
        print("Connection failed.")

def update_gif_animation():
    global gif_label, gif_frames, gif_current_frame
    # Ustaw bieżący obraz w label
    gif_label.configure(image=gif_frames[gif_current_frame])
    # Przesuń do następnej klatki
    gif_current_frame = (gif_current_frame + 1) % len(gif_frames)
    # Opóźnienie w ms (np. 100ms)
    root.after(100, update_gif_animation)

def gui():
    global coordinates_label, entry_x, entry_y, entry_z, tree, combobox, com_ports_var, refresh_button, button_connection, root, gif_label, gif_frames, gif_current_frame

    ctk.set_appearance_mode("dark")  # Ustawienie ciemnego trybu
    ctk.set_default_color_theme("blue")  # Ustawienie domyślnego motywu kolorystycznego

    root = ctk.CTk()  # Użycie CTk zamiast Tk
    root.title("Robot Arm Inverse Kinematics")

    button_connection = ctk.StringVar()
    refresh_button = ctk.CTkButton(root, textvariable=button_connection, command=update_refresh_connection, fg_color='red')
    refresh_button.grid(row=3, column=1, padx=10, pady=10)
    update_refresh_connection()

    com_ports_var = ctk.StringVar()
    combobox = ctk.CTkComboBox(root, variable=com_ports_var)
    combobox.bind("<<ComboboxSelected>>", on_combobox_select)
    combobox.grid(row=1, column=1, padx=10, pady=10)

    refresh_button2 = ctk.CTkButton(root, text="Refresh COM Ports", command=refresh_com_ports)
    refresh_button2.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    ctk.CTkLabel(root, text="X:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    ctk.CTkLabel(root, text="Y:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    ctk.CTkLabel(root, text="Z:", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")

    entry_x = ctk.CTkEntry(root, width=200)
    entry_y = ctk.CTkEntry(root, width=200)
    entry_z = ctk.CTkEntry(root, width=200)
    entry_x.grid(row=1, column=0, padx=25, pady=10, sticky="w")
    entry_y.grid(row=2, column=0, padx=25, pady=10, sticky="w")
    entry_z.grid(row=3, column=0, padx=25, pady=10, sticky="w")

    button_compute = ctk.CTkButton(root, text="Compute", command=update_robot)
    button_compute.grid(row=4, column=0, padx=50, pady=10, sticky="w")

    coordinates_label = ctk.CTkLabel(root, text="End-Effector Coordinates:\nX: 0.00, Y: 0.00, Z: 0.00")
    coordinates_label.grid(row=5, column=0, columnspan=2, padx=50, pady=10, sticky="w")

    init_plot()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(row=7, column=6, columnspan=2, padx=10, pady=10)
    canvas.draw()

    columns = ("Id", "Voltage", "Current", "Temperature", "Position", "Load")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.grid(row=6, column=6, padx=10, pady=10, sticky='nsew')

    # Załaduj i przeskaluj animowany GIF
    gif_path = "animated.gif"
    gif_image = Image.open(gif_path)
    gif_frames = [frame.copy() for frame in ImageSequence.Iterator(gif_image)]
    gif_frames = resize_gif_frames(gif_frames, (150, 150))  # Zmien rozmiar GIF-u
    gif_current_frame = 0

    gif_label = ctk.CTkLabel(root)
    gif_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    update_gif_animation()  # Rozpocznij animację GIF-u

    com.start_receive_data_thread(update_display)
    root.after(100, update_table)
    root.mainloop()

gui()
