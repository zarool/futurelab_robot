from firmware.communication import Communicator
import time

def move_to_position(communicator, pos1, pos2, pos3, pos4):
    #off_1, off_2, off_3, off_4 = pl.uptd_offset()
    try:
        if(pos3 < 150 or pos3 > 2000):
            raise ValueError("Ruch poza zakresem")
        if(pos4 < 1024):
            raise ValueError("Ruch poza zakresem")
        communicator.move(1, pos1)
        communicator.move(2, pos2)
        communicator.move(3, pos3)
        communicator.move(4, pos4)

        # communicator.move(1, (pos1 + off_1))
        # communicator.move(2, (pos2 + off_2))
        # communicator.move(3, (pos3 - off_3))
        # communicator.move(4, (pos4 - off_4))
        # communicator.move(5, (4096 - pos4 + off_4))

    except ValueError as e:
        print(f"Błąd konwersji współrzędnych lub punkt poza zasięgiem: {e}")

def transport_mode(communicator):
    communicator.move(2, 2048)
    communicator.move(3, 300)
    communicator.move(4, 2048)
    communicator.move(5, 2048)
    time.sleep(5)
    communicator.move(1, 2160)
    time.sleep(5)
    communicator.move(2, 3620)
    communicator.move(3, 350)
    communicator.move(4, 2048)
    communicator.move(5, 2048)