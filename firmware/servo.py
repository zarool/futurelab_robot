import firmware.communication as com
import src.kinematics as kin
import app.plot as pl


def move_to_position(pos1,pos2,pos3,pos4):
    try:
        com.move(1,pos1)
        com.move(2,pos2)
        com.move(3,pos3)
        com.move(4,pos4)
    except ValueError as e:
        print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")
