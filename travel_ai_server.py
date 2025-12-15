from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import joblib
from sklearn.preprocessing import StandardScaler
# TensorFlow deshabilitado para evitar problemas de DLL
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LSTM, Conv1D, MaxPooling1D, Flatten
import uvicorn
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from io import BytesIO
import json
import os

app = FastAPI(title="Travel AI Optimizer")

class TravelDataRequest(BaseModel):
    flight_data: Dict
    hotel_data: Dict
    user_preferences: Dict

class TravelOptimizationResponse(BaseModel):
    best_flight: Dict
    best_hotel: Dict
    alternatives: List[Dict]
    market_average: float
    recommendations: List[str]
    confidence_score: float
    estimated_activities_cost: float
    estimated_food_cost: float
    recommended_activities: List[str]

class ReportRequest(BaseModel):
    travel_data: Dict
    report_type: str  # 'offers', 'itinerary', 'analysis', 'full'
    format: str  # 'pdf', 'excel'

# Modelo híbrido para optimización de viajes
class TravelAIOptimizer:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.initialize_model()
    
    def initialize_model(self):
        """Inicializar modelo híbrido para optimización de precios de viajes"""
        try:
            # Modelo TensorFlow deshabilitado para evitar problemas de DLL
            # Se usa lógica simplificada en su lugar
            self.model = None
            print("Modelo TensorFlow deshabilitado - usando lógica simplificada")
        except Exception as e:
            print(f"Error inicializando modelo: {e}")
    
    def extract_flight_features(self, flight_data: Dict) -> List[float]:
        """Extraer características de datos de vuelos"""
        flights = flight_data.get('content', {}).get('results', {}).get('itineraries', {})
        
        if not flights:
            return [0] * 10
        
        # Analizar todos los vuelos disponibles
        prices = []
        durations = []
        airlines = set()
        stops = []
        
        for itinerary_id, itinerary in flights.items():
            price = itinerary.get('pricing_options', [{}])[0].get('price', {}).get('amount', 0)
            if price > 0:
                prices.append(price)
            
            # Duración del vuelo
            legs = itinerary.get('legs', [])
            if legs:
                duration = legs[0].get('durationInMinutes', 0)
                durations.append(duration)
            
            # Aerolíneas y escalas
            for leg in legs:
                segments = leg.get('segments', [])
                stops.append(len(segments) - 1)
                for segment in segments:
                    airline = segment.get('marketingCarrier', {}).get('name', '')
                    if airline:
                        airlines.add(airline)
        
        # Características calculadas
        features = [
            np.mean(prices) if prices else 0,
            np.min(prices) if prices else 0,
            np.std(prices) if prices else 0,
            np.mean(durations) if durations else 0,
            np.mean(stops) if stops else 0,
            len(airlines),
            len(prices),
            max(prices) if prices else 0,
            min(prices) if prices else 0,
            np.median(prices) if prices else 0
        ]
        
        return features
    
    def extract_hotel_features(self, hotel_data: Dict) -> List[float]:
        """Extraer características de datos de hoteles"""
        hotels = hotel_data.get('result', [])
        
        if not hotels:
            return [0] * 10
        
        prices = []
        ratings = []
        reviews = []
        distances = []
        
        for hotel in hotels:
            price = hotel.get('composite_price_breakdown', {}).get('all_inclusive_amount', {}).get('value', 0)
            if price > 0:
                prices.append(price)
            
            rating = hotel.get('review_score', 0)
            if rating > 0:
                ratings.append(rating)
            
            review_count = hotel.get('review_nr', 0)
            reviews.append(review_count)
            
            # Distancia al centro (aproximada)
            distance = hotel.get('distances', [{}])[0].get('text', '0 km').replace(' km', '').replace(',', '')
            try:
                distances.append(float(distance))
            except:
                distances.append(0)
        
        # Características calculadas
        features = [
            np.mean(prices) if prices else 0,
            np.min(prices) if prices else 0,
            np.std(prices) if prices else 0,
            np.mean(ratings) if ratings else 0,
            np.mean(reviews) if reviews else 0,
            np.mean(distances) if distances else 0,
            len(prices),
            max(prices) if prices else 0,
            min(prices) if prices else 0,
            np.median(prices) if prices else 0
        ]
        
        return features
    
    def find_best_flight(self, flight_data: Dict) -> Dict:
        """Encontrar el mejor vuelo basado en precio y características"""
        itineraries = flight_data.get('content', {}).get('results', {}).get('itineraries', {})
        
        best_flight = None
        best_score = float('inf')
        
        for itinerary_id, itinerary in itineraries.items():
            pricing_options = itinerary.get('pricing_options', [])
            if not pricing_options:
                continue
            
            price_info = pricing_options[0].get('price', {})
            price = price_info.get('amount', 0)
            
            # Calcular score considerando precio y duración
            legs = itinerary.get('legs', [])
            duration = legs[0].get('durationInMinutes', 0) if legs else 0
            
            # Penalizar vuelos muy largos
            duration_penalty = duration / 60  # Horas como penalización
            
            score = price + duration_penalty * 10  # $10 por hora extra
            
            if score < best_score and price > 0:
                best_score = score
                best_flight = {
                    'itinerary_id': itinerary_id,
                    'price': price,
                    'currency': price_info.get('currency', 'USD'),
                    'airline': legs[0].get('segments', [{}])[0].get('marketingCarrier', {}).get('name', 'Unknown'),
                    'duration': f"{duration // 60}h {duration % 60}m",
                    'stops': len(legs[0].get('segments', [])) - 1,
                    'departure_time': legs[0].get('departure', ''),
                    'arrival_time': legs[0].get('arrival', '')
                }
        
        return best_flight or {}
    
    def find_best_hotel(self, hotel_data: Dict) -> Dict:
        """Encontrar el mejor hotel basado en precio y rating"""
        hotels = hotel_data.get('result', [])
        
        best_hotel = None
        best_score = float('inf')
        
        for hotel in hotels:
            price = hotel.get('composite_price_breakdown', {}).get('all_inclusive_amount', {}).get('value', 0)
            rating = hotel.get('review_score', 0)
            review_count = hotel.get('review_nr', 0)
            
            if price <= 0:
                continue
            
            # Calcular score considerando precio, rating y reviews
            price_score = price
            rating_bonus = (10 - rating) * 10  # Penalizar ratings bajos
            review_bonus = max(0, 5 - (review_count / 100))  # Bonificar hoteles con muchas reviews
            
            score = price_score + rating_bonus + review_bonus
            
            if score < best_score:
                best_score = score
                best_hotel = {
                    'hotel_id': hotel.get('hotel_id'),
                    'hotel_name': hotel.get('hotel_name', 'Unknown Hotel'),
                    'price': price,
                    'currency': hotel.get('currency_code', 'USD'),
                    'rating': rating,
                    'review_count': review_count,
                    'address': hotel.get('address', ''),
                    'distance': hotel.get('distances', [{}])[0].get('text', 'Unknown'),
                    'amenities': hotel.get('hotel_facilities', [])[:5]  # Top 5 amenities
                }
        
        return best_hotel or {}
    
    def generate_recommendations(self, user_preferences: Dict, best_flight: Dict, best_hotel: Dict) -> List[str]:
        """Generar recomendaciones personalizadas"""
        recommendations = []
        
        destination = user_preferences.get('destination', '')
        duration = user_preferences.get('trip_duration', 0)
        travelers = user_preferences.get('travelers', 1)
        season = user_preferences.get('season', 'medium')
        
        # Recomendaciones basadas en destino
        destination_recommendations = {
            'NYC': ['Visitar Central Park', 'Subir al Empire State', 'Ver un musical en Broadway'],
            'PAR': ['Subir a la Torre Eiffel', 'Visitar el Louvre', 'Pasear por Montmartre'],
            'LON': ['Ver el Cambio de Guardia', 'Visitar el British Museum', 'Pasear por el Thames'],
            'ROM': ['Visitar el Coliseo', 'Tirar una moneda en Fontana di Trevi', 'Ver el Vaticano'],
            'TYO': ['Visitar Sensō-ji', 'Cruzar el Shibuya Crossing', 'Probar sushi en Tsukiji']
        }
        
        if destination in destination_recommendations:
            recommendations.extend(destination_recommendations[destination][:2])
        
        # Recomendaciones generales
        recommendations.extend([
            f"Reservar con anticipación para mejores precios",
            f"Llevar efectivo local para gastos pequeños",
            f"Descargar mapa offline de {destination}"
        ])
        
        # Recomendaciones basadas en temporada
        if season == 'high':
            recommendations.append("Reservar actividades con anticipación - temporada alta")
        elif season == 'low':
            recommendations.append("Aprovechar precios más bajos en actividades")
        
        return recommendations

# Función para generar itinerarios detallados
def generate_detailed_itinerary(destination: str, duration: int, travelers: int) -> Dict:
    """Generar itinerario detallado basado en el destino y duración"""
    
    # Itinerarios por destino
    itineraries = {
        'NYC': {
            'theme': 'Exploración Urbana',
            'days': [
                {
                    'day': 1,
                    'theme': 'Llegada y Orientación',
                    'description': 'Llegada al aeropuerto, traslado al hotel y exploración del barrio',
                    'activities': [
                        {'time': '14:00', 'name': 'Llegada al Aeropuerto JFK', 'duration': '2h', 'cost': 0},
                        {'time': '16:00', 'name': 'Traslado al Hotel', 'duration': '1h', 'cost': 50},
                        {'time': '18:00', 'name': 'Check-in y Descanso', 'duration': '1h', 'cost': 0},
                        {'time': '19:30', 'name': 'Cena en Restaurante Local', 'duration': '2h', 'cost': 60},
                    ],
                    'meals': {
                        'breakfast': 'En el hotel',
                        'lunch': 'Comida rápida en el camino',
                        'dinner': 'Restaurante italiano en Times Square'
                    },
                    'recommendations': [
                        'Descansar después del viaje',
                        'Cambiar dinero en el hotel',
                        'Comprar tarjeta de transporte MetroCard'
                    ],
                    'difficulty': 'Bajo',
                    'weather': 'Variable'
                },
                {
                    'day': 2,
                    'theme': 'Atracciones Principales',
                    'description': 'Visita a los monumentos icónicos de Nueva York',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno en Café Local', 'duration': '1h', 'cost': 20},
                        {'time': '10:00', 'name': 'Visita Estatua de la Libertad', 'duration': '4h', 'cost': 75},
                        {'time': '14:30', 'name': 'Almuerzo en Battery Park', 'duration': '1.5h', 'cost': 40},
                        {'time': '16:00', 'name': 'Paseo por Brooklyn Bridge', 'duration': '2h', 'cost': 0},
                        {'time': '19:00', 'name': 'Cena con vista al atardecer', 'duration': '2h', 'cost': 80},
                    ],
                    'meals': {
                        'breakfast': 'Café con bagel',
                        'lunch': 'Seafood en Battery Park',
                        'dinner': 'Restaurante con vista al puente'
                    },
                    'recommendations': [
                        'Llegar temprano a la Estatua de la Libertad',
                        'Llevar cámara para fotos',
                        'Usar protector solar'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Soleado'
                },
                {
                    'day': 3,
                    'theme': 'Cultura y Entretenimiento',
                    'description': 'Museos, Broadway y vida nocturna',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno Buffet', 'duration': '1h', 'cost': 25},
                        {'time': '10:00', 'name': 'Museo Metropolitano', 'duration': '3h', 'cost': 65},
                        {'time': '13:30', 'name': 'Almuerzo en Upper West Side', 'duration': '1.5h', 'cost': 45},
                        {'time': '15:00', 'name': 'Shopping en 5th Avenue', 'duration': '3h', 'cost': 100},
                        {'time': '19:00', 'name': 'Cena Pre-Teatro', 'duration': '1.5h', 'cost': 70},
                        {'time': '20:30', 'name': 'Musical en Broadway', 'duration': '2.5h', 'cost': 150},
                    ],
                    'meals': {
                        'breakfast': 'Desayuno buffet del hotel',
                        'lunch': 'Comida casual en Upper West Side',
                        'dinner': 'Restaurante cerca de Times Square'
                    },
                    'recommendations': [
                        'Reservar entradas de Broadway con anticipación',
                        'Usar zapatos cómodos para caminar',
                        'Llevar dinero en efectivo para propinas'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Parcialmente nublado'
                }
            ]
        },
        'PAR': {
            'theme': 'Romanticismo Parisino',
            'days': [
                {
                    'day': 1,
                    'theme': 'Bienvenido a París',
                    'description': 'Llegada y exploración de la Margen Izquierda',
                    'activities': [
                        {'time': '10:00', 'name': 'Llegada a CDG', 'duration': '2h', 'cost': 0},
                        {'time': '12:00', 'name': 'Traslado al Hotel', 'duration': '1h', 'cost': 45},
                        {'time': '14:00', 'name': 'Check-in y Descanso', 'duration': '1h', 'cost': 0},
                        {'time': '16:00', 'name': 'Paseo por Barrio Latino', 'duration': '2h', 'cost': 0},
                        {'time': '19:00', 'name': 'Cena en Bistró Tradicional', 'duration': '2h', 'cost': 65},
                    ],
                    'meals': {
                        'breakfast': 'En el hotel',
                        'lunch': 'Sándwich en el camino',
                        'dinner': 'Bistró tradicional parisino'
                    },
                    'recommendations': [
                        'Cambiar euros en el aeropuerto',
                        'Comprar pase de transporte semanal',
                        'Aprender frases básicas en francés'
                    ],
                    'difficulty': 'Bajo',
                    'weather': 'Templado'
                },
                {
                    'day': 2,
                    'theme': 'La Magia de la Torre Eiffel',
                    'description': 'Día dedicado a la Torre Eiffel y sus alrededores',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno Francés', 'duration': '1h', 'cost': 20},
                        {'time': '10:00', 'name': 'Subida Torre Eiffel', 'duration': '3h', 'cost': 85},
                        {'time': '13:30', 'name': 'Almuerzo en Café Cercano', 'duration': '1.5h', 'cost': 50},
                        {'time': '15:00', 'name': 'Paseo por Campos de Marte', 'duration': '2h', 'cost': 0},
                        {'time': '18:00', 'name': 'Crucero por el Sena', 'duration': '1.5h', 'cost': 60},
                        {'time': '20:00', 'name': 'Cena Romántica', 'duration': '2h', 'cost': 90},
                    ],
                    'meals': {
                        'breakfast': 'Croissants y café',
                        'lunch': 'Café parisino',
                        'dinner': 'Restaurante romántico'
                    },
                    'recommendations': [
                        'Subir a la Torre Eiffel al atardecer',
                        'Llevar cámara para fotos',
                        'Reservar crucero con anticipación'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Soleado'
                },
                {
                    'day': 3,
                    'theme': 'Arte y Cultura',
                    'description': 'Museos y monumentos históricos',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno en Hotel', 'duration': '1h', 'cost': 25},
                        {'time': '10:00', 'name': 'Museo del Louvre', 'duration': '4h', 'cost': 75},
                        {'time': '14:30', 'name': 'Almuerzo en Palacio Real', 'duration': '1.5h', 'cost': 55},
                        {'time': '16:00', 'name': 'Catedral de Notre-Dame', 'duration': '1.5h', 'cost': 0},
                        {'time': '18:00', 'name': 'Paseo por Île de la Cité', 'duration': '1.5h', 'cost': 0},
                        {'time': '20:00', 'name': 'Cena de Despedida', 'duration': '2h', 'cost': 85},
                    ],
                    'meals': {
                        'breakfast': 'Desayuno continental',
                        'lunch': 'Comida francesa tradicional',
                        'dinner': 'Cena de despedida especial'
                    },
                    'recommendations': [
                        'Llegar al Louvre temprano',
                        'Usar audioguía para mejor experiencia',
                        'Comprar souvenirs en tiendas locales'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Parcialmente nublado'
                }
            ]
        },
        'LON': {
            'theme': 'Londres Clásico',
            'days': [
                {
                    'day': 1,
                    'theme': 'Bienvenido a Londres',
                    'description': 'Llegada y exploración del centro histórico',
                    'activities': [
                        {'time': '10:00', 'name': 'Llegada a Heathrow', 'duration': '2h', 'cost': 0},
                        {'time': '12:00', 'name': 'Traslado al Hotel', 'duration': '1.5h', 'cost': 40},
                        {'time': '14:00', 'name': 'Check-in y Descanso', 'duration': '1h', 'cost': 0},
                        {'time': '16:00', 'name': 'Paseo por Westminster', 'duration': '2h', 'cost': 0},
                        {'time': '19:00', 'name': 'Cena Tradicional Británica', 'duration': '2h', 'cost': 70},
                    ],
                    'meals': {
                        'breakfast': 'En el hotel',
                        'lunch': 'Fish and Chips',
                        'dinner': 'Pub tradicional británico'
                    },
                    'recommendations': [
                        'Cambiar libras esterlinas',
                        'Comprar Oyster Card para transporte',
                        'Conducen por la izquierda'
                    ],
                    'difficulty': 'Bajo',
                    'weather': 'Nublado'
                },
                {
                    'day': 2,
                    'theme': 'Monumentos Icónicos',
                    'description': 'Big Ben, Palacio de Buckingham y más',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno Inglés Completo', 'duration': '1h', 'cost': 25},
                        {'time': '10:00', 'name': 'Cambio de Guardia en Buckingham', 'duration': '1.5h', 'cost': 0},
                        {'time': '12:00', 'name': 'Visita Palacio de Westminster', 'duration': '2h', 'cost': 60},
                        {'time': '14:30', 'name': 'Almuerzo en Westminster', 'duration': '1.5h', 'cost': 45},
                        {'time': '16:00', 'name': 'Paseo por Tower Bridge', 'duration': '2h', 'cost': 0},
                        {'time': '19:00', 'name': 'Cena con Vistas al Támesis', 'duration': '2h', 'cost': 80},
                    ],
                    'meals': {
                        'breakfast': 'Desayuno inglés',
                        'lunch': 'Comida tradicional',
                        'dinner': 'Restaurante con vistas'
                    },
                    'recommendations': [
                        'Llegar temprano al Cambio de Guardia',
                        'Llevar paraguas (clima impredecible)',
                        'Usar transporte público'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Variable'
                },
                {
                    'day': 3,
                    'theme': 'Museos y Compras',
                    'description': 'Museos gratuitos y compras en Oxford Street',
                    'activities': [
                        {'time': '09:00', 'name': 'Desayuno en Hotel', 'duration': '1h', 'cost': 25},
                        {'time': '10:00', 'name': 'Museo Británico', 'duration': '3h', 'cost': 0},
                        {'time': '13:30', 'name': 'Almuerzo en Bloomsbury', 'duration': '1.5h', 'cost': 40},
                        {'time': '15:00', 'name': 'Compras en Oxford Street', 'duration': '3h', 'cost': 150},
                        {'time': '19:00', 'name': 'Cena de Despedida', 'duration': '2h', 'cost': 75},
                    ],
                    'meals': {
                        'breakfast': 'Desayuno continental',
                        'lunch': 'Comida casual',
                        'dinner': 'Cena especial'
                    },
                    'recommendations': [
                        'Museo Británico es gratuito',
                        'Oxford Street es muy concurrida',
                        'Comprar souvenirs británicos'
                    ],
                    'difficulty': 'Moderado',
                    'weather': 'Parcialmente nublado'
                }
            ]
        }
    }
    
    # Obtener itinerario del destino o usar uno genérico
    destination_key = destination[:3].upper() if destination else 'NYC'
    itinerary_template = itineraries.get(destination_key, itineraries['NYC'])
    
    # Ajustar duración
    days = itinerary_template['days'][:duration]
    
    return {
        'destination': destination,
        'duration': duration,
        'theme': itinerary_template['theme'],
        'day_by_day': days,
        'cost_breakdown': {
            'flights': 850,
            'hotel': 150 * duration,
            'activities': 200 * duration,
            'food': 40 * travelers * duration
        }
    }


# Clase para generar reportes
class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FF6B35'),
            spaceAfter=30,
            alignment=1  # Center
        )
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#FF6B35'),
            spaceAfter=12
        )
    
    def generate_offers_pdf(self, travel_data: Dict) -> BytesIO:
        """Generar PDF de ofertas"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Título
        elements.append(Paragraph("✈️ REPORTE DE OFERTAS DE VIAJE", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Información general
        elements.append(Paragraph("Información del Viaje", self.heading_style))
        travel_info = [
            ["Origen", travel_data.get('origin', 'N/A')],
            ["Destino", travel_data.get('destination', 'N/A')],
            ["Fecha de Salida", travel_data.get('departure_date', 'N/A')],
            ["Fecha de Retorno", travel_data.get('return_date', 'N/A')],
            ["Viajeros", str(travel_data.get('travelers', 1))],
            ["Presupuesto", f"${travel_data.get('budget', 0):.0f}"],
        ]
        
        table = Table(travel_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF6B35')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Mejores ofertas
        elements.append(Paragraph("Mejores Ofertas Encontradas", self.heading_style))
        
        best_flight = travel_data.get('best_flight', {})
        elements.append(Paragraph("Vuelo Recomendado", self.styles['Heading3']))
        flight_info = [
            ["Aerolínea", best_flight.get('airline', 'N/A')],
            ["Precio", f"${best_flight.get('price', 0):.0f}"],
            ["Duración", best_flight.get('duration', 'N/A')],
            ["Escalas", str(best_flight.get('stops', 0))],
            ["Salida", best_flight.get('departure_time', 'N/A')],
            ["Llegada", best_flight.get('arrival_time', 'N/A')],
        ]
        
        flight_table = Table(flight_info, colWidths=[2*inch, 4*inch])
        flight_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(flight_table)
        elements.append(Spacer(1, 0.2*inch))
        
        best_hotel = travel_data.get('best_hotel', {})
        elements.append(Paragraph("Hotel Recomendado", self.styles['Heading3']))
        hotel_info = [
            ["Hotel", best_hotel.get('hotel_name', 'N/A')],
            ["Precio", f"${best_hotel.get('price', 0):.0f}"],
            ["Rating", f"{best_hotel.get('rating', 0)}/10"],
            ["Reviews", str(best_hotel.get('review_count', 0))],
            ["Distancia", best_hotel.get('distance', 'N/A')],
            ["Dirección", best_hotel.get('address', 'N/A')],
        ]
        
        hotel_table = Table(hotel_info, colWidths=[2*inch, 4*inch])
        hotel_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#2196F3')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(hotel_table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_itinerary_pdf(self, travel_data: Dict) -> BytesIO:
        """Generar PDF de itinerario"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        elements.append(Paragraph("📅 ITINERARIO DE VIAJE", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Información del viaje
        elements.append(Paragraph("Resumen del Viaje", self.heading_style))
        summary_info = [
            ["Destino", travel_data.get('destination', 'N/A')],
            ["Duración", f"{travel_data.get('trip_duration', 0)} días"],
            ["Fecha Inicio", travel_data.get('departure_date', 'N/A')],
            ["Fecha Fin", travel_data.get('return_date', 'N/A')],
        ]
        
        summary_table = Table(summary_info, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF6B35')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Actividades por día
        elements.append(Paragraph("Actividades Recomendadas", self.heading_style))
        activities = travel_data.get('recommended_activities', [])
        for i, activity in enumerate(activities, 1):
            elements.append(Paragraph(f"• {activity}", self.styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_analysis_pdf(self, travel_data: Dict) -> BytesIO:
        """Generar PDF de análisis de precios"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        elements.append(Paragraph("💰 ANÁLISIS DE PRECIOS", self.title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Métricas principales
        elements.append(Paragraph("Métricas de Precios", self.heading_style))
        metrics_info = [
            ["Costo Total", f"${travel_data.get('total_cost', 0):.0f}"],
            ["Precio de Mercado", f"${travel_data.get('market_average', 0):.0f}"],
            ["Ahorro Total", f"${travel_data.get('total_savings', 0):.0f}"],
            ["Porcentaje Ahorro", f"{travel_data.get('savings_percentage', 0):.1f}%"],
            ["Confianza IA", f"{travel_data.get('confidence_score', 0)*100:.0f}%"],
        ]
        
        metrics_table = Table(metrics_info, colWidths=[2.5*inch, 3.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(metrics_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Desglose de costos
        elements.append(Paragraph("Desglose de Costos", self.heading_style))
        cost_breakdown = [
            ["Vuelos", f"${travel_data.get('best_flight', {}).get('price', 0):.0f}"],
            ["Hotel", f"${travel_data.get('best_hotel', {}).get('price', 0):.0f}"],
            ["Actividades", f"${travel_data.get('estimated_activities_cost', 0):.0f}"],
            ["Comida", f"${travel_data.get('estimated_food_cost', 0):.0f}"],
        ]
        
        cost_table = Table(cost_breakdown, colWidths=[2.5*inch, 3.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        elements.append(cost_table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_excel_report(self, travel_data: Dict, report_type: str) -> BytesIO:
        """Generar reporte en Excel"""
        buffer = BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            if report_type in ['offers', 'full']:
                # Hoja de ofertas
                offers_data = {
                    'Tipo': ['Vuelo', 'Hotel'],
                    'Nombre': [
                        travel_data.get('best_flight', {}).get('airline', 'N/A'),
                        travel_data.get('best_hotel', {}).get('hotel_name', 'N/A')
                    ],
                    'Precio': [
                        travel_data.get('best_flight', {}).get('price', 0),
                        travel_data.get('best_hotel', {}).get('price', 0)
                    ],
                    'Rating': [
                        'N/A',
                        travel_data.get('best_hotel', {}).get('rating', 0)
                    ]
                }
                df_offers = pd.DataFrame(offers_data)
                df_offers.to_excel(writer, sheet_name='Ofertas', index=False)
            
            if report_type in ['analysis', 'full']:
                # Hoja de análisis
                analysis_data = {
                    'Métrica': ['Costo Total', 'Precio Mercado', 'Ahorro Total', 'Porcentaje Ahorro', 'Confianza IA'],
                    'Valor': [
                        travel_data.get('total_cost', 0),
                        travel_data.get('market_average', 0),
                        travel_data.get('total_savings', 0),
                        f"{travel_data.get('savings_percentage', 0):.1f}%",
                        f"{travel_data.get('confidence_score', 0)*100:.0f}%"
                    ]
                }
                df_analysis = pd.DataFrame(analysis_data)
                df_analysis.to_excel(writer, sheet_name='Análisis', index=False)
            
            if report_type in ['itinerary', 'full']:
                # Hoja de itinerario
                itinerary_data = {
                    'Destino': [travel_data.get('destination', 'N/A')],
                    'Duración (días)': [travel_data.get('trip_duration', 0)],
                    'Fecha Inicio': [travel_data.get('departure_date', 'N/A')],
                    'Fecha Fin': [travel_data.get('return_date', 'N/A')],
                    'Viajeros': [travel_data.get('travelers', 1)]
                }
                df_itinerary = pd.DataFrame(itinerary_data)
                df_itinerary.to_excel(writer, sheet_name='Itinerario', index=False)
        
        buffer.seek(0)
        return buffer

@app.post("/optimize-travel", response_model=TravelOptimizationResponse)
async def optimize_travel(request: TravelDataRequest):
    try:
        optimizer = TravelAIOptimizer()
        
        # Encontrar mejores opciones
        best_flight = optimizer.find_best_flight(request.flight_data)
        best_hotel = optimizer.find_best_hotel(request.hotel_data)
        
        # Generar alternativas (simuladas)
        alternatives = []
        if best_flight:
            alternatives.append({
                'type': 'flight',
                'description': 'Vuelo con escala - Más económico',
                'price': best_flight.get('price', 0) * 0.8,
                'savings': best_flight.get('price', 0) * 0.2
            })
        
        if best_hotel:
            alternatives.append({
                'type': 'hotel',
                'description': 'Hotel 3 estrellas - Buena relación calidad-precio',
                'price': best_hotel.get('price', 0) * 0.7,
                'savings': best_hotel.get('price', 0) * 0.3
            })
        
        # Calcular promedio de mercado
        flight_features = optimizer.extract_flight_features(request.flight_data)
        hotel_features = optimizer.extract_hotel_features(request.hotel_data)
        
        market_average = (flight_features[0] + hotel_features[0]) * 1.1  # +10% como margen
        
        # Generar recomendaciones
        recommendations = optimizer.generate_recommendations(
            request.user_preferences, best_flight, best_hotel
        )
        
        # Calcular costos estimados
        duration = request.user_preferences.get('trip_duration', 0)
        estimated_activities_cost = duration * 25  # $25 por día en actividades
        estimated_food_cost = duration * request.user_preferences.get('travelers', 1) * 40  # $40 por persona por día
        
        # Actividades recomendadas
        recommended_activities = [
            'Tour gastronómico local',
            'Visita a atracciones principales',
            'Experiencia cultural única',
            'Tour de compras en mercados locales'
        ]
        
        # Generar itinerario detallado
        itinerary = generate_detailed_itinerary(
            request.user_preferences.get('destination', 'N/A'),
            request.user_preferences.get('trip_duration', 0),
            request.user_preferences.get('travelers', 1)
        )
        
        return TravelOptimizationResponse(
            best_flight=best_flight,
            best_hotel=best_hotel,
            alternatives=alternatives,
            market_average=float(market_average),
            recommendations=recommendations,
            confidence_score=0.85,
            estimated_activities_cost=float(estimated_activities_cost),
            estimated_food_cost=float(estimated_food_cost),
            recommended_activities=recommended_activities
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Travel optimization error: {str(e)}")

@app.post("/download-report")
async def download_report(request: ReportRequest):
    """Descargar reporte en PDF o Excel"""
    try:
        generator = ReportGenerator()
        report_type = request.report_type
        format_type = request.format
        
        if format_type == 'pdf':
            if report_type == 'offers':
                buffer = generator.generate_offers_pdf(request.travel_data)
                filename = f"ofertas_viaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            elif report_type == 'itinerary':
                buffer = generator.generate_itinerary_pdf(request.travel_data)
                filename = f"itinerario_viaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            elif report_type == 'analysis':
                buffer = generator.generate_analysis_pdf(request.travel_data)
                filename = f"analisis_precios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            else:
                # Generar reporte completo
                buffer = BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=letter)
                elements = []
                
                # Agregar todas las secciones
                generator_instance = ReportGenerator()
                # Ofertas
                offers_buffer = generator_instance.generate_offers_pdf(request.travel_data)
                # Itinerario
                itinerary_buffer = generator_instance.generate_itinerary_pdf(request.travel_data)
                # Análisis
                analysis_buffer = generator_instance.generate_analysis_pdf(request.travel_data)
                
                filename = f"reporte_completo_viaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                buffer = offers_buffer  # Simplificado: devolver ofertas como reporte completo
        
        elif format_type == 'excel':
            buffer = generator.generate_excel_report(request.travel_data, report_type)
            filename = f"reporte_viaje_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        else:
            raise HTTPException(status_code=400, detail="Formato no soportado. Use 'pdf' o 'excel'")
        
        return StreamingResponse(
            iter([buffer.getvalue()]),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")

@app.get("/statistics")
async def get_statistics():
    """Obtener estadísticas generales del sistema"""
    try:
        stats = {
            "total_searches": 0,
            "average_savings": 0,
            "most_popular_destination": "N/A",
            "average_trip_duration": 0,
            "total_users": 0,
            "timestamp": datetime.now().isoformat()
        }
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching statistics: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
