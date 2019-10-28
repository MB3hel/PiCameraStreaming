#!/bin/bash

set HOST=192.168.1.113
set PORT=5008

ffplay -fflags nobuffer -probesize 32 -flags low_delay -framedrop tcp://%HOST%:%PORT%/
