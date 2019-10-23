#!/bin/bash

# Set server IP and port. Use IP address 0.0.0.0 for the server to be accessible on all interfaces (via any IP)
SERVER_IP=0.0.0.0
SERVER_PORT=5008

gst-launch-1.0 v4l2src device=/dev/video0 ! 'video/x-raw,width=640,height=480' ! omxh264enc ! mpegtsmux ! tcpserversink host=$SERVER_IP port=$SERVER_PORT
