import cv2
import os
import time

from jetcam.csi_camera import CSICamera

# Function to capture video from the camera and store frames
def capture_video_and_save():
    cameras = [
        CSICamera(capture_device=0, width=600, height=400, capture_width=1536, capture_height=864, capture_fps=90),
        CSICamera(capture_device=1, width=600, height=400, capture_width=1536, capture_height=864, capture_fps=90)
        ]

    while True:
        # Capture a frame

        for camera in cameras:

            frame = camera.read()
            if not frame:
                print(f"Error: Could not read frame from camera - id: {camera.capture_device}.")
                break

            # Save the captured frame as a temporary file
            cv2.imwrite(f'/tmp/captured_frame{camera.capture_device}.jpg', frame)

        # Add a small delay to simulate real-time streaming
        time.sleep(0.5)

capture_video_and_save()
