# Raspberry Pi Camera Streaming

## Setup

### Pi Setup
- Tested on Raspbian Buster
- Install gstreamer (1.0) and plugins

```
sudo apt install install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```
- Tested with Pi Camera. Make sure to enable with `raspi-config`

### Linux Streaming Setup
- Tested on Ubuntu 18.04 (64-bit)
- Install gstreamer

```
install libgstreamer1.0-0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

- Install VDAPU for decode of OMX stream from pi

```
sudo apt install gstreamer1.0-vaapi vdpau-va-driver vainfo
```

### Windows streaming setup
- Use the following ffplay command

```
ffplay -fflags nobuffer -probesize 32 -flags low_delay -framedrop tcp://HOST_NAME:PORT_NUMBER/
```


## Communication Protocols

#### UDP Unicast
Payload encodes H.264 video into RTP packets to be sent to a single computer over UDP (this means that the IP of the target compuer must be known). This is fast, but there is high risk for packet loss (and video freezing) if network issues occur. However, when the network recovers the stream will resume at the time of recovery (it will not have to send lost packets first).

#### UDP Multicast
Same idea as UDP unicast, however it sends the data to a port for all client computers on the network (any IP) so the host's IP does not have to be known. I did notice an increaced delay and packet loss when using multicast as compared to unicast. Same type of behavior if network issues occur.

#### TCP Server/Client
TCP allows for a Client/Server concept. This means that the client must know the address of the server. Gstreamer allows either the video sink (where the pi puts the encoded video) or the video source (where the computer gets the encoded video from) to be a server. If the sink is the server (meaning the server runs on the pi) then the computer must know the Pi's IP address. This is often more useful than having the Pi know the target computer's address. RTP does not work over TCP so an MPEG-TS container is used to mux the H.264 encoded video. This seems to be about the same speed as UDP Unicast. TCP ensures that all packets arrive and that they arrive in order. This means that if network interferecne slows or freezes the stream it will retry sending lost packets instead of sending new frames. This can lead to a delay after resuming the stream or the client may just disconnect and have to be restarted.
