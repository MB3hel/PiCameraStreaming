#!/bin/bash

# Playback for UDP (multicast or direct)
#gst-launch-1.0 udpsrc port=5008 ! "application/x-rtp, payload=127" ! rtph264depay vaapih264dec ! xvimagesink sync=false

# Playback for TCP
gst-launch-1.0 tcpclientsrc host=192.168.1.113 port=5008 ! tsdemux ! h264parse ! vaapih264dec ! xvimagesink sync=false
