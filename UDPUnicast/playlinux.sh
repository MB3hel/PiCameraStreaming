#!/bin/bash

# The port the stream packets are being sent to
PORT=5008

gst-launch-1.0 udpsrc port=$PORT ! "application/x-rtp, payload=127" ! rtph264depay vaapih264dec ! xvimagesink sync=false
