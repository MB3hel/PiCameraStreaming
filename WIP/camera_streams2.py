
from enum import Enum, auto


class Modes(Enum):
    RawToH264 = auto()
    RawToMjpeg = auto()
    H264ToH264 = auto()
    MjpegToMjpeg = auto()


class H264Encoders(Enum):
    OmxH264 = auto()
    Libx264 = auto()
    VaapiH264 = auto()


class H264Streams(Enum):
    TcpMpegTs = auto()
    TcpFlv = auto()
    # UdpRtpUnicast = auto()
    # UdpRtpMulticast = auto()

class MjpegEncoders(Enum):
    JpegEnc = auto()

class MjpegStreams(Enum):
    Tcp = auto()


################################################################################
# Settings
################################################################################

# Network settings
IP_ADDRESS="0.0.0.0"
PORT=5008

# Video device settings
VIDEO_DEVICE = "/dev/video0"
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_FPS = 30

# Options are auto, rw, mmap, userptr, dmabuf, dmabuf-import
# Generally use auto.
# If bad latency with USB camera try dmabuf
V4L2_IOMODE="auto"

# Determines both input video mode (must be supported by camera) and stream video mode
MODE = Modes.H264ToH264

# H264 settings (when stream mode is H264)
H264_ENC = H264Encoders.OmxH264
H264_STR = H264Streams.TcpMpegTs

# MJPEG settings (when stream mode is Mjpeg)
MJPEG_ENC = MjpegEncoders.JpegEnc
MJPEG_STR = MjpegStreams.Tcp
MJPEG_QUALITY=0.8


def get_input_opts() -> str:
    fmt = ""
    if MODE == Modes.RawToH264 or MODE == Modes.RawToMjpeg:
        # Raw input
        fmt="video/x-raw"
    elif MODE == Modes.H264ToH264:
        # H.264 input
        fmt="video/x-h264"
    elif MODE == Modes.MjpegToMjpeg:
        # JPEG input
        fmt="image/jpeg"
    else:
        raise Exception("Unknown input format!")
    return "{0},with={1},height={2},framerate={3}/1".format(fmt, VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS)

def get_encoder_opts() -> str:
    if MODE == Modes.H264ToH264 or MODE == Modes.MjpegToMjpeg:
        return "identity"
    elif MODE == Modes.RawToMjpeg:
        if(MJPEG_ENC == MjpegEncoders.JpegEnc):
            return "jpegenc"
        else:
            raise Exception("Unknown encoder!")
    elif MODE == Modes.RawToH264:
        if(H264_ENC == H264Encoders.OmxH264):
            return "omxh264enc"
        elif(H264_ENC == H264Encoders.Libx264):
            return "x264enc tune=zerolatency speed-preset=ultrafast"
        elif(H264_ENC == H264Encoders.VaapiH264):
            return "vaapih264enc"
        else:
            raise Exception("Unknown encoder!")
    else:
        raise Exception("Unknown mode!")

def get_net_opts() -> str:
    if MODE == Modes.RawToMjpeg or MODE == Modes.MjpegToMjpeg:
        if(MJPEG_STR == MjpegStreams.Tcp):
            return "BROKEN_FIX_ME"
        else:
            raise Exception("Unknown stream type!")
    elif MODE == Modes.RawToH264 or MODE == Modes.H264ToH264:
        if(H264_STR == H264Streams.TcpMpegTs):
            return "h264parse config-interval=-1 ! mpegtsmux ! tcpserversink host={0} port={1}".format(IP_ADDRESS, PORT)
        elif(H264_STR == H264Streams.TcpFlv):
            return "h264parse config-interval=-1 ! flvmux streamable=true ! tcpserversink host={0} port={1}".format(IP_ADDRESS, PORT)
        else:
            raise Exception("Unknown stream type!")
    else:
        raise Exception("Unknown mode!")

if __name__ == "__main__":
    cmd = "gst-launch-1.0 v4l2src device={0} io-mode={1} ! {2} ! {3} ! {4}".format(VIDEO_DEVICE, V4L2_IOMODE, 
            get_input_opts(), get_encoder_opts(), get_net_opts())
    print(cmd)
