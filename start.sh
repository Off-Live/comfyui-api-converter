#!/bin/bash

# get aws ready
#echo 'getting aws ready...'
#aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID} \
#  && aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY} \
#  && aws configure set default.region ${AWS_REGION}

echo "*** RUN IN API SERVICE MODE ***"

echo "Starting ComfyUI"
python /root/ComfyUI/main.py --listen --cpu --port=3000 &

echo "Starting API converter"
python /root/comfyui-api-converter/app.py
