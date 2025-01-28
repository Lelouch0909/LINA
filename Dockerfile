# Utiliser une image Python de base
FROM python:3.11-slim

# Définir les arguments (tokens passés au build)
ARG NGROK_AUTH_TOKEN
ARG HUGGINGFACEHUB_API_TOKEN
ARG MISTRAL_TOKEN

# Définir les variables d'environnement pour Hugging Face et Mistral
ENV HUGGINGFACEHUB_API_TOKEN=${HUGGINGFACEHUB_API_TOKEN}
ENV MISTRAL_TOKEN=${MISTRAL_TOKEN}

# Copier le code source dans le conteneur
WORKDIR /app
COPY . /app

# Installer les dépendances système (curl, jq, ngrok, python3-pip, portaudio-dev, etc.)
RUN apt-get update && \
    apt-get install -y \
    curl \
    jq \
    libportaudio2 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    portaudio19-dev \  
    libgl1-mesa-glx \  
    python3-pip && \
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && \
    apt-get install -y ngrok && \
    ngrok config add-authtoken $NGROK_AUTH_TOKEN && \
    apt-get clean

# Installer les dépendances Python
RUN pip install --no-cache-dir -r /app/requirements.txt

# Script d'entrée pour lancer ngrok et ton application
RUN echo '#!/bin/bash\n\
    ngrok http 5000 & \n\
    sleep 5 \n\
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r .tunnels[0].public_url) \n\
    export NGROK_URL=$NGROK_URL \n\
    echo "NGROK_URL=$NGROK_URL" \n\
    python3 /app/main.py' > /app/entrypoint.sh

# Rendre le script exécutable
RUN chmod +x /app/entrypoint.sh

# Lancer le script d'entrée
ENTRYPOINT ["/app/entrypoint.sh"]

# Exposer le port 5000 pour ngrok
EXPOSE 5000
