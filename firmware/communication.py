import serial as ser
import serial.tools.list_ports
import threading
import time

# Inicjalizacja zmiennych globalnych
id = [1, 2, 3, 4, 5]
voltage = [1.2, 1.3, 1.4, 1.5, 1.6]
current = [2.3, 2.4, 2.5, 2.6, 2.7]
temperature = [36.0, 37.0, 38.0, 39.0, 40.0]
positions = [120, 130, 140, 150, 160]
load = [1.5, 1.6, 1.7, 1.8, 1.9]
speed = 1000
acc = 1000

connection_status = None
_selected_port = ""
arduino_port = ""
arduino_baudrate = 115200
running = True
ser = None  # Inicjalizowanie zmiennej do portu szeregowego

def send_command(command):
    if command and ser is not None and ser.is_open:
        try:
            ser.write(command.encode('utf-8') + b'\n')  # Wysyłanie komendy przez port szeregowy
            print(f"Wysłano komendę: {command}")
        except serial.SerialException as e:
            print(f"Błąd wysyłania komendy: {e}")

def connect():
    global connection_status, ser, arduino_port, running
    try:
        ser = serial.Serial(arduino_port, arduino_baudrate, timeout=1)
        print(f"Połączono z Arduino na porcie {arduino_port}")
        connection_status = 1
        running = True
        return connection_status
    except serial.SerialException as e:
        running = False
        print(f"Błąd połączenia: {e}")
        connection_status = 0
        return connection_status

def move(id, position):
    send_command(f"np {id},{position},{speed},{acc}")
    positions[id - 1] = position

def get_com_ports():
    ports = list(serial.tools.list_ports.comports())
    return [port.device for port in ports]

def refresh_com_ports(com_ports_var, combobox):
    com_ports = get_com_ports()
    com_ports_var.set(com_ports)
    combobox['values'] = com_ports

def set_selected_port(port):
    global _selected_port, arduino_port
    _selected_port = port
    arduino_port = port

def get_selected_port():
    return _selected_port

def update_display(servo_id, voltage, current, temperature, pos, load):
    # Funkcja wywoływana z plot.py do aktualizacji Treeview
    pass  # Ta funkcja będzie implementowana w plot.py

def receive_data(callback):
    global ser, running
    while running:
        if ser is not None and ser.is_open and ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line.startswith("ID:"):
                    data = line.split(", ")
                    if len(data) >= 6:  # Sprawdzenie, czy są wystarczające elementy w liście data
                        servo_id = int(data[0].split(": ")[1])
                        voltage_str = data[1].split(": ")[1].rstrip('V')  # Usunięcie jednostki 'V' z końca
                        current_str = data[2].split(": ")[1].rstrip('A')  # Usunięcie jednostki 'A' z końca
                        temperature_str = data[3].split(":")[1].rstrip('C')  # Usunięcie jednostki 'C' z końca
                        pos_str = data[4].split(":")[1].rstrip('x')
                        load_str = data[5].split(":")[1].rstrip('x')
                        try:
                            voltage = float(voltage_str) / 10.0  # Przesunięcie wartości napięcia o jedno miejsce dziesiętne w lewo
                            current = float(current_str) / 10.0  # Przesunięcie wartości prądu o jedno miejsce dziesiętne w lewo
                            temperature = float(temperature_str) / 1.0  # Przesunięcie wartości temperatury o jedno miejsce dziesiętne w lewo
                            pos = int(pos_str)  # Konwersja pozycji na liczbę całkowitą
                            load = float(load_str) / 1.0
                            # Wywołanie funkcji callback z danymi
                            callback(servo_id,voltage,current,temperature,pos,load)
                        except ValueError as e:
                            print(f"Błąd konwersji danych: {e}")
            except serial.SerialException as e:
                print(f"Błąd odczytu danych: {e}")

        time.sleep(0.1) 

def start_receive_data_thread(callback):
    global running
    running = True
    thread = threading.Thread(target=lambda: receive_data(callback), daemon=True)
    
    thread.start()

def stop_receiving():
    global running
    running = False
