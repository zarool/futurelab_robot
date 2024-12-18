#!/usr/bin/env python3

import cv2
import struct
import redis
import numpy as np

from camera.jetcam.csi_camera import CSICamera

def toRedis(r,a,n):
   """Store given Numpy array 'a' in Redis under key 'n'"""
   h, w = a.shape[:2]
   shape = struct.pack('>II',h,w)
   encoded = shape + a.tobytes()

   # Store encoded data in Redis
   r.set(n,encoded)
   return

if __name__ == '__main__':

    # Redis connection
    r = redis.Redis(host='localhost', port=6379, db=0)
    cam = CSICamera(capture_device=0, width=800, height=500, capture_width=1280, capture_height=720, capture_fps=60, flip=2)
    # cam1 = CSICamera(capture_device=1, width=500, height=400, capture_width=1536, capture_height=864, capture_fps=90)

    key = 0
    while key != 27:
        img = cam.read()
        # img1 = cam1.read()

        key = cv2.waitKey(1) & 0xFF
        toRedis(r, img, 'image')
        # toRedis(r, img1, 'image1')
