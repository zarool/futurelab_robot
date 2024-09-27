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