FROM python:3.11-slim

ARG NGROK_AUTH_TOKEN
ARG HUGGINGFACEHUB_API_TOKEN
ARG MISTRAL_TOKEN

ENV HUGGINGFACEHUB_API_TOKEN=${HUGGINGFACEHUB_API_TOKEN}
ENV MISTRAL_TOKEN=${MISTRAL_TOKEN}

RUN apt-get update && apt-get install -y \
    curl \
    jq \
    gcc \
    g++ \
    make \
    portaudio19-dev \
    libasound2-dev \
    libjack-dev \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com bullseye main" | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update \
    && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

RUN ngrok config add-authtoken ${NGROK_AUTH_TOKEN}

WORKDIR /app
COPY requirements.txt .

# Solution pour contourner le conflit Pydantic/LangChain
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    "pydantic<2" \
    "langchain==0.0.348" \ 
    -r requirements.txt && \
    sed -i '/pydantic/d' requirements.txt && \
    pip install --no-cache-dir opencv-python-headless==4.10.0.84

COPY . .

# Patch automatique pour MistralAPIWrapper
RUN sed -i 's/apikey = None/apikey: str = None/' services/orchestrationServices/MistralAPIWrapper.py

RUN echo '#!/bin/bash\n\
    ngrok http 5000 &\n\
    sleep 5\n\
    while ! curl -s http://localhost:4040/api/tunnels | grep -q "public_url"; do\n\
        sleep 1\n\
    done\n\
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r .tunnels[0].public_url)\n\
    export NGROK_URL\n\
    echo "NGROK URL: $NGROK_URL"\n\
    python3 /app/main.py' > entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 5000