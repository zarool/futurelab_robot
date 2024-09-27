###################################
# Copy necessary files from repo  #
# to Jetson Nano via ssh          #
###################################

# scp src/* orin@192.168.55.1:/podwodny/src/

ssh -fMNS ssh-conn -o ControlPersist=yes orin@192.168.55.1
ssh orin@192.168.55.1 "mkdir ~/podwodny && mkdir ~/podwodny/src && mkdir ~/podwodny/src/jetson-utilities"
scp -o ControlPath=ssh-conn *.py orin@192.168.55.1:~/podwodny/
scp -o ControlPath=ssh-conn src/* orin@192.168.55.1:~/podwodny/src/
scp -o ControlPath=ssh-conn jetson-utilities/opencv-cuda-installer/* orin@192.168.55.1:~/podwodny/jetson-utilities/
ssh -S ssh-conn -O exit -
