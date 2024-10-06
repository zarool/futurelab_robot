import communication as com
import kinematics as kin
import plot as pl
import time
from communication import positions



def move_to_position(pos1,pos2,pos3,pos4):
    off_1, off_2, off_3, off_4 = pl.uptd_offset()
    try:
        if(pos3 < 150 or pos3 > 2000):
            raise ValueError("Ruch poza zakresem")
        if(pos4 < 1024):
            raise ValueError("Ruch poza zakresem")
        com.move(1, (pos1 + off_1))
        com.move(2, (pos2 + off_2))
        com.move(3, (pos3 - off_3))
        com.move(4, (pos4 - off_4))
        com.move(5, (4096 - pos4 + off_4))

    except ValueError as e:
        print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")

def transport_mode():
    com.move(2, 2048)
    com.move(3, 300)
    com.move(4, 2048)
    com.move(5, 2048)
    time.sleep(5)
    com.move(1, 2160)
    time.sleep(5)
    com.move(2, 3620)
    com.move(3, 350)
    com.move(4, 2048)
    com.move(5, 2048)




