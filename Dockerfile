# Utiliser une image Python de base
FROM python:3.11-slim

# Définir les arguments (tokens passés au build)
ARG NGROK_AUTH_TOKEN
ARG HUGGINGFACEHUB_API_TOKEN
ARG MISTRAL_TOKEN

# Définir les variables d'environnement pour Hugging Face et Mistral
ENV HUGGINGFACEHUB_API_TOKEN=${HUGGINGFACEHUB_API_TOKEN}
ENV MISTRAL_TOKEN=${MISTRAL_TOKEN}

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir flask requests && \
    apt-get clean

# Installer ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

# Ajouter le token ngrok à la configuration
RUN mkdir -p /root/.ngrok2 && \
    echo "authtoken: ${NGROK_AUTH_TOKEN}" > /root/.ngrok2/ngrok.yml

# Copier le code source dans le conteneur
WORKDIR /app
COPY . /app

# Lancer un script pour gérer ngrok, récupérer l'URL et lancer main.py
CMD ["bash", "/app/entrypoint.sh"]
