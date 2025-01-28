#!/bin/bash

# Lancer ngrok sur le port 5000
echo "Starting ngrok..."
ngrok http 5000 &

# Attendre que ngrok soit prêt
sleep 5

# Vérifier si jq est installé
if ! command -v jq &> /dev/null
then
    echo "jq could not be found. Please ensure it is installed."
    exit 1
fi

# Récupérer l'URL générée par ngrok
NGROK_URL=$(curl --silent http://127.0.0.1:4040/api/tunnels | jq -r .tunnels[0].public_url)
if [[ -z "$NGROK_URL" ]]; then
  echo "Failed to retrieve NGROK_URL."
  exit 1
fi

echo "Ngrok URL: $NGROK_URL"

# Ajouter l'URL aux variables d'environnement
export NGROK_URL

# Lancer l'application Python
echo "Launching Python application..."
python3 /app/main.py
