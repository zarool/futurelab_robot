import serial as ser
import serial.tools.list_ports
import threading
import time

class Communicator:
    def __init__(self) -> None:
        # Inicjalizacja zmiennych globalnych
        self.id = [1, 2, 3, 4, 5]
        self.voltage = [1.2, 1.3, 1.4, 1.5, 1.6]
        self.current = [2.3, 2.4, 2.5, 2.6, 2.7]
        self.temperature = [36.0, 37.0, 38.0, 39.0, 40.0]
        self.positions = [120, 130, 140, 150, 160]
        self.load = [1.5, 1.6, 1.7, 1.8, 1.9]
        self.speed = 1000
        self.acc = 1000

        self.connection_status = None
        self.selected_port = ""
        self.arduino_port = ""
        self.arduino_baudrate = 115200
        self.running = True
        self.ser = None  # Inicjalizowanie zmiennej do portu szeregowego

    def connect(self):
        try:
            self.ser = serial.Serial(self.arduino_port, self.arduino_baudrate, timeout=1)
            print(f"Połączono z Arduino na porcie {self.arduino_port}")
            self.connection_status = 1
            self.running = True
            return self.connection_status
        except serial.SerialException as e:
            self.running = False
            print(f"Błąd połączenia: {e}")
            self.connection_status = 0
            return self.connection_status

    def send_command(self, command):
        if command and self.ser is not None and self.ser.is_open:
            try:
                self.ser.write(command.encode('utf-8') + b'\n')  # Wysyłanie komendy przez port szeregowy
                print(f"Wysłano komendę: {command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def send_command_camera(self, command):
        if command and ser_esp32 is not None and ser_esp32.is_open:
            try:
                full_command = f"*{command}*"
                ser_esp32.write(full_command.encode('utf-8') + b'\n')
                print(f"Wysłano komendę: {full_command}")
            except serial.SerialException as e:
                print(f"Błąd wysyłania komendy: {e}")

    def move_camera(self, id_camera, position):
        id_camera = int(id_camera)
        position = int(position)
        self.send_command_camera(f"{id_camera},{position}")


    def move(self, id, position):
        self.send_command(f"np {id},{position},{self.speed},{self.acc}")
        self.positions[id - 1] = position

    def get_com_ports(self):
        ports = list(serial.tools.list_ports.comports())
        return [port.device for port in ports]

    def refresh_com_ports(self, com_ports_var, combobox):
        com_ports = self.get_com_ports()
        com_ports_var.set(com_ports)
        combobox['values'] = com_ports

    def set_selected_port(self, port):
        self.selected_port = port
        self.arduino_port = port

    def get_selected_port(self):
        return self.selected_port

    def update_display(self, servo_id, voltage, current, temperature, pos, load):
        # Funkcja wywoływana z plot.py do aktualizacji Treeview
        pass  # Ta funkcja będzie implementowana w plot.py

    def receive_data(self, callback):
        while self.running:
            if self.ser is not None and self.ser.is_open and self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
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
                                callback(servo_id, voltage, current, temperature, pos, load)
                            except ValueError as e:
                                print(f"Błąd konwersji danych: {e}")
                except serial.SerialException as e:
                    print(f"Błąd odczytu danych: {e}")

            time.sleep(0.1)

    def start_receive_data_thread(self, callback):
        self.running = True
        thread = threading.Thread(target=lambda: self.receive_data(callback), daemon=True)
        thread.start()

    def stop_receiving(self):
        self.running = False

    def get_data(self):
        return [self.id,
            self.voltage,
            self.current,
            self.temperature,
            self.positions,
            self.load]
