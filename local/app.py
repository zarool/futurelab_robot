import cv2
import time
import paramiko
from scp import SCPClient
from skimage import io
import numpy
from io import StringIO
import PIL.Image
import os


# Function to create SSH connection to remote machine
def create_ssh_client(hostname, port, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, password=password)

    # Set SSH keep-alive interval to avoid broken pipe
    ssh_client.get_transport().set_keepalive(30)  # Sends a keepalive every 30 seconds

    return ssh_client


# Function to fetch the captured frame from remote machine with retry logic
def fetch_frame_from_remote_with_retry(ssh_client, frames, max_retries=5):
    attempt = 0
    while attempt < max_retries:
        try:
            scp = SCPClient(ssh_client.get_transport())
            for frame in frames:
                scp.get(f'/tmp/{frame}', f'{frame}')
            scp.close()
            return True
        except Exception as e:
            print(f"Error during SCP transfer: {e}. Retrying...")
            attempt += 1
            time.sleep(2)  # Wait for 2 seconds before retrying
    return False

# Function to display the video stream from the received frames
def display_video_stream(ssh_client, frames):
    while True:
        # Fetch the latest frame from the remote machine with retries
        if fetch_frame_from_remote_with_retry(ssh_client, frames):
            for frame_name in frames:
                with open(frame_name, 'rb') as im:
                    im.seek(-2, 2)
                    if im.read() == b'\xff\xd9':
                        print('Image OK :', frame_name)
                    else:
                        # fix image
                        img = cv2.imread(frame_name)
                        cv2.imwrite(frame_name, img)
                        print('FIXED corrupted image :', frame_name)

                frame = cv2.imread(frame_name)

                if frame is not None:
                    cv2.imshow(f"{frame_name}", frame)

            time.sleep(0.5)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


# Local machine info
hostname = '192.168.55.1'  # Remote machine's IP address
port = 22  # SSH port (default is 22)
username = 'nvidia'  # Username for remote machine
password = 'nvidia'  # Password for remote machine
names = ['captured_frame0.jpg', 'captured_frame1.jpg']

if __name__ == "__main__":
    # Create SSH client to connect to the remote machine
    ssh_client = create_ssh_client(hostname, port, username, password)

    # Start displaying the video stream
    display_video_stream(ssh_client, names)

    # Close the SSH connection when done
    ssh_client.close()
