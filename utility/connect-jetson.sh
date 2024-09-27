ssh_key_path=$1

# TODO
# check if jetson-key.pub exist in ~/.ssh/

ssh -i $ssh_key_path orin@192.168.55.1
