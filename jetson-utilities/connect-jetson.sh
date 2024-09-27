ssh-key-path=$1

# TODO
# check if jetson-klucz.pub exist in ~/.ssh/

ssh -i $ssh-key-path orin@192.168.55.1
