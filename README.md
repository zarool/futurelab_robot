## Dual camera with ssh test

### Copy [`jetson`](./jetson) folder to Nvidia Jetson Orin

```bash
cd futurelab 
ssh nvidia@192.168.55.1 "mkdir -p ~/dual-camera"
scp -r jetson nvidia@192.168.55.1:/home/nvidia/dual-camera
```
### Run program on Jetson

```bash
cd dual-camera
python3 capture.py
```

### Run program on local machine

```bash
python3 local/app.py
```
