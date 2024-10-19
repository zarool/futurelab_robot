import serial
import serial.tools.list_ports
import threading
import time

# Inicjalizacja zmiennych globalnych
id = [1, 2, 3, 4, 5, 6]
voltage = [1.2, 1.3, 1.4, 1.5, 1.6, 1.7]
current = [2.3, 2.4, 2.5, 2.6, 2.7, 3]
temperature = [36.0, 37.0, 38.0, 39.0, 40.0, 40]
load = [1.5, 1.6, 1.7, 1.8, 1.9, 2]
speed = 150
acc = 150
arduino_baudrate = 9600
esp32_baudrate = 115200


class Driver:
    def __init__(self) -> None:
        self.running = True

        self.positions = [120, 130, 140, 150, 160, 200]

        self.connection_status = None
        self.selected_port = ""
        self.arduino_port = ""
        self.esp32_port = ""
        self.ser_arduino = None
        self.ser_esp32 = None

    def get_com_ports(self):
        ports = list(serial.tools.list_ports.comports())
        return [port.device for port in ports]

    def get_positions(self):
        return self.positions

    def move_camera(self, id_camera, position):
        id_camera = int(id_camera)
        position = int(position)
        self.send_command_camera(f"{id_camera},{position}")

    def send_command_camera(self, command):
        if command and self.ser_esp32 is not None and self.ser_esp32.is_open:
            try:
                full_command = f"*{command}*"
                self.ser_esp32.write(full_command.encode('utf-8') + b'\n')
                print(f"Wysłano komendę: {full_command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def send_command(self, command):
        if command and self.ser_arduino is not None and self.ser_arduino.is_open:
            try:
                full_command = f"({command})"
                self.ser_arduino.write(full_command.encode('utf-8') + b'\n')
                print(f"Wysłano komendę: {full_command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def connect_arduino(self):
        try:
            if self.ser_arduino is not None and self.ser_arduino.is_open:
                self.ser_arduino.close()
                print("Zresetowano połączenie z Arduino.")
            self.ser_arduino = serial.Serial(self.arduino_port, arduino_baudrate, timeout=1)
            print(f"Połączono z Arduino na porcie {self.arduino_port}")
            connection_status_arduino = 1
            self.running = True
            return connection_status_arduino
        except serial.SerialException as e:
            self.running = False
            print(f"Błąd połączenia: {e}")
            connection_status_arduino = 0
            return connection_status_arduino

    def connect_esp32(self):
        try:
            if self.ser_esp32 is not None and self.ser_esp32.is_open:
                self.ser_esp32.close()
                print("Zresetowano połączenie z ESP32.")
            self.ser_esp32 = serial.Serial(self.esp32_port, esp32_baudrate, timeout=1)
            print(f"Połączono z ESP32 na porcie {self.esp32_port}")
            connection_status_esp32 = 1
            self.running = True
            return connection_status_esp32
        except serial.SerialException as e:
            self.running = False
            print(f"Błąd połączenia: {e}")
            connection_status_esp32 = 0
            return connection_status_esp32

    def move(self, id, position):
        id = int(id)
        position = int(position)
        self.send_command(f"{id},{position},{speed},{acc}")
        self.positions[id - 1] = position

    def move_to_position(self, pos1, pos2, pos3, pos4, off_1, off_2, off_3, off_4):
        try:
            if(pos3 < 150 or pos3 > 2000):
                raise ValueError("Ruch poza zakresem")
            if(pos4 < 1024):
                raise ValueError("Ruch poza zakresem")
                self.move(1, (pos1 + off_1))
                self.move(2, (pos2 + off_2))
                self.move(3, (pos3 - off_3))
                self.move(4, (pos4 - off_4))
                self.move(5, (4096 - pos4 + off_4))

        except ValueError as e:
            print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")

    def set_selected_port(self, port, device):
        self.selected_port = port
        if device == "arduino":
            self.arduino_port = port
        elif device == "esp32":
            self.esp32_port = port

    def get_selected_port(self):
        return self.selected_port

    def get_data(self):
        return id, voltage, current, temperature, self.positions, load

    def receive_data(self, serial_connection, callback):
        buffer = ""
        while self.running:
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


    def start_receive_data_thread(self, callback):
        self.running = True
        arduino_thread = threading.Thread(target=lambda: self.receive_data(self.ser_arduino, callback), daemon=True)
        esp32_thread = threading.Thread(target=lambda: self.receive_data(self.ser_esp32, callback), daemon=True)
        arduino_thread.start()
        esp32_thread.start()

    def stop_receiving(self):
        self.running = False



# def refresh_com_ports(com_ports_var, combobox):
#     com_ports = get_com_ports()
#     com_ports_var.set(com_ports)
#     combobox['values'] = com_ports
