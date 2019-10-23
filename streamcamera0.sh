#!/bin/bash

# To send to one known client
#gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! rtph264pay ! udpsink host=192.168.1.105 port=5008

# Multicast so many (or unknown) client(s) can see the stream
#gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! rtph264pay ! udpsink host=224.0.0.1 auto-multicast=true port=5008

# TCP Server sink instead of UDP
gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! mpegtsmux ! tcpserversink host="0.0.0.0" port=5008
