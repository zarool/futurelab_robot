import os
import sys
import time
import threading

from app.gui import App
from camera.camera_read import start_capture


ENV_DISPLAY_CAMERA = ":0"
ENV_DISPLAY_APP = ":1"


def start_camera():

    os.environ["DISPLAY"] = ENV_DISPLAY_CAMERA
    print("[ ] Variable DISPLAY on camera process is", os.environ["DISPLAY"])
    print("[+] Started camera capture process. Saving frames to redis database")

    # possible args
    # display_w=800, display_h=500, capture_w=1280, capture_h=720, capture_fps=60, flip=2
    start_capture(display_w=600, display_h=500, capture_w=1280, capture_h=720, capture_fps=30, flip=2)


def start_app():

    os.environ["DISPLAY"] = ENV_DISPLAY_APP
    print("[ ] Variable DISPLAY on app process is", os.environ["DISPLAY"])
    print("[+] Started GUI app.")
    
    app = App()
    app.run()

if __name__ =="__main__":
    thread_camera = threading.Thread(target=start_camera, daemon=True, args=())
    thread_camera.start()

    time.sleep(1)

    start_app()
    