#!/bin/bash

echo "*** RUN IN API SERVICE MODE ***"

echo "Starting ComfyUI"
python /root/ComfyUI/main.py --listen --cpu --port=3000 &

echo "Starting API converter"
python /root/comfyui-api-converter/app.py
