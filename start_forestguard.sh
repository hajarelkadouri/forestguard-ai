#!/bin/bash

echo "🌲 Lancement de ForestGuard AI..."
echo "=================================="

# Aller dans le bon dossier
cd "$(dirname "$0")"

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import streamlit, folium" 2>/dev/null || {
    echo "📥 Installation des dépendances..."
    pip3 install -r requirements.txt
}

echo "🚀 Démarrage du serveur..."
echo "📱 L'application s'ouvrira dans votre navigateur"
echo "🔗 URL: http://localhost:8504"
echo ""
echo "💡 Pour arrêter l'application, appuyez sur Ctrl+C"
echo "=================================="

# Lancer l'application
python3 run_app.py