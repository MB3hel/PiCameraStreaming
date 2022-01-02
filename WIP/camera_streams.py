#!/usr/bin/env python3

from enum import Enum, auto
import os

class StreamTypes(Enum):
    TCP_MPEGTS = auto()
    TCP_FLV = auto()
    # UDP_UNICAST = auto()
    # UDP_MULTICAST = auto()


class StreamFormats(Enum):
    MJPEG = auto()
    H264 = auto()


class InputFormats(Enum):
    RAW = auto()
    MJPEG = auto()
    H264 = auto()


class Encoders(Enum):
    NONE = auto()
    OMXH264 = auto()
    LIBX264 = auto()
    JPEGENC = auto()


################################################################################
# Settings
################################################################################

VIDEO_DEVICE = "/dev/video0"
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_FPS = 30

# Options are auto, rw, mmap, userptr, dmabuf, dmabuf-import
# Generally use auto.
# If bad latency with USB camera try dmabuf
V4L2_IOMODE="auto"

IP_ADDRESS="0.0.0.0"
PORT=5008

INPUT_FORMAT = InputFormats.H264
ENCODER = Encoders.NONE
STREAM_FORMAT = StreamFormats.H264
STREAM_TYPE = StreamTypes.TCP_MPEGTS


################################################################################
# Helper functions
################################################################################

def input_pipeline(input_format: InputFormats, width: int, height: int, fps: int) -> str:
    fmt = ""
    if(input_format == InputFormats.RAW):
        fmt = "video/x-raw"
    elif(input_format == InputFormats.H264):
        fmt = "video/x-h264"
    elif(input_format == InputFormats.MJPEG):
        fmt = "image/jpeg"
    else:
        raise Exception("Unknown input format!")
    return "{0},width={1},height={2},framerate={3}/1".format(fmt, width, height, fps)

def encoder_pipeline(input_format: InputFormats, encoder: Encoders, stream_format: StreamFormats) -> str:
    if(encoder == Encoders.NONE):
        if(input_format == InputFormats.H264 and stream_format == StreamFormats.H264):
            return "identity"
        elif(input_format == InputFormats.MJPEG and stream_format == StreamFormats.MJPEG):
            return "identity"
    elif(encoder == Encoders.OMXH264 and stream_format == StreamFormats.H264):
        if(input_format == InputFormats.MJPEG):
            return "jpegdec ! omxh264enc"
        elif(input_format == InputFormats.RAW):
            return "omxh264enc"
    elif(encoder == Encoders.LIBX264 and stream_format == StreamFormats.H264):
        if(input_format == InputFormats.MJPEG):
            return "jpegdec ! x264enc tune=zerolatency speed-preset=ultrafast"
        elif(input_format == InputFormats.RAW):
            return "x264enc tune=zerolatency speed-preset=ultrafast"
    elif(encoder == Encoders.JPEGENC and stream_format == StreamFormats.MJPEG):
        if(input_format == InputFormats.H264):
            return "v4l2h264dec ! jpegenc"
        elif(input_format == InputFormats.RAW):
            return "jpegenc"

    raise Exception("Invalid encoder for given input and stream formats!")

def output_pipeline(stream_type: StreamTypes, stream_format: StreamFormats) -> str:
    mux = ""
    if(stream_type == StreamTypes.TCP_MPEGTS):
        if(stream_format == StreamFormats.MJPEG):
            mux = "mpegtsmux"
        elif(stream_format):
            mux = "h264parse config-interval=-1 ! mpegtsmux"
        else:
            raise Exception("Unknown stream format!")
    elif(stream_type == StreamTypes.TCP_FLV):
        if(stream_format == StreamFormats.MJPEG):
            mux = "flvmux streamable=true"
        elif(stream_format):
            mux = "h264parse config-interval=-1 ! flvmux streamable=true"
        else:
            raise Exception("Unknown stream format!")
    else:
        raise Exception("Unknown stream type!")
    
    if(stream_type == StreamTypes.TCP_MPEGTS or stream_type == StreamTypes.TCP_FLV):
        return "{0} ! tcpserversink host={1} port={2}".format(mux, IP_ADDRESS, PORT)
    else:
        raise Exception("Unknown stream type!")

if __name__ == "__main__":
    inpipe = input_pipeline(INPUT_FORMAT, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS)
    encpipe = encoder_pipeline(INPUT_FORMAT, ENCODER, STREAM_FORMAT)
    outpipe = output_pipeline(STREAM_TYPE, STREAM_FORMAT)
    pipeline = "gst-launch-1.0 v4l2src device={0} ! {1} ! {2} ! {3}".format(VIDEO_DEVICE, inpipe, encpipe, outpipe)
    print(pipeline)