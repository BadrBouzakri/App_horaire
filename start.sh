#!/bin/bash

# Script de démarrage pour l'application de gestion des horaires

echo "🕐 Démarrage de l'application de gestion des horaires..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker first."
    exit 1
fi

# Vérifier si docker-compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose."
    exit 1
fi

# Créer le dossier templates s'il n'existe pas
if [ ! -d "templates" ]; then
    echo "📁 Création du dossier templates..."
    mkdir templates
fi

# Vérifier que tous les fichiers nécessaires sont présents
files=("app.py" "templates/index.html" "requirements.txt" "Dockerfile" "docker-compose.yml")
missing_files=false

for file in "${files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        missing_files=true
    fi
done

if [ "$missing_files" = true ]; then
    echo "⚠️  Veuillez vous assurer que tous les fichiers sont présents avant de continuer."
    exit 1
fi

# Construire et démarrer les conteneurs
echo "🔨 Construction de l'image Docker..."
docker-compose build

echo "🚀 Démarrage des conteneurs..."
docker-compose up -d

# Attendre que l'application soit prête
echo "⏳ Attente du démarrage de l'application..."
sleep 3

# Vérifier si l'application est en cours d'exécution
if docker-compose ps | grep -q "Up"; then
    echo "✅ Application démarrée avec succès!"
    echo "📍 Accédez à l'application: http://localhost:5000"
    echo ""
    echo "Commandes utiles:"
    echo "  - Voir les logs: docker-compose logs -f"
    echo "  - Arrêter l'application: docker-compose down"
    echo "  - Redémarrer: docker-compose restart"
else
    echo "❌ Erreur lors du démarrage de l'application."
    echo "Consultez les logs avec: docker-compose logs"
    exit 1
fi