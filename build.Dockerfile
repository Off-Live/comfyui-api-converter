FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
# Expose port to the outside
EXPOSE 3003

# Update base packages and install dependencies
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends curl unzip vim wget gnupg git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

RUN --mount=type=cache,target=/cache --mount=type=cache,target=/root/.cache/pip \
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# install awscli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && ./aws/install

# install ComfyUI
RUN cd /root \
    && git clone -b dev https://github.com/Off-Live/ComfyUI.git \
    && cd ComfyUI && pip install -r requirements.txt

# install custom nodes
RUN cd /root/ComfyUI/custom_nodes \
    && git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git \
    && git clone https://github.com/WASasquatch/was-node-suite-comfyui \
    && git clone https://github.com/cubiq/ComfyUI_IPAdapter_plus \
    && git clone https://github.com/Off-Live/ComfyUI-off-suite \
    && git clone https://github.com/Fannovel16/comfyui_controlnet_aux.git \
    && git clone https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git \
    && git clone https://github.com/mav-rik/facerestore_cf/

# update custom nodes
# COPY impact-pack.ini /root/ComfyUI/custom_nodes/ComfyUI-Impact-Pack/
RUN cd /root/ComfyUI/custom_nodes/ComfyUI-Impact-Pack && git submodule update --init --recursive && python install.py
RUN cd /root/ComfyUI/custom_nodes/was-node-suite-comfyui && pip install -r requirements.txt
RUN cd /root/ComfyUI/custom_nodes/comfyui_controlnet_aux && echo "\nonnxruntime-gpu" >> requirements.txt && pip install -r requirements.txt
RUN cd /root/ComfyUI/custom_nodes/facerestore_cf && pip install -r requirements.txt

# quick test ComfyUI --> ONLY for serverless
#RUN cd /root/ComfyUI && python main.py --quick-test-for-ci --cpu

# converter
COPY . /root/comfyui-api-converter

RUN cd /root/comfyui-api-converter \
    && pip install --ignore-installed blinker==1.7.0 \
    && pip install -r requirements.txt

# Cleanup section (Worker Template)
RUN apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Set permissions and specify the command to run
RUN chmod +x /root/comfyui-api-converter/start.sh
CMD /root/comfyui-api-converter/start.sh
