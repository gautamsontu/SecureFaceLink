#!/bin/bash

# Navigate to the script's directory
cd /home/pi/FaceAuth

# Define the command to run the Python script
PYTHON_CMD="/usr/bin/python3 /home/pi/FaceAuth/main.py"

# Check if the script is already running
Process1=$(pgrep -f -x "$PYTHON_CMD")

if [ ! -z "$Process1" ]; then
    echo "Script is already running with PID: $Process1"
else
    echo "Script is not running. Starting script..."
    nohup $PYTHON_CMD > /home/pi/FaceAuth/main.log 2>&1 &
    echo "Script started with new PID: $(pgrep -f -x "$PYTHON_CMD")"
fi
