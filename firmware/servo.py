from firmware.communication import Communicator

def move_to_position(communicator, pos1, pos2, pos3, pos4):
    try:
        communicator.move(1, pos1)
        communicator.move(2, pos2)
        communicator.move(3, pos3)
        communicator.move(4, pos4)
    except ValueError as e:
        print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")
