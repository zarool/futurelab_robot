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
