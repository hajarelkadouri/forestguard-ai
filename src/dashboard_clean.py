"""
ForestGuard AI - Version Clean
ImageOverlay + Déforestation Réaliste (Sans IA)
TOUS LES PAYS DU MONDE + BEAUCOUP DE ZONES
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
from shapely.geometry import Point, Polygon
from PIL import Image
import io, base64, random, math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Configuration
st.set_page_config(
    page_title="ForestGuard AI", 
    layout="wide",
    page_icon="🌲",
    initial_sidebar_state="collapsed"
)

# CSS personnalisé pour une mise en forme professionnelle
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Variables CSS */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #4CAF50;
        --accent-color: #81C784;
        --danger-color: #D32F2F;
        --warning-color: #F57C00;
        --info-color: #1976D2;
        --background-light: #F8F9FA;
        --text-dark: #2C3E50;
        --border-color: #E0E0E0;
        --shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Styles généraux */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Header avec logo */
    .header-container {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow);
        color: white;
        text-align: center;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    
    .logo {
        font-size: 3rem;
        background: linear-gradient(45deg, #81C784, #A5D6A7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Conteneurs avec encadrés */
    .custom-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    
    .controls-container {
        background: var(--background-light);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid var(--primary-color);
        margin-bottom: 2rem;
    }
    
    .kpi-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }
    
    /* Sections avec titres colorés */
    .section-header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px 10px 0 0;
        margin: 0 -1.5rem 1.5rem -1.5rem;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.3rem;
    }
    
    .analytics-section {
        background: white;
        border-radius: 12px;
        box-shadow: var(--shadow);
        border: 1px solid var(--border-color);
        overflow: hidden;
        margin: 2rem 0;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid var(--border-color);
        margin-bottom: 1rem;
    }
    
    /* Badges de statut */
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.2rem;
    }
    
    .status-critique {
        background-color: #FFEBEE;
        color: var(--danger-color);
        border: 1px solid #FFCDD2;
    }
    
    .status-eleve {
        background-color: #FFF3E0;
        color: var(--warning-color);
        border: 1px solid #FFCC02;
    }
    
    .status-modere {
        background-color: #E3F2FD;
        color: var(--info-color);
        border: 1px solid #BBDEFB;
    }
    
    .status-faible {
        background-color: #E8F5E8;
        color: var(--primary-color);
        border: 1px solid #C8E6C9;
    }
    
    /* Amélioration des métriques Streamlit */
    [data-testid="metric-container"] {
        background: white;
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        .subtitle {
            font-size: 1rem;
        }
        .logo {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Données géographiques réalistes - TOUS LES PAYS DU MONDE
COUNTRIES = {
    # AMÉRIQUE DU SUD
    "Brésil": {
        "bounds": [[-33.8, -73.9], [5.3, -28.8]],
        "polygon": [
            (-73.9, -33.8), (-60.0, -33.8), (-50.0, -30.0), (-40.0, -25.0),
            (-35.0, -20.0), (-28.8, -15.0), (-28.8, -5.0), (-35.0, 0.0),
            (-40.0, 2.0), (-45.0, 5.3), (-55.0, 5.3), (-65.0, 2.0),
            (-70.0, -5.0), (-73.9, -15.0), (-73.9, -25.0)
        ],
        "deforestation_zones": [
            {"center": (0.25, 0.15), "name": "Amazonie Nord-Ouest", "intensity": 0.9, "size": 35},
            {"center": (0.35, 0.25), "name": "Amazonie Nord", "intensity": 0.9, "size": 40},
            {"center": (0.45, 0.20), "name": "Amazonie Nord-Est", "intensity": 0.8, "size": 35},
            {"center": (0.30, 0.35), "name": "Amazonie Ouest", "intensity": 0.8, "size": 40},
            {"center": (0.45, 0.35), "name": "Amazonie Centre", "intensity": 0.8, "size": 45},
            {"center": (0.60, 0.30), "name": "Amazonie Est", "intensity": 0.7, "size": 40},
            {"center": (0.35, 0.45), "name": "Amazonie Sud-Ouest", "intensity": 0.7, "size": 35},
            {"center": (0.55, 0.45), "name": "Amazonie Sud", "intensity": 0.7, "size": 35},
            {"center": (0.70, 0.40), "name": "Amazonie Sud-Est", "intensity": 0.6, "size": 30},
            {"center": (0.75, 0.65), "name": "Mata Atlântica Nord", "intensity": 0.6, "size": 25},
            {"center": (0.80, 0.75), "name": "Mata Atlântica Sud", "intensity": 0.5, "size": 25},
            {"center": (0.65, 0.55), "name": "Cerrado Nord", "intensity": 0.5, "size": 30},
            {"center": (0.70, 0.65), "name": "Cerrado Sud", "intensity": 0.4, "size": 30},
            {"center": (0.25, 0.75), "name": "Pantanal", "intensity": 0.4, "size": 25},
            {"center": (0.15, 0.85), "name": "Pampa", "intensity": 0.3, "size": 20},
            {"center": (0.20, 0.25), "name": "Roraima", "intensity": 0.8, "size": 30},
            {"center": (0.40, 0.15), "name": "Amapá", "intensity": 0.7, "size": 25},
            {"center": (0.50, 0.55), "name": "Mato Grosso", "intensity": 0.8, "size": 40}
        ]
    },
    
    "Argentine": {
        "bounds": [[-55.1, -73.6], [-21.8, -53.6]],
        "polygon": [(-73.6, -55.1), (-53.6, -55.1), (-53.6, -21.8), (-73.6, -21.8)],
        "deforestation_zones": [
            {"center": (0.25, 0.25), "name": "Chaco Húmedo", "intensity": 0.7, "size": 35},
            {"center": (0.35, 0.35), "name": "Chaco Seco", "intensity": 0.8, "size": 40},
            {"center": (0.45, 0.45), "name": "Espinal", "intensity": 0.6, "size": 30},
            {"center": (0.55, 0.25), "name": "Selva Paranaense", "intensity": 0.9, "size": 35},
            {"center": (0.65, 0.35), "name": "Yungas", "intensity": 0.7, "size": 30},
            {"center": (0.25, 0.65), "name": "Patagonie Nord", "intensity": 0.4, "size": 25},
            {"center": (0.35, 0.75), "name": "Patagonie Sud", "intensity": 0.3, "size": 20}
        ]
    },
    
    "Pérou": {
        "bounds": [[-18.3, -81.4], [0.0, -68.7]],
        "polygon": [(-81.4, -18.3), (-68.7, -18.3), (-68.7, 0.0), (-81.4, 0.0)],
        "deforestation_zones": [
            {"center": (0.20, 0.25), "name": "Amazonie Péruvienne Nord", "intensity": 0.8, "size": 35},
            {"center": (0.35, 0.35), "name": "Loreto", "intensity": 0.9, "size": 40},
            {"center": (0.50, 0.45), "name": "Ucayali", "intensity": 0.8, "size": 35},
            {"center": (0.25, 0.55), "name": "Madre de Dios", "intensity": 0.7, "size": 30},
            {"center": (0.40, 0.65), "name": "Cusco Forestier", "intensity": 0.6, "size": 25},
            {"center": (0.60, 0.35), "name": "San Martín", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.25), "name": "Amazonas", "intensity": 0.8, "size": 35},
            {"center": (0.30, 0.45), "name": "Huánuco", "intensity": 0.6, "size": 25}
        ]
    },
    
    "Colombie": {
        "bounds": [[-4.2, -79.0], [12.5, -66.9]],
        "polygon": [(-79.0, -4.2), (-66.9, -4.2), (-66.9, 12.5), (-79.0, 12.5)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Chocó", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.65), "name": "Caquetá", "intensity": 0.8, "size": 35},
            {"center": (0.55, 0.55), "name": "Meta", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.45), "name": "Guaviare", "intensity": 0.8, "size": 35},
            {"center": (0.35, 0.35), "name": "Putumayo", "intensity": 0.6, "size": 25},
            {"center": (0.75, 0.35), "name": "Vichada", "intensity": 0.7, "size": 30},
            {"center": (0.25, 0.45), "name": "Nariño", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.75), "name": "Antioquia", "intensity": 0.5, "size": 25},
            {"center": (0.45, 0.85), "name": "Córdoba", "intensity": 0.6, "size": 25}
        ]
    },
    
    "Bolivie": {
        "bounds": [[-22.9, -69.6], [-9.7, -57.5]],
        "polygon": [(-69.6, -22.9), (-57.5, -22.9), (-57.5, -9.7), (-69.6, -9.7)],
        "deforestation_zones": [
            {"center": (0.35, 0.25), "name": "Pando", "intensity": 0.7, "size": 30},
            {"center": (0.55, 0.35), "name": "Beni", "intensity": 0.8, "size": 35},
            {"center": (0.65, 0.55), "name": "Santa Cruz Nord", "intensity": 0.9, "size": 40},
            {"center": (0.70, 0.70), "name": "Santa Cruz Sud", "intensity": 0.8, "size": 35},
            {"center": (0.45, 0.65), "name": "Cochabamba", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.45), "name": "La Paz Forestier", "intensity": 0.5, "size": 25}
        ]
    },
    
    "Venezuela": {
        "bounds": [[0.6, -73.4], [12.2, -59.8]],
        "polygon": [(-73.4, 0.6), (-59.8, 0.6), (-59.8, 12.2), (-73.4, 12.2)],
        "deforestation_zones": [
            {"center": (0.25, 0.25), "name": "Amazonas", "intensity": 0.7, "size": 35},
            {"center": (0.45, 0.35), "name": "Bolívar", "intensity": 0.8, "size": 40},
            {"center": (0.65, 0.45), "name": "Delta Amacuro", "intensity": 0.6, "size": 25},
            {"center": (0.35, 0.65), "name": "Apure", "intensity": 0.7, "size": 30},
            {"center": (0.55, 0.75), "name": "Barinas", "intensity": 0.6, "size": 25}
        ]
    },
    
    "Équateur": {
        "bounds": [[-5.0, -81.1], [1.7, -75.2]],
        "polygon": [(-81.1, -5.0), (-75.2, -5.0), (-75.2, 1.7), (-81.1, 1.7)],
        "deforestation_zones": [
            {"center": (0.75, 0.35), "name": "Oriente", "intensity": 0.8, "size": 35},
            {"center": (0.65, 0.55), "name": "Pastaza", "intensity": 0.7, "size": 30},
            {"center": (0.55, 0.45), "name": "Morona Santiago", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.65), "name": "Esmeraldas", "intensity": 0.7, "size": 30}
        ]
    },
    
    # ASIE DU SUD-EST
    "Indonésie": {
        "bounds": [[-11.0, 95.0], [6.0, 141.0]],
        "polygon": [
            (95.0, 6.0), (100.0, 6.0), (100.0, -6.0), (95.0, -6.0),
            (106.0, -6.0), (115.0, -6.0), (115.0, -9.0), (106.0, -9.0),
            (108.0, 4.0), (119.0, 4.0), (119.0, -4.0), (108.0, -4.0),
            (130.0, 0.0), (141.0, 0.0), (141.0, -9.0), (130.0, -9.0)
        ],
        "deforestation_zones": [
            {"center": (0.12, 0.25), "name": "Sumatra Nord", "intensity": 0.8, "size": 35},
            {"center": (0.15, 0.45), "name": "Sumatra Centre", "intensity": 0.8, "size": 35},
            {"center": (0.15, 0.65), "name": "Sumatra Sud", "intensity": 0.7, "size": 30},
            {"center": (0.35, 0.75), "name": "Java Ouest", "intensity": 0.6, "size": 25},
            {"center": (0.45, 0.75), "name": "Java Centre", "intensity": 0.5, "size": 20},
            {"center": (0.55, 0.75), "name": "Java Est", "intensity": 0.5, "size": 20},
            {"center": (0.35, 0.25), "name": "Kalimantan Nord-Ouest", "intensity": 0.9, "size": 40},
            {"center": (0.40, 0.35), "name": "Kalimantan Ouest", "intensity": 0.9, "size": 40},
            {"center": (0.50, 0.25), "name": "Kalimantan Nord", "intensity": 0.8, "size": 35},
            {"center": (0.50, 0.35), "name": "Kalimantan Est", "intensity": 0.8, "size": 40},
            {"center": (0.45, 0.45), "name": "Kalimantan Sud", "intensity": 0.7, "size": 35},
            {"center": (0.80, 0.35), "name": "Papua Ouest", "intensity": 0.7, "size": 35},
            {"center": (0.85, 0.45), "name": "Papua Centre", "intensity": 0.6, "size": 30},
            {"center": (0.90, 0.55), "name": "Papua Est", "intensity": 0.6, "size": 30},
            {"center": (0.65, 0.55), "name": "Sulawesi Nord", "intensity": 0.6, "size": 25},
            {"center": (0.70, 0.65), "name": "Sulawesi Sud", "intensity": 0.5, "size": 25}
        ]
    },
    
    "Malaisie": {
        "bounds": [[0.8, 99.6], [7.4, 119.3]],
        "polygon": [(99.6, 0.8), (119.3, 0.8), (119.3, 7.4), (99.6, 7.4)],
        "deforestation_zones": [
            {"center": (0.25, 0.45), "name": "Peninsular Malaysia", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.25), "name": "Sabah", "intensity": 0.8, "size": 35},
            {"center": (0.55, 0.45), "name": "Sarawak", "intensity": 0.8, "size": 35},
            {"center": (0.75, 0.35), "name": "Sabah Est", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.55), "name": "Sarawak Sud", "intensity": 0.7, "size": 30},
            {"center": (0.15, 0.65), "name": "Johor", "intensity": 0.5, "size": 20}
        ]
    },
    
    "Myanmar": {
        "bounds": [[9.8, 92.2], [28.5, 101.2]],
        "polygon": [(92.2, 9.8), (101.2, 9.8), (101.2, 28.5), (92.2, 28.5)],
        "deforestation_zones": [
            {"center": (0.35, 0.75), "name": "Tanintharyi", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.55), "name": "Bago", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.35), "name": "Sagaing", "intensity": 0.5, "size": 25},
            {"center": (0.65, 0.25), "name": "Kachin", "intensity": 0.6, "size": 30},
            {"center": (0.75, 0.45), "name": "Shan", "intensity": 0.5, "size": 25},
            {"center": (0.25, 0.65), "name": "Kayin", "intensity": 0.6, "size": 25}
        ]
    },
    
    "Thaïlande": {
        "bounds": [[5.6, 97.3], [20.5, 105.6]],
        "polygon": [(97.3, 5.6), (105.6, 5.6), (105.6, 20.5), (97.3, 20.5)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Sud Thaïlande", "intensity": 0.6, "size": 25},
            {"center": (0.45, 0.55), "name": "Centre", "intensity": 0.5, "size": 20},
            {"center": (0.65, 0.35), "name": "Nord-Est", "intensity": 0.4, "size": 20},
            {"center": (0.35, 0.25), "name": "Nord", "intensity": 0.5, "size": 25}
        ]
    },
    
    "Laos": {
        "bounds": [[13.9, 100.1], [22.5, 107.6]],
        "polygon": [(100.1, 13.9), (107.6, 13.9), (107.6, 22.5), (100.1, 22.5)],
        "deforestation_zones": [
            {"center": (0.35, 0.25), "name": "Nord Laos", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.45), "name": "Centre", "intensity": 0.5, "size": 20},
            {"center": (0.45, 0.75), "name": "Sud", "intensity": 0.4, "size": 20}
        ]
    },
    
    "Cambodge": {
        "bounds": [[10.4, 102.3], [14.7, 107.6]],
        "polygon": [(102.3, 10.4), (107.6, 10.4), (107.6, 14.7), (102.3, 14.7)],
        "deforestation_zones": [
            {"center": (0.25, 0.65), "name": "Cardamomes", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.35), "name": "Mondulkiri", "intensity": 0.6, "size": 25},
            {"center": (0.45, 0.55), "name": "Centre", "intensity": 0.5, "size": 20}
        ]
    },
    
    "Vietnam": {
        "bounds": [[8.2, 102.1], [23.4, 109.5]],
        "polygon": [(102.1, 8.2), (109.5, 8.2), (109.5, 23.4), (102.1, 23.4)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Delta Mékong", "intensity": 0.5, "size": 20},
            {"center": (0.45, 0.55), "name": "Hauts Plateaux", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.35), "name": "Nord Vietnam", "intensity": 0.4, "size": 20},
            {"center": (0.75, 0.45), "name": "Côte Centre", "intensity": 0.3, "size": 15}
        ]
    },
    
    "Philippines": {
        "bounds": [[4.6, 116.9], [21.1, 126.6]],
        "polygon": [(116.9, 4.6), (126.6, 4.6), (126.6, 21.1), (116.9, 21.1)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Mindanao", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.55), "name": "Visayas", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.35), "name": "Luzon", "intensity": 0.5, "size": 25},
            {"center": (0.75, 0.25), "name": "Palawan", "intensity": 0.8, "size": 35}
        ]
    },
    
    # AFRIQUE CENTRALE
    "Congo (RDC)": {
        "bounds": [[-13.5, 12.2], [5.4, 31.3]],
        "polygon": [
            (12.2, 5.4), (18.0, 5.4), (25.0, 4.0), (31.3, 2.0),
            (31.3, -8.0), (28.0, -13.5), (20.0, -13.5), (15.0, -10.0),
            (12.2, -6.0), (12.2, 0.0)
        ],
        "deforestation_zones": [
            {"center": (0.35, 0.15), "name": "Équateur Nord", "intensity": 0.8, "size": 35},
            {"center": (0.45, 0.25), "name": "Forêt Équatoriale Nord", "intensity": 0.7, "size": 35},
            {"center": (0.55, 0.35), "name": "Orientale Ouest", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.25), "name": "Orientale Est", "intensity": 0.6, "size": 30},
            {"center": (0.40, 0.45), "name": "Bassin Congo Ouest", "intensity": 0.8, "size": 40},
            {"center": (0.55, 0.45), "name": "Bassin Congo Centre", "intensity": 0.8, "size": 40},
            {"center": (0.70, 0.45), "name": "Bassin Congo Est", "intensity": 0.7, "size": 35},
            {"center": (0.35, 0.65), "name": "Kasaï Occidental", "intensity": 0.6, "size": 25},
            {"center": (0.50, 0.65), "name": "Kasaï Oriental", "intensity": 0.5, "size": 25},
            {"center": (0.65, 0.65), "name": "Forêt Équatoriale Sud", "intensity": 0.6, "size": 30},
            {"center": (0.80, 0.35), "name": "Kivu Nord", "intensity": 0.6, "size": 25},
            {"center": (0.85, 0.55), "name": "Kivu Sud", "intensity": 0.5, "size": 25},
            {"center": (0.25, 0.55), "name": "Bandundu", "intensity": 0.5, "size": 25},
            {"center": (0.75, 0.15), "name": "Haut-Uélé", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.35), "name": "Mai-Ndombe", "intensity": 0.7, "size": 30}
        ]
    },
    
    "Cameroun": {
        "bounds": [[1.7, 8.5], [13.1, 16.2]],
        "polygon": [(8.5, 1.7), (16.2, 1.7), (16.2, 13.1), (8.5, 13.1)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Sud-Ouest", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.65), "name": "Sud", "intensity": 0.8, "size": 35},
            {"center": (0.65, 0.55), "name": "Est", "intensity": 0.8, "size": 35},
            {"center": (0.55, 0.45), "name": "Centre", "intensity": 0.6, "size": 25},
            {"center": (0.35, 0.35), "name": "Littoral", "intensity": 0.5, "size": 25},
            {"center": (0.75, 0.35), "name": "Adamaoua", "intensity": 0.4, "size": 20},
            {"center": (0.15, 0.85), "name": "Nord-Ouest", "intensity": 0.5, "size": 20}
        ]
    },
    
    "Gabon": {
        "bounds": [[-4.0, 8.7], [2.3, 14.5]],
        "polygon": [(8.7, -4.0), (14.5, -4.0), (14.5, 2.3), (8.7, 2.3)],
        "deforestation_zones": [
            {"center": (0.35, 0.35), "name": "Estuaire", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.45), "name": "Ogooué-Ivindo", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.65), "name": "Haut-Ogooué", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.65), "name": "Nyanga", "intensity": 0.5, "size": 20},
            {"center": (0.45, 0.25), "name": "Woleu-Ntem", "intensity": 0.6, "size": 25}
        ]
    },
    
    "République Centrafricaine": {
        "bounds": [[2.2, 14.4], [11.0, 27.4]],
        "polygon": [(14.4, 2.2), (27.4, 2.2), (27.4, 11.0), (14.4, 11.0)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Sangha-Mbaéré", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.65), "name": "Lobaye", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.55), "name": "Mbomou", "intensity": 0.5, "size": 20},
            {"center": (0.35, 0.45), "name": "Mambéré-Kadéï", "intensity": 0.6, "size": 25}
        ]
    },
    
    "Tchad": {
        "bounds": [[7.4, 13.5], [23.4, 24.0]],
        "polygon": [(13.5, 7.4), (24.0, 7.4), (24.0, 23.4), (13.5, 23.4)],
        "deforestation_zones": [
            {"center": (0.25, 0.85), "name": "Logone Oriental", "intensity": 0.5, "size": 20},
            {"center": (0.45, 0.75), "name": "Moyen-Chari", "intensity": 0.4, "size": 20},
            {"center": (0.35, 0.65), "name": "Mandoul", "intensity": 0.4, "size": 15}
        ]
    },
    
    "Congo (Brazzaville)": {
        "bounds": [[-5.0, 11.1], [3.7, 18.6]],
        "polygon": [(11.1, -5.0), (18.6, -5.0), (18.6, 3.7), (11.1, 3.7)],
        "deforestation_zones": [
            {"center": (0.35, 0.35), "name": "Sangha", "intensity": 0.7, "size": 30},
            {"center": (0.55, 0.55), "name": "Likouala", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.65), "name": "Kouilou", "intensity": 0.5, "size": 20},
            {"center": (0.65, 0.25), "name": "Cuvette", "intensity": 0.6, "size": 25}
        ]
    },
    
    # AMÉRIQUE DU NORD
    "Canada": {
        "bounds": [[41.7, -141.0], [83.1, -52.6]],
        "polygon": [(-141.0, 60.0), (-120.0, 70.0), (-100.0, 75.0), (-80.0, 80.0), (-60.0, 75.0), (-52.6, 70.0), (-52.6, 45.0), (-65.0, 41.7), (-80.0, 41.7), (-95.0, 45.0), (-110.0, 48.0), (-125.0, 50.0), (-141.0, 55.0)],
        "deforestation_zones": [
            {"center": (0.10, 0.25), "name": "Forêt Boréale Yukon", "intensity": 0.4, "size": 30},
            {"center": (0.15, 0.35), "name": "Forêt Boréale Ouest", "intensity": 0.5, "size": 35},
            {"center": (0.25, 0.45), "name": "Colombie-Britannique Nord", "intensity": 0.6, "size": 30},
            {"center": (0.20, 0.65), "name": "Colombie-Britannique Sud", "intensity": 0.7, "size": 30},
            {"center": (0.35, 0.35), "name": "Alberta Nord", "intensity": 0.6, "size": 30},
            {"center": (0.40, 0.55), "name": "Alberta Sud", "intensity": 0.7, "size": 35},
            {"center": (0.50, 0.35), "name": "Saskatchewan Nord", "intensity": 0.5, "size": 25},
            {"center": (0.55, 0.45), "name": "Forêt Boréale Centre", "intensity": 0.5, "size": 35},
            {"center": (0.65, 0.55), "name": "Manitoba Nord", "intensity": 0.5, "size": 30},
            {"center": (0.75, 0.65), "name": "Ontario Nord", "intensity": 0.6, "size": 30},
            {"center": (0.85, 0.55), "name": "Québec Nord", "intensity": 0.5, "size": 30},
            {"center": (0.90, 0.65), "name": "Forêt Boréale Est", "intensity": 0.4, "size": 25}
        ]
    },
    
    "États-Unis": {
        "bounds": [[18.9, -180.0], [71.4, -66.9]],
        "polygon": [(-180.0, 18.9), (-66.9, 18.9), (-66.9, 71.4), (-180.0, 71.4)],
        "deforestation_zones": [
            {"center": (0.15, 0.25), "name": "Alaska Intérieur", "intensity": 0.4, "size": 35},
            {"center": (0.10, 0.35), "name": "Alaska Sud-Est", "intensity": 0.5, "size": 30},
            {"center": (0.25, 0.65), "name": "Pacifique Nord-Ouest", "intensity": 0.7, "size": 35},
            {"center": (0.30, 0.75), "name": "Californie Nord", "intensity": 0.6, "size": 30},
            {"center": (0.35, 0.55), "name": "Rocheuses Nord", "intensity": 0.5, "size": 25},
            {"center": (0.45, 0.65), "name": "Rocheuses Sud", "intensity": 0.5, "size": 25},
            {"center": (0.65, 0.45), "name": "Grands Lacs", "intensity": 0.6, "size": 30},
            {"center": (0.75, 0.65), "name": "Appalaches Nord", "intensity": 0.6, "size": 25},
            {"center": (0.80, 0.75), "name": "Appalaches Sud", "intensity": 0.7, "size": 30},
            {"center": (0.70, 0.85), "name": "Sud-Est", "intensity": 0.7, "size": 35}
        ]
    },
    
    "Mexique": {
        "bounds": [[14.5, -118.4], [32.7, -86.7]],
        "polygon": [(-118.4, 14.5), (-86.7, 14.5), (-86.7, 32.7), (-118.4, 32.7)],
        "deforestation_zones": [
            {"center": (0.85, 0.75), "name": "Chiapas", "intensity": 0.8, "size": 35},
            {"center": (0.75, 0.65), "name": "Oaxaca", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.55), "name": "Veracruz", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.45), "name": "Michoacán", "intensity": 0.5, "size": 25},
            {"center": (0.45, 0.35), "name": "Jalisco", "intensity": 0.4, "size": 20}
        ]
    },
    
    # EUROPE
    "Russie": {
        "bounds": [[41.2, 19.6], [81.9, 180.0]],
        "polygon": [(19.6, 55.0), (40.0, 65.0), (60.0, 70.0), (100.0, 75.0), (140.0, 70.0), (180.0, 65.0), (180.0, 50.0), (160.0, 45.0), (120.0, 41.2), (80.0, 45.0), (40.0, 50.0), (19.6, 52.0)],
        "deforestation_zones": [
            {"center": (0.15, 0.45), "name": "Taïga Occidentale", "intensity": 0.5, "size": 40},
            {"center": (0.25, 0.35), "name": "Oural Nord", "intensity": 0.6, "size": 35},
            {"center": (0.35, 0.55), "name": "Sibérie Occidentale", "intensity": 0.5, "size": 40},
            {"center": (0.45, 0.35), "name": "Taïga Centrale", "intensity": 0.5, "size": 45},
            {"center": (0.55, 0.45), "name": "Sibérie Centrale", "intensity": 0.4, "size": 40},
            {"center": (0.65, 0.35), "name": "Yakoutie", "intensity": 0.4, "size": 40},
            {"center": (0.75, 0.45), "name": "Taïga Orientale", "intensity": 0.4, "size": 40},
            {"center": (0.85, 0.55), "name": "Extrême-Orient", "intensity": 0.5, "size": 35},
            {"center": (0.25, 0.65), "name": "Sibérie Sud", "intensity": 0.6, "size": 35}
        ]
    },
    
    "Finlande": {
        "bounds": [[59.8, 19.1], [70.1, 31.6]],
        "polygon": [(19.1, 59.8), (31.6, 59.8), (31.6, 70.1), (19.1, 70.1)],
        "deforestation_zones": [
            {"center": (0.35, 0.25), "name": "Laponie Ouest", "intensity": 0.3, "size": 25},
            {"center": (0.65, 0.15), "name": "Laponie Est", "intensity": 0.3, "size": 20},
            {"center": (0.45, 0.55), "name": "Ostrobotnie", "intensity": 0.4, "size": 25},
            {"center": (0.65, 0.65), "name": "Carélie du Nord", "intensity": 0.4, "size": 25},
            {"center": (0.35, 0.85), "name": "Finlande Sud", "intensity": 0.5, "size": 30}
        ]
    },
    
    "Suède": {
        "bounds": [[55.3, 10.9], [69.1, 24.2]],
        "polygon": [(10.9, 55.3), (24.2, 55.3), (24.2, 69.1), (10.9, 69.1)],
        "deforestation_zones": [
            {"center": (0.45, 0.15), "name": "Norrland Nord", "intensity": 0.3, "size": 30},
            {"center": (0.55, 0.35), "name": "Norrland Sud", "intensity": 0.4, "size": 30},
            {"center": (0.45, 0.55), "name": "Svealand", "intensity": 0.5, "size": 25},
            {"center": (0.35, 0.75), "name": "Götaland", "intensity": 0.5, "size": 25}
        ]
    },
    
    "Norvège": {
        "bounds": [[57.9, 4.6], [71.2, 31.3]],
        "polygon": [(4.6, 57.9), (31.3, 57.9), (31.3, 71.2), (4.6, 71.2)],
        "deforestation_zones": [
            {"center": (0.45, 0.25), "name": "Finnmark", "intensity": 0.2, "size": 20},
            {"center": (0.55, 0.45), "name": "Trøndelag", "intensity": 0.3, "size": 25},
            {"center": (0.35, 0.65), "name": "Vestlandet", "intensity": 0.4, "size": 25},
            {"center": (0.65, 0.75), "name": "Østlandet", "intensity": 0.4, "size": 25}
        ]
    },
    
    # AFRIQUE
    "Côte d'Ivoire": {
        "bounds": [[4.4, -8.6], [10.7, -2.5]],
        "polygon": [(-8.6, 4.4), (-2.5, 4.4), (-2.5, 10.7), (-8.6, 10.7)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Ouest Montagneux", "intensity": 0.8, "size": 30},
            {"center": (0.45, 0.65), "name": "Centre-Ouest", "intensity": 0.7, "size": 25},
            {"center": (0.65, 0.55), "name": "Centre", "intensity": 0.6, "size": 25},
            {"center": (0.75, 0.75), "name": "Sud-Est", "intensity": 0.7, "size": 25}
        ]
    },
    
    "Ghana": {
        "bounds": [[4.7, -3.3], [11.2, 1.2]],
        "polygon": [(-3.3, 4.7), (1.2, 4.7), (1.2, 11.2), (-3.3, 11.2)],
        "deforestation_zones": [
            {"center": (0.35, 0.75), "name": "Ashanti", "intensity": 0.7, "size": 25},
            {"center": (0.55, 0.65), "name": "Brong-Ahafo", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.55), "name": "Western", "intensity": 0.8, "size": 30},
            {"center": (0.75, 0.45), "name": "Eastern", "intensity": 0.6, "size": 20}
        ]
    },
    
    "Nigeria": {
        "bounds": [[4.3, 2.7], [13.9, 14.7]],
        "polygon": [(2.7, 4.3), (14.7, 4.3), (14.7, 13.9), (2.7, 13.9)],
        "deforestation_zones": [
            {"center": (0.25, 0.75), "name": "Cross River", "intensity": 0.8, "size": 30},
            {"center": (0.45, 0.65), "name": "Ogun", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.55), "name": "Plateau", "intensity": 0.5, "size": 20},
            {"center": (0.35, 0.45), "name": "Taraba", "intensity": 0.6, "size": 25}
        ]
    },
    
    # OCÉANIE
    "Australie": {
        "bounds": [[-44.0, 112.9], [-9.2, 154.0]],
        "polygon": [(112.9, -44.0), (154.0, -44.0), (154.0, -9.2), (112.9, -9.2)],
        "deforestation_zones": [
            {"center": (0.85, 0.25), "name": "Queensland Nord", "intensity": 0.6, "size": 30},
            {"center": (0.90, 0.45), "name": "Queensland Sud", "intensity": 0.7, "size": 30},
            {"center": (0.85, 0.65), "name": "Nouvelle-Galles du Sud", "intensity": 0.6, "size": 25},
            {"center": (0.75, 0.85), "name": "Victoria", "intensity": 0.5, "size": 20},
            {"center": (0.25, 0.75), "name": "Australie-Occidentale Sud", "intensity": 0.4, "size": 25}
        ]
    },
    
    "Papouasie-Nouvelle-Guinée": {
        "bounds": [[-11.7, 140.8], [-0.9, 159.0]],
        "polygon": [(140.8, -11.7), (159.0, -11.7), (159.0, -0.9), (140.8, -0.9)],
        "deforestation_zones": [
            {"center": (0.35, 0.45), "name": "Highlands Ouest", "intensity": 0.7, "size": 30},
            {"center": (0.55, 0.35), "name": "Sepik", "intensity": 0.8, "size": 35},
            {"center": (0.75, 0.55), "name": "Morobe", "intensity": 0.6, "size": 25},
            {"center": (0.25, 0.65), "name": "Fly", "intensity": 0.7, "size": 30}
        ]
    },
    
    # ASIE
    "Chine": {
        "bounds": [[18.2, 73.6], [53.6, 135.0]],
        "polygon": [(73.6, 18.2), (135.0, 18.2), (135.0, 53.6), (73.6, 53.6)],
        "deforestation_zones": [
            {"center": (0.75, 0.25), "name": "Heilongjiang", "intensity": 0.5, "size": 30},
            {"center": (0.70, 0.35), "name": "Jilin", "intensity": 0.6, "size": 25},
            {"center": (0.45, 0.45), "name": "Mongolie Intérieure", "intensity": 0.4, "size": 30},
            {"center": (0.35, 0.65), "name": "Sichuan", "intensity": 0.6, "size": 25},
            {"center": (0.65, 0.75), "name": "Fujian", "intensity": 0.5, "size": 20}
        ]
    },
    
    "Inde": {
        "bounds": [[6.8, 68.1], [37.1, 97.4]],
        "polygon": [(68.1, 6.8), (97.4, 6.8), (97.4, 37.1), (68.1, 37.1)],
        "deforestation_zones": [
            {"center": (0.85, 0.25), "name": "Arunachal Pradesh", "intensity": 0.6, "size": 25},
            {"center": (0.75, 0.35), "name": "Assam", "intensity": 0.7, "size": 30},
            {"center": (0.65, 0.45), "name": "Jharkhand", "intensity": 0.6, "size": 25},
            {"center": (0.45, 0.65), "name": "Maharashtra", "intensity": 0.5, "size": 25},
            {"center": (0.25, 0.75), "name": "Karnataka", "intensity": 0.5, "size": 25}
        ]
    },
    
    "Madagascar": {
        "bounds": [[-25.6, 43.2], [-11.9, 50.5]],
        "polygon": [(43.2, -25.6), (50.5, -25.6), (50.5, -11.9), (43.2, -11.9)],
        "deforestation_zones": [
            {"center": (0.65, 0.25), "name": "Toamasina", "intensity": 0.7, "size": 30},
            {"center": (0.45, 0.45), "name": "Antananarivo", "intensity": 0.6, "size": 25},
            {"center": (0.35, 0.65), "name": "Fianarantsoa", "intensity": 0.6, "size": 25},
            {"center": (0.55, 0.75), "name": "Toliara", "intensity": 0.5, "size": 20}
        ]
    }
}

def generate_deforestation_overlay(country, type_deforestation, w=800, h=400):
    """Génère un overlay de déforestation RAPIDE avec ImageOverlay"""
    
    if country not in COUNTRIES:
        return None, None
    
    info = COUNTRIES[country]
    bounds = info["bounds"]
    zones = info["deforestation_zones"]
    
    # Créer matrice RGBA
    data = np.zeros((h, w, 4), dtype=np.uint8)
    
    # Couleur selon le type
    if "Légale" in type_deforestation:
        base_color = np.array([0, 200, 0], dtype=np.uint8)  # Vert pour légale
        opacity_factor = 0.7
    else:
        base_color = np.array([255, 50, 0], dtype=np.uint8)  # Rouge pour illégale
        opacity_factor = 0.9
    
    # Générer les zones RAPIDEMENT (sans vérification pixel par pixel)
    for zone in zones:
        center_x = int(zone["center"][0] * w)
        center_y = int(zone["center"][1] * h)
        intensity = zone["intensity"]
        size = min(zone["size"], 40)  # Limiter la taille pour la vitesse
        
        # Variation naturelle réduite
        center_x += random.randint(-10, 10)
        center_y += random.randint(-10, 10)
        
        # S'assurer que c'est dans les limites
        center_x = max(size, min(w-size, center_x))
        center_y = max(size, min(h-size, center_y))
        
        # Créer forme circulaire simple (RAPIDE)
        radius = size + random.randint(-size//4, size//4)
        
        # Créer masque circulaire avec numpy (TRÈS RAPIDE)
        y_indices, x_indices = np.ogrid[:h, :w]
        mask = (x_indices - center_x)**2 + (y_indices - center_y)**2 <= radius**2
        
        # Calculer gradient de distance (vectorisé)
        distances = np.sqrt((x_indices - center_x)**2 + (y_indices - center_y)**2)
        fade = np.maximum(0, 1 - distances / radius)
        fade = np.where(mask, fade, 0)
        
        # Couleur avec variation légère
        color_variation = np.random.randint(-20, 21, 3)
        color = np.clip(base_color + color_variation, 0, 255)
        
        # Alpha basé sur intensité et fade
        alpha = (intensity * opacity_factor * fade * 200).astype(np.uint8)
        
        # Appliquer couleur où le masque est actif
        active_pixels = mask & (alpha > 0)
        data[active_pixels, :3] = color
        data[active_pixels, 3] = alpha[active_pixels]
    
    return data, bounds

def calculate_country_kpis(country_data):
    """Calcule les KPIs pour un pays donné"""
    zones = country_data["deforestation_zones"]
    
    total_zones = len(zones)
    avg_intensity = np.mean([zone["intensity"] for zone in zones])
    high_risk_zones = len([zone for zone in zones if zone["intensity"] > 0.7])
    total_area = sum([zone["size"] for zone in zones])
    
    # Calcul du risque global
    risk_level = "Faible"
    if avg_intensity > 0.7:
        risk_level = "Critique"
    elif avg_intensity > 0.5:
        risk_level = "Élevé"
    elif avg_intensity > 0.3:
        risk_level = "Modéré"
    
    return {
        "total_zones": total_zones,
        "avg_intensity": avg_intensity,
        "high_risk_zones": high_risk_zones,
        "total_area": total_area,
        "risk_level": risk_level
    }

def create_intensity_chart(zones):
    """Crée un graphique en barres des intensités par zone"""
    df = pd.DataFrame([
        {"Zone": zone["name"], "Intensité": zone["intensity"], "Taille": zone["size"]}
        for zone in zones
    ])
    
    # Couleurs basées sur l'intensité
    colors = ['#2E8B57' if x < 0.4 else '#FFD700' if x < 0.7 else '#DC143C' for x in df["Intensité"]]
    
    fig = go.Figure(data=[
        go.Bar(
            x=df["Zone"],
            y=df["Intensité"],
            marker_color=colors,
            text=[f"{x:.2f}" for x in df["Intensité"]],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Intensité: %{y:.2f}<br>Taille: %{customdata} km²<extra></extra>',
            customdata=df["Taille"]
        )
    ])
    
    fig.update_layout(
        title="Distribution de l'Intensité de Déforestation par Zone",
        xaxis_title="Zones",
        yaxis_title="Intensité (0-1)",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        xaxis=dict(tickangle=45)
    )
    
    return fig

def create_intensity_pie_chart(zones):
    """Crée un graphique en secteurs des catégories d'intensité"""
    low = len([z for z in zones if z["intensity"] < 0.4])
    medium = len([z for z in zones if 0.4 <= z["intensity"] < 0.7])
    high = len([z for z in zones if z["intensity"] >= 0.7])
    
    labels = ['Faible (0-0.4)', 'Modéré (0.4-0.7)', 'Élevé (0.7-1.0)']
    values = [low, medium, high]
    colors = ['#2E8B57', '#FFD700', '#DC143C']
    
    # Filtrer les valeurs nulles
    filtered_data = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]
    if filtered_data:
        labels, values, colors = zip(*filtered_data)
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{value} zones<br>(%{percent})',
        hovertemplate='<b>%{label}</b><br>Zones: %{value}<br>Pourcentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title="Répartition des Zones par Niveau d'Intensité",
        height=400,
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig

def create_scatter_plot(zones):
    """Crée un graphique de dispersion taille vs intensité"""
    df = pd.DataFrame([
        {"Zone": zone["name"], "Intensité": zone["intensity"], "Taille": zone["size"]}
        for zone in zones
    ])
    
    colors = ['#2E8B57' if x < 0.4 else '#FFD700' if x < 0.7 else '#DC143C' for x in df["Intensité"]]
    
    fig = go.Figure(data=go.Scatter(
        x=df["Taille"],
        y=df["Intensité"],
        mode='markers+text',
        marker=dict(
            size=12,
            color=colors,
            line=dict(width=2, color='white')
        ),
        text=df["Zone"],
        textposition="top center",
        textfont=dict(size=10),
        hovertemplate='<b>%{text}</b><br>Taille: %{x} km²<br>Intensité: %{y:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="Relation Taille des Zones vs Intensité de Déforestation",
        xaxis_title="Taille de la Zone (km²)",
        yaxis_title="Intensité (0-1)",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )
    
    return fig
# Interface utilisateur avec design professionnel
# Header avec logo
st.markdown("""
<div class="header-container">
    <div class="logo-container">
        <div class="logo">🌲</div>
        <div>
            <h1 class="main-title">ForestGuard AI</h1>
            <p class="subtitle">Système de Surveillance de la Déforestation Mondiale</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Contrôles dans un conteneur encadré
st.markdown('<div class="controls-container">', unsafe_allow_html=True)
st.markdown("### Paramètres de Visualisation")

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox("Sélectionner un Pays", list(COUNTRIES.keys()))

with col2:
    type_deforestation = st.radio(
        "Type de Déforestation",
        ["Déforestation Légale", "Déforestation Illégale"]
    )

with col3:
    resolution = st.selectbox("Résolution de la Carte", 
                             ["Standard (800x400)", "Haute (1200x600)"])

st.markdown('</div>', unsafe_allow_html=True)

# Résolution
if "Haute" in resolution:
    w, h = 1200, 600
else:
    w, h = 800, 400

# Générer l'overlay (RAPIDE) avec cache
@st.cache_data
def cached_generate_overlay(country, type_deforestation, w, h):
    return generate_deforestation_overlay(country, type_deforestation, w, h)

with st.spinner("Génération rapide..."):
    overlay_data, bounds = cached_generate_overlay(country, type_deforestation, w, h)

if overlay_data is not None:
    # Conteneur pour la carte
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    st.markdown("### Carte Interactive de Déforestation")
    
    # Convertir en image
    img = Image.fromarray(overlay_data)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    
    # Créer carte avec position stable
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2
    
    # Utiliser une clé stable basée sur le pays pour éviter le rechargement
    if f"map_center_{country}" not in st.session_state:
        st.session_state[f"map_center_{country}"] = [center_lat, center_lon]
    
    m = folium.Map(
        location=st.session_state[f"map_center_{country}"], 
        zoom_start=6,
        prefer_canvas=True  # Améliore les performances
    )
    
    # Fond satellite
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite", overlay=False, control=True
    ).add_to(m)
    
    # ImageOverlay
    folium.raster_layers.ImageOverlay(
        image=f"data:image/png;base64,{b64}",
        bounds=bounds, opacity=0.75,
        name=f"Déforestation {type_deforestation.split(' ')[1]}"
    ).add_to(m)
    
    folium.LayerControl().add_to(m)
    
    # Clé stable pour éviter le flash de la carte
    map_key = f"map_{country}_{hash(str(bounds))}"
    st_folium(m, width=1400, height=600, key=map_key)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Section Statistiques avec encadrés
    st.markdown('<div class="custom-container">', unsafe_allow_html=True)
    st.markdown("### Statistiques Générales")
    
    col1, col2 = st.columns(2)
    zones_info = COUNTRIES[country]["deforestation_zones"]
    
    with col1:
        st.metric("Pays Analysé", country)
        st.metric("Zones Détectées", len(zones_info))
        st.metric("Type d'Analyse", type_deforestation.split(" ")[1])
        
    with col2:
        st.markdown("**Zones de Déforestation Identifiées:**")
        for zone in zones_info[:5]:  # Limiter à 5 zones pour l'affichage
            intensity_level = "Critique" if zone["intensity"] > 0.7 else "Élevée" if zone["intensity"] > 0.5 else "Modérée" if zone["intensity"] > 0.3 else "Faible"
            badge_class = f"status-{intensity_level.lower()}"
            st.markdown(f"""
            <div style="margin: 0.3rem 0;">
                <strong>{zone['name']}</strong> 
                <span class="status-badge {badge_class}">{intensity_level}</span>
            </div>
            """, unsafe_allow_html=True)
        
        if len(zones_info) > 5:
            st.markdown(f"*... et {len(zones_info) - 5} autres zones*")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Section Analytics avec design professionnel
    st.markdown("""
    <div class="analytics-section">
        <div class="section-header">
            Analyse Détaillée des Données
        </div>
    """, unsafe_allow_html=True)
    
    # Calculer les KPIs
    kpis = calculate_country_kpis(COUNTRIES[country])
    
    # KPIs avec encadrés colorés
    st.markdown("#### Indicateurs Clés de Performance")
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        st.metric(
            label="Zones Totales",
            value=kpis["total_zones"],
            help="Nombre total de zones de déforestation identifiées"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_col2:
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        st.metric(
            label="Intensité Moyenne",
            value=f"{kpis['avg_intensity']:.2f}",
            delta=f"{kpis['avg_intensity']-0.5:.2f}" if kpis['avg_intensity'] > 0.5 else None,
            delta_color="inverse",
            help="Intensité moyenne de déforestation (0-1)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_col3:
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        st.metric(
            label="Zones Critiques",
            value=kpis["high_risk_zones"],
            delta=f"{(kpis['high_risk_zones']/kpis['total_zones']*100):.0f}%" if kpis['total_zones'] > 0 else "0%",
            delta_color="inverse",
            help="Zones avec intensité > 0.7"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_col4:
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        st.metric(
            label="Surface Totale",
            value=f"{kpis['total_area']} km²",
            help="Surface totale des zones affectées"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with kpi_col5:
        # Couleur du badge selon le niveau de risque
        risk_colors = {
            "Faible": "#4CAF50",
            "Modéré": "#2196F3", 
            "Élevé": "#FF9800",
            "Critique": "#F44336"
        }
        risk_color = risk_colors.get(kpis['risk_level'], "#9E9E9E")
        
        st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
        st.metric(
            label="Niveau de Risque",
            value=kpis['risk_level'],
            help="Évaluation globale du risque de déforestation"
        )
        st.markdown(f"""
        <div style="text-align: center; margin-top: 0.5rem;">
            <span style="background-color: {risk_color}; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem; font-weight: 500;">
                {kpis['risk_level'].upper()}
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Graphiques avec encadrés
    st.markdown("#### Visualisations Interactives")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Graphique en barres des intensités
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        intensity_fig = create_intensity_chart(zones_info)
        st.plotly_chart(intensity_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Graphique de dispersion
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        scatter_fig = create_scatter_plot(zones_info)
        st.plotly_chart(scatter_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with chart_col2:
        # Graphique en secteurs
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        pie_fig = create_intensity_pie_chart(zones_info)
        st.plotly_chart(pie_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tableau détaillé avec encadré
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown("#### Détails des Zones")
        zones_df = pd.DataFrame([
            {
                "Zone": zone["name"],
                "Intensité": f"{zone['intensity']:.2f}",
                "Taille (km²)": zone["size"],
                "Niveau": "Critique" if zone["intensity"] > 0.7 else "Élevé" if zone["intensity"] > 0.5 else "Modéré" if zone["intensity"] > 0.3 else "Faible"
            }
            for zone in zones_info
        ])
        
        # Colorier le tableau selon l'intensité
        def color_intensity(val):
            if "Critique" in str(val):
                return 'background-color: #ffebee; color: #d32f2f; font-weight: 500;'
            elif "Élevé" in str(val):
                return 'background-color: #fff3e0; color: #f57c00; font-weight: 500;'
            elif "Modéré" in str(val):
                return 'background-color: #e3f2fd; color: #1976d2; font-weight: 500;'
            elif "Faible" in str(val):
                return 'background-color: #e8f5e8; color: #2e7d32; font-weight: 500;'
            return ''
        
        styled_df = zones_df.style.applymap(color_intensity, subset=['Niveau'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fermer le conteneur analytics
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer professionnel
    st.markdown("""
    <div style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #2E7D32 0%, #4CAF50 100%); border-radius: 12px; text-align: center; color: white;">
        <h4 style="margin: 0; font-family: 'Inter', sans-serif;">ForestGuard AI</h4>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
            Surveillance intelligente de la déforestation mondiale • Données en temps réel • Analyse prédictive
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    pass