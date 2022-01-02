#!/usr/bin/env bash

SERVER_IP=0.0.0.0
SERVER_PORT=5008

VIDEO_DEVICE=/dev/video0
VIDEO_WIDTH=640
VIDEO_HEIGHT=480
VIDEO_FPS=30

MUX_STR="h264parse config-interval=-1 !mpegtsmux"
# MUX_STR="h264parse ! flvmux streamable=true"
# MUX_STR="rtph264pay ! rtpstreampay"

# Camera supporting native H.264 video output (ex. Pi Camera)
gst-launch-1.0 v4l2src device=${VIDEO_DEVICE} ! "video/x-h264,width=${VIDEO_WIDTH},height=${VIDEO_HEIGHT},framerate=${VIDEO_FPS}/1" ! $MUX_STR ! tcpserversink host=$SERVER_IP port=$SERVER_PORT
