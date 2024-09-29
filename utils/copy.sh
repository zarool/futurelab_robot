###################################
# Copy necessary files from repo  #
# to Jetson Nano via ssh          #
###################################

jetson_key=$1

if [ -z $jetson_key ]; then
    ssh -fMNS ssh-conn -o ControlPersist=yes orin@192.168.55.1
    ssh -o ControlPath=ssh-conn orin@192.168.55.1 "mkdir -p ~/podwodny && mkdir -p ~/podwodny/src && mkdir -p ~/podwodny/utils"
    scp -o ControlPath=ssh-conn -r *.py orin@192.168.55.1:~/podwodny/
    scp -o ControlPath=ssh-conn -r src/* orin@192.168.55.1:~/podwodny/src/
    scp -o ControlPath=ssh-conn -r utils/opencv-cuda-installer/* orin@192.168.55.1:~/podwodny/utils/
    ssh -o ControlPath=ssh-conn orin@192.168.55.1 "chmod +x ~/podwodny/utils/installer.sh"
    ssh -S ssh-conn -O exit orin@192.168.55.1
    echo All files copied using password.
    exit 0
fi

ssh -i $jetson_key orin@192.168.55.1 "mkdir -p ~/podwodny && mkdir -p ~/podwodny/src && mkdir -p ~/podwodny/utils"
scp -i $jetson_key -r *.py orin@192.168.55.1:~/podwodny/
scp -i $jetson_key -r src/* orin@192.168.55.1:~/podwodny/src/
scp -i $jetson_key -r utils/opencv-cuda-installer/* orin@192.168.55.1:~/podwodny/utils/
ssh -i $jetson_key orin@192.168.55.1 "chmod +x ~/podwodny/utils/installer.sh"
echo All files copied using ssh key.
exit 0
