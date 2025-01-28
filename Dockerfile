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
    && curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com bullseye main" | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update \
    && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

# Configuration de ngrok
RUN ngrok config add-authtoken ${NGROK_AUTH_TOKEN}

# Installation des dépendances Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY . .

# Script d'entrée
RUN echo '#!/bin/bash\n\
    ngrok http 5000 & \n\
    while ! curl -s http://localhost:4040/api/tunnels > /dev/null; do sleep 1; done\n\
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r .tunnels[0].public_url)\n\
    export NGROK_URL\n\
    echo "NGROK URL: $NGROK_URL"\n\
    python3 /app/main.py' > entrypoint.sh \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 5000