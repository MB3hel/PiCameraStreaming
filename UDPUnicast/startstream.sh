#!/bin/bash

# The IP and Port to send the packets to (UDP Unicast destination)
DEST_IP=192.168.1.105
DEST_PORT=5008

gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! rtph264pay ! udpsink host=$DEST_IP port=$DEST_PORT
