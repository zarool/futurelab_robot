###################################
# Copy necessary files from repo  #
# to Jetson Nano via ssh          #
###################################

jetson_key="~/.ssh/jetson"

ssh -i $jetson_key -fMNS ssh-conn -o ControlPersist=yes orin@192.168.55.1
ssh orin@192.168.55.1 "mkdir -p ~/podwodny && mkdir -p ~/podwodny/src && mkdir -p ~/podwodny/utils"
scp -o ControlPath=ssh-conn -r *.py orin@192.168.55.1:~/podwodny/
scp -o ControlPath=ssh-conn -r src/* orin@192.168.55.1:~/podwodny/src/
scp -o ControlPath=ssh-conn -r utils/opencv-cuda-installer/* orin@192.168.55.1:~/podwodny/utils/
ssh -S ssh-conn -O exit -
