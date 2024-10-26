import os
import cv2
from camera.jetcam.csi_camera import CSICamera


class Devices:
    def __init__(self, width, height, display_w, display_h, fps, flip, exposure=0.0):
        self.width = width
        self.height = height
        self.fps = fps
        self.flip = flip
        self.exposure = exposure

        self.display_w = display_w
        self.display_h = display_h

    def init_camera(self, exposure=0.0):
        return CSICamera(width=self.display_w, height=self.display_h, capture_width=self.width,
                         capture_height=self.height,
                         capture_fps=self.fps,
                         flip=self.flip, exposure=exposure)

    def prepare_devices(self, cam_disp):
        cam = None
        vid = None
        images_a = []
        if cam_disp:
            try:
                # init external camera as jetcam object
                cam = self.init_camera()
                print("\nUsing external camera.")
            except Exception as e:
                # if not, check for built-in camera
                print(e)
                print("\nUsing build-in webcam.")
                vid = cv2.VideoCapture(0)
        else:
            try:
                # if not using camera, use photos in images folder
                files = os.listdir("./images/")
                size = len(files)
                for index in range(0, size):
                    images_a.append(cv2.imread(f"./images/cam{index}.jpg"))
            except FileNotFoundError:
                print("Could not read the 'images' folder, none images received.")

        return cam, vid, images_a
