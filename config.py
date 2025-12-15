# Configuración de la aplicación Travel AI

# Configuración del Servidor FastAPI
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8002
SERVER_URL = f"http://localhost:{SERVER_PORT}"

# Configuración de Streamlit
STREAMLIT_PORT = 8501
STREAMLIT_URL = f"http://localhost:{STREAMLIT_PORT}"

# Configuración de Reportes
REPORT_FORMATS = ["pdf", "excel"]
REPORT_TYPES = ["offers", "itinerary", "analysis", "full"]

# Configuración de Estilos
COLORS = {
    "primary": "#FF6B35",      # Naranja
    "success": "#4CAF50",      # Verde
    "info": "#2196F3",         # Azul
    "warning": "#FF9800",      # Naranja claro
    "danger": "#F44336"        # Rojo
}

# Configuración de Supabase
SUPABASE_TABLES = {
    "travel_searches": "travel_searches",
    "users": "users",
    "statistics": "statistics"
}

# Configuración de Timeouts
REQUEST_TIMEOUT = 30
SEARCH_TIMEOUT = 90

# Configuración de Límites
MAX_TRAVELERS = 10
MIN_TRAVELERS = 1
MAX_TRIP_DURATION = 365
MIN_TRIP_DURATION = 1

# Configuración de Monedas Soportadas
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "JPY", "MXN", "ARS", "COP"]

# Configuración de Idiomas
SUPPORTED_LANGUAGES = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR"]

# Configuración de Estilos de Viaje
TRAVEL_STYLES = {
    "budget": "💰 Económico",
    "comfort": "😊 Confort",
    "luxury": "💎 Lujo"
}

# Configuración de Destinos Populares
POPULAR_DESTINATIONS = {
    "NYC": "Nueva York",
    "PAR": "París",
    "LON": "Londres",
    "ROM": "Roma",
    "TYO": "Tokio",
    "BCN": "Barcelona",
    "MIA": "Miami",
    "LAX": "Los Ángeles",
    "SYD": "Sídney",
    "DXB": "Dubái"
}

# Configuración de Actividades por Destino
ACTIVITIES_BY_DESTINATION = {
    "NYC": [
        "Visitar Central Park",
        "Subir al Empire State",
        "Ver un musical en Broadway",
        "Recorrer Times Square",
        "Visitar el Museo Metropolitano"
    ],
    "PAR": [
        "Subir a la Torre Eiffel",
        "Visitar el Louvre",
        "Pasear por Montmartre",
        "Recorrer Notre-Dame",
        "Visitar Versalles"
    ],
    "LON": [
        "Ver el Cambio de Guardia",
        "Visitar el British Museum",
        "Pasear por el Thames",
        "Visitar Big Ben",
        "Recorrer Tower Bridge"
    ],
    "ROM": [
        "Visitar el Coliseo",
        "Tirar una moneda en Fontana di Trevi",
        "Ver el Vaticano",
        "Visitar el Foro Romano",
        "Recorrer la Capilla Sixtina"
    ],
    "TYO": [
        "Visitar Sensō-ji",
        "Cruzar el Shibuya Crossing",
        "Probar sushi en Tsukiji",
        "Visitar Meiji Shrine",
        "Explorar Akihabara"
    ]
}

# Configuración de Costos Estimados
ESTIMATED_COSTS = {
    "activities_per_day": 25,  # USD
    "food_per_person_per_day": 40,  # USD
    "transport_per_day": 15  # USD
}

# Configuración de Confianza de IA
AI_CONFIDENCE_THRESHOLD = 0.75
AI_CONFIDENCE_MULTIPLIER = 1.0

# Configuración de Ahorros
SAVINGS_MULTIPLIER = 1.1  # 10% sobre el promedio de mercado

# Configuración de Logging
LOG_LEVEL = "INFO"
LOG_FILE = "travel_ai.log"

# Configuración de Caché
CACHE_ENABLED = True
CACHE_TTL = 3600  # segundos

# Configuración de Base de Datos
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20

# Configuración de Validación
VALIDATE_EMAIL = True
VALIDATE_PHONE = True

# Configuración de Notificaciones
ENABLE_EMAIL_NOTIFICATIONS = True
ENABLE_SMS_NOTIFICATIONS = False
ENABLE_PUSH_NOTIFICATIONS = False

# Configuración de Análisis
ENABLE_ANALYTICS = True
ANALYTICS_SAMPLE_RATE = 1.0  # 100%

# Configuración de Seguridad
CORS_ORIGINS = ["*"]  # Cambiar en producción
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Configuración de Rate Limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_PERIOD = 3600  # segundos

# Configuración de Validación de Datos
VALIDATE_INPUT_DATA = True
SANITIZE_INPUT = True

# Configuración de Errores
SHOW_ERROR_DETAILS = True
ERROR_LOG_FILE = "errors.log"
