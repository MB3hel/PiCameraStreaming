#!/usr/bin/env bash

########################################################################################################################
# Stream / Network Settings
########################################################################################################################

# Output URL. TCP:
# TCP = tcp://[IP_ADDR]:[PORT]\?listen
# mkvserver_mk2: tcp://localhost:[PORT]
# UDP = udp://[IP_ADDR]:[PORT]
OUTPUT_URL=tcp://0.0.0.0:5008\?listen


########################################################################################################################
# Video input settings
########################################################################################################################

# Which camera to stream video from. List available devices with
# v4l2-ctl --list-devices
VID_DEV=/dev/video0

# What format to capture data from the camera in
# Not all cameras support the same formats. List using
# ffplay -f v4l2 -list_formats all /dev/video[#]
# Most commonly:
#    Raw input:     yuyv422
#    MJPEG input:   mjpeg
#    H.264 input:   h264
VID_IN_FMT=yuyv422

# Video mode settings (resolution and framerate)
# Supported values depend on the camera and the selected input format
VID_WID=640
VID_HEI=480
VID_FPS=60


########################################################################################################################
# Stream encoding settings
########################################################################################################################

# What codec to encode the data from the camera in
# This determines what data is streamed. Generally, using either H.264 or mjpeg is recommended
#
# Generally, MJPEG will be easier to encode and thus be lower latency. However, 
# H.264 will be lower bandwidth and allow higher framerates and resolutions.
# If using hardware accelerated H.264 encoding (such as OMX H.264 on the Pi) the 
# latency should not be an issue. Also, if the camera is providing H.264 data no 
# encoding needs to happen, thus latency is not an issue. If the camera does not provide H.264 data 
# and hardware accelerated encoding is not available, libx264 can be used for software encoding.
# Using certain options, the latency should not be too bad, but the CPU usage could be an 
# issue on lower power devices. As such, an mjpeg stream may be preferable.
#
# Encoding mjpeg (even if not hardware accelerated) will be less demanding than encoding H.264
#
# copy = keep same format as camera data
# mjpeg = Encode mjpeg
# libx264 = Encode H.264 using libx264
# h264_omx = Encode H.264 using OMX hardware (Raspberry Pi)
STREAM_CODEC=h264_omx

# Extra options to configure the selected codec
# See https://ffmpeg.org/ffmpeg-codecs.html for details
#
# Recommendations
# libx264: tune=zerolatency speed-preset=ultrafast
# mjpeg: -q:v [2-31] (quality of JPEG images, 2 = best quality, 31 = small size)
#
# For "copy" and "h264_omx" likely nothing is needed here
CODEC_OPTS=""


########################################################################################################################
# Stream container settings
########################################################################################################################

# Stream can either use a container for the video or it can contain raw video
# Latency is often better using raw video (no container), however using a container 
# can be more compatible or required for some networking setups (server, udp, etc)
# See https://ffmpeg.org/ffmpeg-formats.html#Muxers for details
#
# Raw containers (recommended to use with TCP):
# mjpeg for mjpeg streams
# h264 for h264 streams
#
# Recommended Containers for Streaming (if not using raw):
# mpegts
# flv
# matroska (use with mkvserver_mk2)
STREAM_MUX=h264


########################################################################################################################
# Run command
########################################################################################################################

ffmpeg \
    -f v4l2 -input_format ${VID_IN_FMT} -video_size ${VID_WID}x${VID_HEI} -framerate ${VID_FPS} -i ${VID_DEV} \
    -an -c:v ${STREAM_CODEC} ${CODEC_OPTS} -r ${VID_FPS} \
    -f ${STREAM_MUX} ${OUTPUT_URL}
