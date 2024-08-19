import serial
import serial.tools.list_ports
import threading
import time

# Inicjalizacja zmiennych globalnych
id = [1, 2, 3, 4, 5, 6]
voltage = [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
current = [2.3, 2.4, 2.5, 2.6, 2.7, 3]
temperature = [36.0, 37.0, 38.0, 39.0, 40.0, 40]
positions = [120, 130, 140, 150, 160, 200]
load = [1.5, 1.6, 1.7, 1.8, 1.9, 2]
speed = 150
acc = 150
connection_status = None
_selected_port = ""
arduino_port = ""
arduino_baudrate = 9600
esp32_port = ""
esp32_baudrate = 115200
running = True
ser_arduino = None
ser_esp32 = None

def send_command_camera(command):
    if command and ser_esp32 is not None and ser_esp32.is_open:
        try:
            full_command = f"*{command}*"
            ser_esp32.write(full_command.encode('utf-8') + b'\n')
            print(f"Wysłano komendę: {full_command}")
        except serial.SerialException as e:
            print(f"Błąd wysyłania komendy: {e}")

def move_camera(id_camera, position):
    id_camera = int(id_camera)
    position = int(position)
    send_command_camera(f"{id_camera},{position}")

def send_command(command):
    if command and ser_arduino is not None and ser_arduino.is_open:
        try:
            full_command = f"({command})"
            ser_arduino.write(full_command.encode('utf-8') + b'\n')
            print(f"Wysłano komendę: {full_command}")
        except serial.SerialException as e:
            print(f"Błąd wysyłania komendy: {e}")

def connect_arduino():
    global connection_status, ser_arduino, arduino_port, running
    try:
        if ser_arduino is not None and ser_arduino.is_open:
            ser_arduino.close()
            print("Zresetowano połączenie z Arduino.")
        ser_arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
        print(f"Połączono z Arduino na porcie {arduino_port}")
        connection_status_arduino = 1
        running = True
        return connection_status_arduino
    except serial.SerialException as e:
        running = False
        print(f"Błąd połączenia: {e}")
        connection_status_arduino = 0
        return connection_status_arduino

def connect_esp32():
    global ser_esp32, esp32_port, running
    try:
        if ser_esp32 is not None and ser_esp32.is_open:
            ser_esp32.close()
            print("Zresetowano połączenie z ESP32.")
        ser_esp32 = serial.Serial(esp32_port, esp32_baudrate, timeout=1)
        print(f"Połączono z ESP32 na porcie {esp32_port}")
        connection_status_esp32 = 1
        running = True
        return connection_status_esp32
    except serial.SerialException as e:
        running = False
        print(f"Błąd połączenia: {e}")
        connection_status_esp32 = 0
        return connection_status_esp32

def move(id, position):
    id = int(id)
    position = int(position)
    send_command(f"{id},{position},{speed},{acc}")
    positions[id - 1] = position

def get_com_ports():
    ports = list(serial.tools.list_ports.comports())
    return [port.device for port in ports]

def refresh_com_ports(com_ports_var, combobox):
    com_ports = get_com_ports()
    com_ports_var.set(com_ports)
    combobox['values'] = com_ports

def set_selected_port(port, device):
    global _selected_port, arduino_port, esp32_port
    _selected_port = port
    if device == "arduino":
        arduino_port = port
    elif device == "esp32":
        esp32_port = port

def get_selected_port():
    return _selected_port

def update_display(servo_id, voltage, current, temperature, pos, load):
    # Funkcja wywoływana z plot.py do aktualizacji Treeview
    pass  # Ta funkcja będzie implementowana w plot.py

def receive_data(serial_connection, callback):
    buffer = ""
    while running:
        if serial_connection is not None and serial_connection.is_open and serial_connection.in_waiting > 0:
            try:
                data = serial_connection.read(serial_connection.in_waiting).decode('utf-8')
                buffer += data
                while '<' in buffer and '>' in buffer:
                    start = buffer.index('<')
                    end = buffer.index('>')
                    message = buffer[start + 1:end]
                    buffer = buffer[end + 1:]
                    
                    values = message.split(',')
                    if len(values) == 6:
                        try:
                            servo_id = int(values[0])
                            voltage = float(values[1])
                            current = float(values[2])
                            temperature = float(values[3])
                            pos = int(values[4])
                            load = float(values[5])
                            callback(servo_id, voltage, current, temperature, pos, load)
                        except ValueError as e:
                            print(f"Błąd konwersji danych: {e}")
            except serial.SerialException as e:
                print(f"Błąd odczytu danych: {e}")

        time.sleep(0.1)

def start_receive_data_thread(callback):
    global running
    running = True
    arduino_thread = threading.Thread(target=lambda: receive_data(ser_arduino, callback), daemon=True)
    esp32_thread = threading.Thread(target=lambda: receive_data(ser_esp32, callback), daemon=True)
    arduino_thread.start()
    esp32_thread.start()

def stop_receiving():
    global running
    running = False
