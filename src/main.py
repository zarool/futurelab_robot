import os
import time
import threading

from app.gui import App
from camera.camera_read import start_capture


ENV_DISPLAY_CAMERA = ":0"
ENV_DISPLAY_APP = ":1"


#########################
# Camera modes for IMX708

# DO ZMODYFIKOWANIA ZGODNIE Z OUTPUTEM KOMENDY `v4l2-ctl --list-formats-ext` 

# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [1536, 864, 10],
    [1536, 864, 90],
    [1920, 1090, 30],
    [1640, 1232, 30],
    [1280, 720, 60],
    [1280, 720, 120]
]
ENV_CAMERA_MODE = 0


def start_camera():

    os.environ["DISPLAY"] = ENV_DISPLAY_CAMERA
    print("[ ] Variable DISPLAY on camera process is", os.environ["DISPLAY"])
    print("[+] Started camera capture process. Saving frames to redis database")

    # possible args
    # display_w=800, display_h=500, capture_w=1280, capture_h=720, capture_fps=60, flip=2
    start_capture(display_w = 600, display_h = 500, 
                  capture_w = CAMERA_MODES[ENV_CAMERA_MODE][0], 
                  capture_h = CAMERA_MODES[ENV_CAMERA_MODE][1], 
                  capture_fps = CAMERA_MODES[ENV_CAMERA_MODE][2], 
                  flip = 2)


def start_app():

    os.environ["DISPLAY"] = ENV_DISPLAY_APP
    print("[ ] Variable DISPLAY on app process is", os.environ["DISPLAY"])
    print("[+] Started GUI app.")
    
    app = App(CAMERA_MODES[ENV_CAMERA_MODE][0], CAMERA_MODES[ENV_CAMERA_MODE][1])
    app.run()



if __name__ =="__main__":

    # start camera capture thread
    thread_camera = threading.Thread(target=start_camera, daemon=True, args=())
    thread_camera.start()

    # wait for camera thread to start
    time.sleep(1)

    # start GUI application
    start_app()
    