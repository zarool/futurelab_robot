import cv2
import numpy as np

from camera.processing.device import Devices
from camera.processing.utils import Utils

# [WIDTH, HEIGHT, FPS]
CAMERA_MODES = [
    [3264, 2454, 21],
    [3264, 1848, 28],
    [1920, 1090, 30],
    [1640, 1232, 30],
    [1280, 720, 60],
    [1280, 720, 120]
]

class Camera:
    def __init__(self, mode) -> None:

        # CAPTURE MODE
        # all modes in main configuration script file
        self.WIDTH = CAMERA_MODES[mode][0]
        self.HEIGHT = CAMERA_MODES[mode][1]
        self.FPS = CAMERA_MODES[mode][2]


        self.devices = Devices(self.WIDTH, self.HEIGHT, self.display_w, self.display_h, self.FPS, self.FLIP)
