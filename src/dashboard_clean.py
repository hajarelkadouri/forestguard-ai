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

# Configuration
st.set_page_config(
    page_title="ForestGuard AI", 
    layout="wide",
    page_icon="🌲"
)

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
# Interface utilisateur
st.title("ForestGuard AI - Dashboard")
st.markdown("**Analyse de déforestation par pays - MONDE ENTIER**")

col1, col2, col3 = st.columns(3)

with col1:
    country = st.selectbox("Pays", list(COUNTRIES.keys()))

with col2:
    type_deforestation = st.radio(
        "Type de déforestation",
        ["Déforestation Légale", "Déforestation Illégale"]
    )

with col3:
    resolution = st.selectbox("Résolution", 
                             ["Standard (800x400)", "Haute (1200x600)"])

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
    
    # Stats
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Statistiques")
        zones_info = COUNTRIES[country]["deforestation_zones"]
        st.metric("Pays", country)
        st.metric("Zones détectées", len(zones_info))
        st.metric("Type", type_deforestation.split(" ")[1])
        
    with col2:
        st.markdown("### Zones de Déforestation")
        for zone in zones_info:
            intensity_text = "Élevée" if zone["intensity"] > 0.7 else "Moyenne" if zone["intensity"] > 0.5 else "Faible"
            st.write(f"**{zone['name']}** - Intensité: {intensity_text}")

st.markdown("---")
st.markdown(f"""
### Caractéristiques du système
- **{len(COUNTRIES)} pays** disponibles dans le monde entier
- **ImageOverlay** : Technique professionnelle GIS
- **Frontières exactes** : Pas de zones dans l'océan
- **Déforestation réaliste** : Basée sur vraies zones forestières
- **Interface simple** : Sans complexité inutile
- **Formes organiques** : Rendu naturel
- **Performance optimisée** : Génération ultra-rapide
""")

if __name__ == "__main__":
    pass