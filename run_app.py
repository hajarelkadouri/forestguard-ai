#!/usr/bin/env python3
"""
ForestGuard AI - Script de lancement
Auteur: ForestGuard AI Team
Version: 1.0
"""

import subprocess
import sys
import os

def check_requirements():
    """Vérifie que les dépendances sont installées"""
    try:
        import streamlit
        import folium
        print("✅ Toutes les dépendances sont installées")
        return True
    except ImportError as e:
        print(f"❌ Dépendance manquante: {e}")
        print("💡 Exécutez: pip install -r requirements.txt")
        return False

def check_data():
    """Vérifie que les fichiers de données existent"""
    data_files = [
        "data/global_all_countries_deforestation.geojson",
        "data/verified_global_deforestation_2020_2023.geojson"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ Données trouvées: {file_path}")
            return True
    
    print("❌ Aucun fichier de données trouvé")
    print("💡 Assurez-vous que les fichiers GeoJSON sont dans le dossier data/")
    return False

def main():
    """Fonction principale"""
    print("ForestGuard AI - Dashboard Simple")
    print("=" * 50)
    
    # Vérifications
    if not check_requirements():
        sys.exit(1)
    
    # Lancement direct du dashboard clean
    dashboard_file = "src/dashboard_clean.py"
    
    print("\n🚀 Lancement du Dashboard...")
    print("📱 L'application s'ouvrira dans votre navigateur")
    print("🔗 URL: http://localhost:8504")
    print("Interface simple + ImageOverlay + Déforestation réaliste")
    print("Version épurée et efficace")
    print("\n💡 Pour arrêter l'application, appuyez sur Ctrl+C")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            dashboard_file,
            "--server.port", "8504",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()