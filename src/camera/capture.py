import cv2
import numpy as np
from PIL import Image, ImageTk

import struct
import redis

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

def fromRedis(r,n):
   """Retrieve Numpy array from Redis key 'n'"""
   encoded = r.get(n)
   h, w = struct.unpack('>II',encoded[:8])
   a = np.frombuffer(encoded, dtype=np.uint8, offset=8).reshape(h,w,3)
   return a


class Camera:
    def __init__(self, mode):
        # system arguments default values
        self.cam_disp = 1#cam_disp
        self.contour = 0#contour
        self.detect = 1#detect
        self.info = 1#info
        self.current_img = 0#current

        # 0 - default, 2 - turn 180 [deg]
        self.FLIP = 0#flip
        # BOOL to don't open camera twice at beginning of program (used for changing exposure in set_exposure())
        self.RUN = False

        # display window size
        self.display_w = CAMERA_MODES[mode][0] #int(display_w)
        self.display_h = CAMERA_MODES[mode][1] #int(display_h)

        # CAPTURE MODE
        # all modes in main configuration script file
        self.WIDTH = CAMERA_MODES[mode][0]
        self.HEIGHT = CAMERA_MODES[mode][1]
        self.FPS = CAMERA_MODES[mode][2]

        # OBJECT TO DETECT
        self.OBJECT_W = 10#object_w  # [cm]
        self.OBJECT_L = 10#object_l  # [cm]

        self.detected_object = [0, 0, 0, 0, 0, 0]

        # OBJECT CAMERA
        self.devices = Devices(self.WIDTH, self.HEIGHT, self.display_w, self.display_h, self.FPS, self.FLIP)

        # OPENCV CAMERA OBJECT, VIDEO FROM THAT OBJECT, IMAGES TO READ FROM
        # self.camera, self.video, self.images = self.devices.prepare_devices(self.cam_disp)

        self.image = None
        self.image_contour = None
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

        # UTILS
        self.utils = Utils()

    def update_image_param(self, param):
        self.utils.threshold1 = param[0]
        self.utils.threshold2 = param[1]
        self.utils.max_area = param[2]
        self.utils.min_area = param[3]
        self.utils.brightness_v = param[4]
        self.utils.contrast_v = param[5]
        self.utils.lower_color = np.array([param[7], param[8], param[9]])
        self.utils.upper_color = np.array([param[10], param[11], param[12]])

        print(self.utils.exposure, param[6])
        self.update_image_exposure(param[6])

    def update_image_exposure(self, exposure_value):
        if exposure_value != self.utils.exposure:
            self.set_exposure(exposure_value)

    def set_exposure(self, value):
        if self.RUN:
            exp_value = value

            self.utils.exposure = exp_value
            # reset camera and create new one with different exposure
            self.camera.cap.release()
            self.camera = None
            self.camera = self.devices.init_camera(exposure=exp_value)

    def start(self):
        # self.image = None
        # 0
        # capturing video frame
        # if self.camera:
        #     self.image = self.camera.read()
        #     self.RUN = True
        # elif self.video:
        #     _, self.image = self.video.read()
        #     self.image = cv2.resize(self.image, (self.display_w, self.display_h))
        # else:
        #     # capturing image
        #     try:
        #         img = self.images[self.current_img]
        #         self.image = cv2.resize(img, (self.display_w, self.display_h))
        #     except IndexError:
        #         print('An error occurred while loading images.')
        # ===============

        self.image = fromRedis(self.redis, 'image')

        # 1
        # image operations to get black and white contours
        self.image = self.utils.masking(self.image, self.utils.lower_color, self.utils.upper_color)
        self.image, self.image_contour = Utils.get_contours(self.image, [self.utils.threshold1, self.utils.threshold2],
                                                            self.utils.contrast_v, self.utils.brightness_v,
                                                            draw=self.contour)

        # 2
        # detecting squares from image and returning it with square contours
        # finals_contours = [index, x, y, w, h [straight rectangle around object], box corner points [box],
        # width [cm], height [cm], color]
        self.image, final_contours = self.utils.detect_square(self.image_contour, self.image, self.utils.min_area,
                                                              self.utils.max_area,
                                                              self.OBJECT_W, self.OBJECT_L)

        # 3
        # display detected rectangles and
        # display info about length, width and color
        self.utils.display_info(self.image, final_contours, draw_detect=self.detect, draw_info=self.info)

        self.image_contour = cv2.resize(self.image_contour, (int(self.display_w / 2), int(self.display_h / 2)))

        # 4
        # todo returning picked image coordinates and color
        self.detected_object = self.utils.pick_object(self.image, final_contours)

    def get_image(self):
        img0 = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        img1 = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        return img0, img1

    def get_current_img(self):
        return self.current_img

    def next_img(self):
        if not self.cam_disp:
            self.current_img = self.current_img + 1 if self.current_img < (len(self.images) - 1) else 0
            # print(f"Current image: cam{self.current_img}.jpg")

    def previous_img(self):
        if not self.cam_disp:
            self.current_img = self.current_img - 1 if self.current_img > 0 else (len(self.images) - 1)
            # print(f"Current image: cam{self.current_img}.jpg")

    def close(self):
        # closing camera only if using it
        if self.camera is not None:
            self.camera.cap.release()
        elif self.video is not None:
            self.video.release()
        cv2.destroyAllWindows()

    def get_info(self):
        info = [bool(self.cam_disp),
                self.WIDTH, self.HEIGHT, self.FPS,
                bool(self.contour),
                bool(self.detect),
                bool(self.info),
                self.current_img]
        return info

    def get_object_info(self):
        return self.detected_object

    def __str__(self):
        return (
            f"========================\n"
            f"Running image processing program\n"
            f"Use camera: {bool(self.cam_disp)}\n"
            f"Camera stream resolution:\n"
            f"W = {self.WIDTH} | H = {self.HEIGHT} | FPS = {self.FPS}\n"
            f"Draw contour: {bool(self.contour)}\n"
            f"Draw rectangles: {bool(self.detect)}\n"
            f"Display info: {bool(self.info)}\n"
            f"Current image: cam{self.current_img}.jpg\n"
            f"========================\n")
