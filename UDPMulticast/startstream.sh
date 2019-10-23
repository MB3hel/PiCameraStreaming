#!/bin/bash

# This may sometimes need to change
MULTICAST_IP=224.0.0.1
DEST_PORT=5008

gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! rtph264pay ! udpsink host=$MULTICAST_IP auto-multicast=true port=$DEST_PORT

