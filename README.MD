# Raspberry Pi Camera Streaming

## Pi Setup
- Tested on Raspbian Buster
- Install gstreamer (1.0) and plugins

```
sudo apt install install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
- Tested with Pi Camera. Make sure to enable with `raspi-config`

## Linux Streaming Setup
- Tested on Ubuntu 18.04 (64-bit)
- Install gstreamer

```
install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

- Install VDAPU for decode of OMX stream from pi

```
sudo apt install gstreamer1.0-vaapi vdpau-va-driver vainfo
```

## Windows streaming setup
...
