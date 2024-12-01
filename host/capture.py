

import cv2
import os
import time

from jetcam.csi_camera import CSICamera

# Function to capture video from the camera and store frames
def capture_video_and_save():
    camera0 = CSICamera(capture_device=0, width=600, height=400, capture_width=1536, capture_height=864, capture_fps=90)
    camera1 = CSICamera(capture_device=1, width=600, height=400, capture_width=1536, capture_height=864, capture_fps=90)


    while True:
        # Capture a frame
        frame0 = camera0.read()
        frame1 = camera1.read()
        # if not ret:
        #     print("Error: Could not read frame.")
        #     break

        # Save the captured frame as a temporary file
        cv2.imwrite('/tmp/captured_frame0.jpg', frame0)
        cv2.imwrite('/tmp/captured_frame1.jpg', frame1)

        # Add a small delay to simulate real-time streaming
        time.sleep(0.5)

    # Release the video capture object
    # cap.release()


# Main logic
if __name__ == "__main__":
    capture_video_and_save()
