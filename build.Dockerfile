FROM offdev/comfy-base-torch2.1.2-cuda11.8

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
# Expose port to the outside
EXPOSE 3003

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install awscli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && ./aws/install

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
