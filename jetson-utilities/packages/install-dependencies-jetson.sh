#!bin/bash
##################################
# Instal necessary dependencies  #
# for futurelab project          #
##################################

sudo apt install python3-pil python3-pil.imagetk
python3 -m pip install -r requirements.txt

# check if cv2 is installed


# opencv2 is not installed with gstreamer
is_gstreamer=python3 -c "import cv2;print(cv2.getBuildInformation())" | grep "GStreamer:" | cut -f2 -d":" | tr -d " "

