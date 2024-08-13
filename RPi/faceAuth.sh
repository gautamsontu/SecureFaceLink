#!/bin/bash


cd /home/pi/FaceAuth


PYTHON_CMD="/usr/bin/python3 /home/pi/FaceAuth/main.py"


Process1=$(pgrep -f -x "$PYTHON_CMD")

if [ ! -z "$Process1" ]; then
    echo "Script is already running with PID: $Process1"
else
    echo "Script is not running. Starting script..."
    nohup $PYTHON_CMD > /home/pi/FaceAuth/main.log 2>&1 &
    echo "Script started with new PID: $(pgrep -f -x "$PYTHON_CMD")"
fi
