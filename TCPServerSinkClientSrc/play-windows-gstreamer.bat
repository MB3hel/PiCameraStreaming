#!/bin/bash

# Server's IP address and port number
set SERVER_IP=192.168.1.113
set SERVER_PORT=5008

gst-launch-1.0 tcpclientsrc host=%SERVER_IP% port=%SERVER_PORT% ! tsdemux ! h264parse ! avdec_h264 ! autovideosink sync=false
