import customtkinter as ctk

# custom modules
from firmware.communication import Communicator
from app.gui import GUI


class App:
    def __init__(self) -> None:
        # gui root
        self.root = ctk.CTk()  # Użycie CTk zamiast Tk
        # robot instance
        self.gui = GUI(self.root)
        self.com = Communicator()

        # update buttons
        self.gui.btn_refresh_com.configure(command=self.refresh_com_ports)
        self.gui.btn_refresh_conn.configure(command=self.update_refresh_connection)
        self.gui.combo.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.gui.btn_compute.configure(command=self.update_robot)

    def run(self):
        self.gui.plot_robot(0, 0, 0, 0)

        self.update_refresh_connection()

        # start new thread
        self.com.start_receive_data_thread(self.gui.update_table_row)

        # update table each 100ms
        self.root.after(100, self.update_gui_table)

        self.root.mainloop()

    def update_robot(self):
        self.gui.update_robot(self.com)
        self.update_gui_table()

    # INTEGRATION COMMUNICATOR WITH GUI
    def update_gui_table(self):
        com_data = self.com.get_data()

        ids = com_data[0]
        voltages = com_data[1]
        currents = com_data[2]
        temperatures = com_data[3]
        positions = com_data[4]
        loads = com_data[5]

        for i in range(len(ids)):
            self.gui.update_table_row(ids[i], voltages[i], currents[i], temperatures[i], positions[i], loads[i])

    def on_combobox_select(self, event):
        selected_port = self.gui.com_ports.get()
        print(f"Selected COM port: {selected_port}")  # Dodaj logi debugujące
        self.com.set_selected_port(selected_port)

    def refresh_com_ports(self):
        com_ports = self.com.get_com_ports()
        print(f"Available COM ports: {com_ports}")  # Dodaj logi debugujące

        if len(com_ports) == 1:
            selected_port = com_ports[0]
            self.gui.com_ports.set(selected_port)
            self.gui.combo.set(selected_port)
            self.com.set_selected_port(selected_port)
            print(f"Automatically selected COM port: {selected_port}")
            self.update_refresh_connection()  # Automatyczne połączenie po wybraniu portu
        else:
            self.gui.com_ports.set(com_ports[0] if com_ports else '')
            self.gui.combo.configure(values=com_ports)

    def update_refresh_connection(self):
        connection_status = self.com.connect()
        if connection_status == 1:
            self.gui.btn_connection.set("Connected")
            self.gui.btn_refresh_conn.configure(fg_color='green')
        else:
            self.gui.btn_connection.set("Refresh Connection")
            self.gui.btn_refresh_conn.configure(fg_color='red')
            print("Connection failed.")
