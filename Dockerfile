# Utiliser une image Python de base
FROM python:3.11-slim

# Définir les arguments
ARG NGROK_AUTH_TOKEN
ARG HUGGINGFACEHUB_API_TOKEN
ARG MISTRAL_TOKEN

# Variables d'environnement
ENV HUGGINGFACEHUB_API_TOKEN=${HUGGINGFACEHUB_API_TOKEN}
ENV MISTRAL_TOKEN=${MISTRAL_TOKEN}

# Installation des dépendances système
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

# Configuration de ngrok
RUN ngrok config add-authtoken ${NGROK_AUTH_TOKEN}

# Installation des dépendances Python avec version spécifique de Pydantic
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    pydantic==1.10.15 \  
    -r requirements.txt

# Solution temporaire pour OpenCV
RUN pip uninstall -y opencv-python && pip install opencv-python-headless==4.10.0.84

# Copie du code
COPY . .

# Script d'entrée modifié
RUN echo '#!/bin/bash\n\
    ngrok http 5000 & \n\
    sleep 5  # Délai supplémentaire pour le démarrage de ngrok\n\
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