import cv2
import numpy as np
from PIL import Image, ImageTk

import struct
import redis

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


        self.image0 = None
        self.image1 = None

        self.image_contour = None
        
        # UTILS
        self.utils = Utils()
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    def update_image_param(self, param):
        self.utils.threshold1 = param[0]
        self.utils.threshold2 = param[1]
        self.utils.max_area = param[2]
        self.utils.min_area = param[3]
        self.utils.brightness_v = param[4]
        self.utils.contrast_v = param[5]
        self.utils.lower_color = np.array([param[7], param[8], param[9]])
        self.utils.upper_color = np.array([param[10], param[11], param[12]])


    def processing(self, frame):
        # 1
        # image operations to get black and white contours
        frame = self.utils.masking(frame, self.utils.lower_color, self.utils.upper_color)
        frame, self.image_contour = Utils.get_contours(frame, [self.utils.threshold1, self.utils.threshold2],
                                                            self.utils.contrast_v, self.utils.brightness_v,
                                                            draw=self.contour)

        # 2
        # detecting squares from image and returning it with square contours
        # finals_contours = [index, x, y, w, h [straight rectangle around object], box corner points [box],
        # width [cm], height [cm], color]
        frame, final_contours = self.utils.detect_square(self.image_contour, frame, self.utils.min_area,
                                                              self.utils.max_area,
                                                              self.OBJECT_W, self.OBJECT_L)

        # 3
        # display detected rectangles and
        # display info about length, width and color
        self.utils.display_info(frame, final_contours, draw_detect=self.detect, draw_info=self.info)

        self.image_contour = cv2.resize(self.image_contour, (int(self.display_w / 2), int(self.display_h / 2)))

        # 4
        # todo returning picked image coordinates and color
        self.detected_object = self.utils.pick_object(frame, final_contours)

        return frame


    def start(self):
        
        self.image0 = fromRedis(self.redis, 'image0')
        self.image1 = fromRedis(self.redis, 'image1')

        self.image0 = self.processing(self.image0)
        self.image1 = self.processing(self.image1)


    def get_image(self):
        img0 = Image.fromarray(cv2.cvtColor(self.image0, cv2.COLOR_BGR2RGB))
        img1 = Image.fromarray(cv2.cvtColor(self.image1, cv2.COLOR_BGR2RGB))
        return img0, img1

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
