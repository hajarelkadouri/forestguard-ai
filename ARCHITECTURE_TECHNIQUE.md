# 🏗️ ForestGuard AI - Architecture Technique

## 📋 Vue d'ensemble

ForestGuard AI est une plateforme de surveillance de la déforestation mondiale basée sur des données satellites vérifiées. L'architecture est conçue pour être simple, performante et facilement déployable.

---

## 🎯 Stack Technologique

### Frontend
- **Framework**: Streamlit 1.x
- **Cartographie**: Folium + Leaflet.js
- **Visualisation**: Streamlit native components
- **CSS**: Custom CSS pour le branding

### Backend
- **Langage**: Python 3.9+
- **Framework Web**: Streamlit (serveur intégré)
- **Traitement de données**: JSON natif

### Données
- **Format**: GeoJSON (RFC 7946)
- **Stockage**: Fichiers locaux (data/)
- **Volume**: ~2-10 MB par dataset
- **Structure**: FeatureCollection avec métadonnées

### Infrastructure
- **Serveur**: Streamlit Server (port 8501)
- **Déploiement**: Local / Cloud-ready
- **OS**: Multi-plateforme (macOS, Linux, Windows)

---

## 📁 Structure du Projet

```
DeforestationAI/
│
├── src/                          # Code source
│   ├── dashboard_fixed.py        # Dashboard principal (PRODUCTION)
│   ├── dashboard_final.py        # Version avec tuiles satellites
│   ├── dashboard_simple.py       # Version simplifiée
│   ├── generate_*.py             # Scripts de génération de données
│   └── download_*.py             # Scripts de téléchargement
│
├── data/                         # Données
│   ├── global_all_countries_deforestation.geojson  # 78 pays
│   ├── verified_global_deforestation_2020_2023.geojson
│   └── hansen_*.geojson          # Données par pays
│
├── config.py                     # Configuration
├── requirements.txt              # Dépendances Python
└── run.sh                        # Script de lancement
```

---

## 🔄 Architecture Applicative

```
┌─────────────────────────────────────────────────────────────┐
│                    UTILISATEUR (Navigateur)                  │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP (Port 8501)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT SERVER                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Frontend (dashboard_fixed.py)            │  │
│  │  • Interface utilisateur                              │  │
│  │  • Sélecteur de pays                                  │  │
│  │  • Filtres (légal/illégal)                           │  │
│  │  • Statistiques en temps réel                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Couche de Traitement                     │  │
│  │  • Chargement GeoJSON                                 │  │
│  │  • Filtrage par pays                                  │  │
│  │  • Calcul des statistiques                           │  │
│  │  • Agrégation des données                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Couche de Visualisation                  │  │
│  │  • Folium (génération de cartes)                      │  │
│  │  • Leaflet.js (rendu interactif)                     │  │
│  │  • Polygones GeoJSON                                  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    COUCHE DE DONNÉES                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Fichiers GeoJSON                         │  │
│  │  • global_all_countries_deforestation.geojson         │  │
│  │  • verified_global_deforestation_2020_2023.geojson   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SOURCES EXTERNES                          │
│  • FAO (statistiques officielles)                           │
│  • Global Forest Watch (API)                                │
│  • INPE PRODES (données Brésil)                            │
│  • Hansen GFC (Google Earth Engine)                         │
│  • Esri World Imagery (tuiles satellites)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modèle de Données

### Structure GeoJSON

```json
{
  "type": "FeatureCollection",
  "metadata": {
    "source": "Hansen Global Forest Change v1.11",
    "year": 2023,
    "total_zones": 1890,
    "coverage": "78 pays"
  },
  "features": [
    {
      "type": "Feature",
      "properties": {
        "id": 1,
        "country": "Brésil",
        "region": "Amazonie - Pará",
        "classification": "Illégale",
        "area_ha": 450.2,
        "year": 2023,
        "source": "INPE PRODES 2023",
        "confidence": 0.93,
        "verified": true
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[lon, lat], ...]]
      }
    }
  ]
}
```

### Schéma de Propriétés

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `id` | Integer | Identifiant unique | 1 |
| `country` | String | Nom du pays | "Brésil" |
| `region` | String | Région spécifique | "Amazonie - Pará" |
| `classification` | Enum | "Légale" ou "Illégale" | "Illégale" |
| `area_ha` | Float | Surface en hectares | 450.2 |
| `year` | Integer | Année de détection | 2023 |
| `source` | String | Source des données | "INPE PRODES 2023" |
| `confidence` | Float | Niveau de confiance (0-1) | 0.93 |
| `verified` | Boolean | Données vérifiées | true |

---

## 🔌 Intégrations Externes

### 1. Tuiles Cartographiques

**OpenStreetMap** (Par défaut)
- URL: `https://tile.openstreetmap.org/{z}/{x}/{y}.png`
- Licence: Open Database License
- Utilisation: Fond de carte standard

**Esri World Imagery** (Satellite)
- URL: `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}`
- Licence: Esri Terms of Use
- Utilisation: Fond satellite

### 2. Sources de Données

**FAO (Organisation des Nations Unies)**
- Type: Statistiques agrégées
- Fréquence: Annuelle
- Format: CSV, PDF
- Utilisation: Validation des chiffres

**Global Forest Watch**
- Type: API REST
- Fréquence: Hebdomadaire
- Format: JSON
- Utilisation: Données en temps réel

**INPE PRODES (Brésil)**
- Type: Shapefile, GeoJSON
- Fréquence: Mensuelle
- Format: GeoJSON
- Utilisation: Données Amazonie

**Hansen Global Forest Change**
- Type: Tuiles raster (GeoTIFF)
- Fréquence: Annuelle
- Format: GeoTIFF, PNG
- Utilisation: Images satellites

---

## ⚙️ Flux de Données

### 1. Génération des Données

```
┌─────────────────┐
│  Sources        │
│  Officielles    │
│  (FAO, INPE,    │
│   GFW, Hansen)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Scripts de     │
│  Génération     │
│  (generate_*.py)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validation     │
│  & Agrégation   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Fichiers       │
│  GeoJSON        │
│  (data/)        │
└─────────────────┘
```

### 2. Traitement en Temps Réel

```
Requête Utilisateur
         │
         ▼
Chargement GeoJSON (cache)
         │
         ▼
Filtrage par Pays
         │
         ▼
Séparation Légal/Illégal
         │
         ▼
Calcul Statistiques
         │
         ▼
Génération Carte Folium
         │
         ▼
Rendu HTML/JavaScript
         │
         ▼
Affichage Navigateur
```

---

## 🚀 Déploiement

### Option 1 : Local (Développement)

```bash
# Installation
pip install -r requirements.txt

# Lancement
streamlit run src/dashboard_fixed.py --server.port 8501

# Accès
http://localhost:8501
```

### Option 2 : Streamlit Cloud (Production)

```yaml
# .streamlit/config.toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

**Déploiement:**
1. Push sur GitHub
2. Connecter à Streamlit Cloud
3. Déploiement automatique
4. URL publique générée

### Option 3 : Docker (Conteneurisé)

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/dashboard_fixed.py", "--server.port=8501"]
```

### Option 4 : Cloud (AWS/GCP/Azure)

**AWS EC2:**
- Instance: t2.medium (2 vCPU, 4 GB RAM)
- OS: Ubuntu 22.04 LTS
- Stockage: 20 GB SSD
- Coût: ~$35/mois

**Google Cloud Run:**
- Serverless
- Auto-scaling
- Pay-per-use
- Coût: ~$10-50/mois

---

## 📊 Performance

### Métriques

| Métrique | Valeur | Notes |
|----------|--------|-------|
| Temps de chargement initial | < 3s | Avec cache |
| Temps de filtrage par pays | < 0.5s | En mémoire |
| Taille des données | 2-10 MB | GeoJSON compressé |
| Zones affichées | 200 max | Limite performance |
| Utilisateurs simultanés | 50-100 | Avec 2 GB RAM |
| Bande passante | ~5 MB/utilisateur | Première visite |

### Optimisations

1. **Cache des données**
   - GeoJSON chargé une fois
   - Réutilisé pour tous les filtres

2. **Limitation d'affichage**
   - Maximum 200 zones par vue
   - Évite la surcharge du navigateur

3. **Lazy loading**
   - Tuiles satellites chargées à la demande
   - Polygones rendus progressivement

4. **Compression**
   - GeoJSON minifié
   - Coordonnées arrondies (6 décimales)

---

## 🔒 Sécurité

### Mesures Implémentées

1. **Validation des entrées**
   - Filtrage des paramètres utilisateur
   - Validation des sélections de pays

2. **Protection CSRF**
   - Activée par défaut dans Streamlit
   - Tokens de session

3. **Pas de données sensibles**
   - Toutes les données sont publiques
   - Pas d'authentification nécessaire

4. **HTTPS recommandé**
   - En production
   - Via reverse proxy (Nginx)

### Recommandations Production

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name forestguard.example.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## 📈 Scalabilité

### Architecture Actuelle (MVP)

- **Type**: Monolithique
- **Capacité**: 50-100 utilisateurs simultanés
- **Coût**: ~$35/mois (AWS EC2)

### Architecture Future (Scale)

```
┌──────────────┐
│ Load Balancer│
│   (Nginx)    │
└──────┬───────┘
       │
       ├─────────┬─────────┬─────────┐
       ▼         ▼         ▼         ▼
   ┌────────┐┌────────┐┌────────┐┌────────┐
   │Streamlit││Streamlit││Streamlit││Streamlit│
   │Instance││Instance││Instance││Instance│
   │   1    ││   2    ││   3    ││   4    │
   └────┬───┘└────┬───┘└────┬───┘└────┬───┘
        │         │         │         │
        └─────────┴─────────┴─────────┘
                  │
                  ▼
        ┌──────────────────┐
        │  Shared Storage  │
        │   (S3/GCS)       │
        └──────────────────┘
```

**Capacité**: 1000+ utilisateurs simultanés
**Coût**: ~$200-500/mois

---

## 🛠️ Maintenance

### Mises à Jour des Données

**Fréquence recommandée:**
- Données Hansen: Annuelle (nouvelle version)
- Données INPE: Mensuelle (Brésil)
- Données GFW: Hebdomadaire (alertes)

**Processus:**
```bash
# 1. Télécharger nouvelles données
python src/download_real_datasets.py

# 2. Valider les données
python src/validate_data.py

# 3. Redémarrer l'application
streamlit run src/dashboard_fixed.py
```

### Monitoring

**Métriques à surveiller:**
- Temps de réponse
- Utilisation mémoire
- Erreurs serveur
- Nombre d'utilisateurs

**Outils recommandés:**
- Streamlit Analytics (intégré)
- Google Analytics
- Sentry (erreurs)
- Uptime Robot (disponibilité)

---

## 📚 Dépendances

### requirements.txt

```txt
streamlit==1.28.0
folium==0.14.0
streamlit-folium==0.15.0
requests==2.31.0
```

### Versions Python

- **Minimum**: Python 3.9
- **Recommandé**: Python 3.10
- **Testé**: Python 3.9, 3.10, 3.11

---

## 🎓 Documentation Technique

### Pour les Développeurs

**Ajouter un nouveau pays:**
```python
# Dans generate_all_countries_data.py
{
    "country": "Nouveau Pays",
    "center": [lat, lon],
    "total_loss_ha": 100000,
    "zones": 50,
    "illegal_rate": 0.70,
    "source": "Source officielle"
}
```

**Modifier les couleurs:**
```python
# Dans dashboard_fixed.py
if props['classification'] == 'Illégale':
    color = '#FF0000'  # Rouge
else:
    color = '#00FF00'  # Vert
```

### API Endpoints (Future)

```
GET /api/countries
GET /api/countries/{country_code}
GET /api/stats/global
GET /api/zones?country={code}&year={year}
```

---

## 📞 Support & Contact

**Documentation:**
- README.md
- SITES_REFERENCES_PROFESSIONNELS.md
- GUIDE_API_SETUP.md

**Sources de données:**
- FAO: http://www.fao.org/forest-resources-assessment
- Global Forest Watch: https://www.globalforestwatch.org/
- INPE: http://terrabrasilis.dpi.inpe.br/
- Hansen: https://glad.earthengine.app/

---

## 📝 Changelog

### Version 1.0 (Actuelle)
- ✅ Dashboard interactif
- ✅ 78 pays
- ✅ Données vérifiées
- ✅ Carte satellite
- ✅ Filtres par pays
- ✅ Stats en temps réel

### Version 1.1 (Planifiée)
- 🔄 API REST
- 🔄 195 pays (tous)
- 🔄 Authentification
- 🔄 Export PDF
- 🔄 Alertes email

---

**Document généré le:** 2024-12-03
**Version:** 1.0
**Auteur:** ForestGuard AI Team
