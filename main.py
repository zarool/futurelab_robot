import os
import time
import threading

from src.app.gui import App
from src.camera.camera_read import start_capture


DO_CHANGE_ENV = True
ENV_DISPLAY_CAMERA = ":0"
ENV_DISPLAY_APP = ":1"

#########################
# Camera modes for IMX708
# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [1536, 864, 10],
    [1536, 864, 90]
]

ENV_CAMERA = {
    "MODE": 0, 
    "DISPLAY_W": 600,
    "DISPLAY_H": 500,
    "FLIP": 0, # 0 or 2
    "EXPOSURE": 0, # <-2; 2>
    "TNR_STRENGTH" : 1,
    "WB_MODE": 1, # wyłączenie automatycznego balansu bieli
    "SATURATION": 1.0,
    "AUTO_EXPOSURE": False # Domyślnie brak blokadu autoekspozycji
}

def start_camera():

    if DO_CHANGE_ENV:
        os.environ["DISPLAY"] = ENV_DISPLAY_CAMERA
        print("[ ] Variable DISPLAY on camera process is", os.environ["DISPLAY"])
        print("[+] Started camera capture process. Saving frames to redis database")

    # possible args
    # display_w=800, display_h=500, capture_w=1280, capture_h=720, capture_fps=60, flip=2
    start_capture(display_w = ENV_CAMERA["DISPLAY_W"], 
                  display_h = ENV_CAMERA["DISPLAY_H"], 
                  capture_w = CAMERA_MODES[ENV_CAMERA["MODE"]][0], 
                  capture_h = CAMERA_MODES[ENV_CAMERA["MODE"]][1], 
                  capture_fps = CAMERA_MODES[ENV_CAMERA["MODE"]][2], 
                  flip = ENV_CAMERA["FLIP"],
                  exposure = ENV_CAMERA["EXPOSURE"],
                  tnr_strength = ENV_CAMERA["TNR_STRENGTH"],
                  wb_mode = ENV_CAMERA["WB_MODE"],
                  auto_exposure = ENV_CAMERA["AUTO_EXPOSURE"])


def start_app():
    if DO_CHANGE_ENV:
        os.environ["DISPLAY"] = ENV_DISPLAY_APP
        print("[ ] Variable DISPLAY on app process is", os.environ["DISPLAY"])
        print("[+] Started GUI app.")
    
    app = App(CAMERA_MODES[ENV_CAMERA["MODE"]][0], CAMERA_MODES[ENV_CAMERA["MODE"]][1])
    app.run()



if __name__ =="__main__":

    # start camera capture thread
    thread_camera = threading.Thread(target=start_camera, daemon=True, args=())
    thread_camera.start()

    # wait for camera thread to start
    time.sleep(1)

    # start GUI application
    start_app()
    