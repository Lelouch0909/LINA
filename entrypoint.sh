#!/bin/bash

# Lancer ngrok sur le port 5000 en arrière-plan
ngrok http 5000 > /dev/null &

# Attendre quelques secondes pour que ngrok génère l'URL
sleep 5

# Récupérer l'URL publique générée par ngrok
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

# Ajouter l'URL ngrok aux variables d'environnement
export NGROK_URL

# Afficher les variables d'environnement (pour le debug)
echo "NGROK_URL=$NGROK_URL"
echo "HUGGINGFACEHUB_API_TOKEN=$HUGGINGFACEHUB_API_TOKEN"
echo "MISTRAL_TOKEN=$MISTRAL_TOKEN"

# Lancer le contrôleur ImageController et main.py
python3 services/cacheServices/ImageController.py &
python3 main.py
