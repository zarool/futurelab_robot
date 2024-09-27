# Update OpenCV ze wsparciem CUDA oraz GSTREAMER

Update zajmuje ~3h, kawa do umilenia czasu obowiązkowa ☕

W pliku `installer.sh` należy zmienić
  - `-D CUDA_ARCH_BIN=8.9`
  - `-D CUDNN_VERSION='8.9'`

Jeżeli chcemy zainstalować inną wersję CUDA, uruchamiamy skrypt z poziomu Orina w folderze `podwodny`

```bash
export OPENCV_VERSION=4.8.0 # opcjonalnie, jeżeli konieczna konkretna wersja
sudo jetson-utilities/installer.sh $OPENCV_VERSION
```
