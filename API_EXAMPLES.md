# 📚 Ejemplos de Uso de la API

## 🔗 Endpoints Disponibles

### 1. POST `/optimize-travel` (Existente)
Optimizar viaje y obtener mejores ofertas

### 2. POST `/download-report` (Nuevo)
Descargar reportes en PDF o Excel

### 3. GET `/statistics` (Nuevo)
Obtener estadísticas del sistema

---

## 📥 Descargar Reportes

### Endpoint
```
POST http://localhost:8002/download-report
```

### Headers
```
Content-Type: application/json
```

### Body - Reporte de Ofertas (PDF)
```json
{
  "travel_data": {
    "origin": "NYC",
    "destination": "PAR",
    "departure_date": "2024-02-15",
    "return_date": "2024-02-22",
    "travelers": 2,
    "budget": 5000,
    "trip_duration": 7,
    "best_flight": {
      "airline": "Air France",
      "price": 850,
      "duration": "7h 30m",
      "stops": 0,
      "departure_time": "10:00 AM",
      "arrival_time": "10:30 PM"
    },
    "best_hotel": {
      "hotel_name": "Hotel Le Marais",
      "price": 150,
      "rating": 8.5,
      "review_count": 245,
      "distance": "2 km",
      "address": "75003 Paris, France"
    },
    "total_cost": 3500,
    "market_average": 4200,
    "total_savings": 700,
    "savings_percentage": 16.7,
    "confidence_score": 0.85,
    "estimated_activities_cost": 200,
    "estimated_food_cost": 400,
    "recommended_activities": [
      "Tour gastronómico local",
      "Visita a atracciones principales",
      "Experiencia cultural única"
    ]
  },
  "report_type": "offers",
  "format": "pdf"
}
```

### Respuesta
```
Content-Type: application/octet-stream
Content-Disposition: attachment; filename=ofertas_viaje_20240115_103000.pdf

[Contenido del archivo PDF]
```

---

## 📊 Ejemplos con cURL

### Descargar Reporte de Ofertas (PDF)
```bash
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{
    "travel_data": {
      "origin": "NYC",
      "destination": "PAR",
      "departure_date": "2024-02-15",
      "return_date": "2024-02-22",
      "travelers": 2,
      "budget": 5000,
      "trip_duration": 7,
      "best_flight": {
        "airline": "Air France",
        "price": 850,
        "duration": "7h 30m",
        "stops": 0,
        "departure_time": "10:00 AM",
        "arrival_time": "10:30 PM"
      },
      "best_hotel": {
        "hotel_name": "Hotel Le Marais",
        "price": 150,
        "rating": 8.5,
        "review_count": 245,
        "distance": "2 km",
        "address": "75003 Paris, France"
      },
      "total_cost": 3500,
      "market_average": 4200,
      "total_savings": 700,
      "savings_percentage": 16.7,
      "confidence_score": 0.85,
      "estimated_activities_cost": 200,
      "estimated_food_cost": 400,
      "recommended_activities": ["Tour gastronómico", "Visita cultural"]
    },
    "report_type": "offers",
    "format": "pdf"
  }' \
  -o ofertas.pdf
```

### Descargar Reporte de Itinerario (PDF)
```bash
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{
    "travel_data": {
      "destination": "PAR",
      "departure_date": "2024-02-15",
      "return_date": "2024-02-22",
      "trip_duration": 7,
      "recommended_activities": [
        "Tour gastronómico local",
        "Visita a atracciones principales",
        "Experiencia cultural única"
      ]
    },
    "report_type": "itinerary",
    "format": "pdf"
  }' \
  -o itinerario.pdf
```

### Descargar Reporte de Análisis (PDF)
```bash
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{
    "travel_data": {
      "total_cost": 3500,
      "market_average": 4200,
      "total_savings": 700,
      "savings_percentage": 16.7,
      "confidence_score": 0.85,
      "best_flight": {"price": 850},
      "best_hotel": {"price": 150},
      "estimated_activities_cost": 200,
      "estimated_food_cost": 400
    },
    "report_type": "analysis",
    "format": "pdf"
  }' \
  -o analisis.pdf
```

### Descargar Reporte de Ofertas (Excel)
```bash
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{
    "travel_data": {...},
    "report_type": "offers",
    "format": "excel"
  }' \
  -o ofertas.xlsx
```

### Obtener Estadísticas
```bash
curl -X GET http://localhost:8002/statistics \
  -H "Content-Type: application/json"
```

---

## 🐍 Ejemplos con Python

### Descargar Reporte con Requests
```python
import requests

url = "http://localhost:8002/download-report"

payload = {
    "travel_data": {
        "origin": "NYC",
        "destination": "PAR",
        "departure_date": "2024-02-15",
        "return_date": "2024-02-22",
        "travelers": 2,
        "budget": 5000,
        "trip_duration": 7,
        "best_flight": {
            "airline": "Air France",
            "price": 850,
            "duration": "7h 30m",
            "stops": 0,
            "departure_time": "10:00 AM",
            "arrival_time": "10:30 PM"
        },
        "best_hotel": {
            "hotel_name": "Hotel Le Marais",
            "price": 150,
            "rating": 8.5,
            "review_count": 245,
            "distance": "2 km",
            "address": "75003 Paris, France"
        },
        "total_cost": 3500,
        "market_average": 4200,
        "total_savings": 700,
        "savings_percentage": 16.7,
        "confidence_score": 0.85,
        "estimated_activities_cost": 200,
        "estimated_food_cost": 400,
        "recommended_activities": ["Tour gastronómico", "Visita cultural"]
    },
    "report_type": "offers",
    "format": "pdf"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    with open("ofertas.pdf", "wb") as f:
        f.write(response.content)
    print("✅ Reporte descargado exitosamente")
else:
    print(f"❌ Error: {response.status_code}")
```

### Obtener Estadísticas con Python
```python
import requests
import json

url = "http://localhost:8002/statistics"

response = requests.get(url)

if response.status_code == 200:
    stats = response.json()
    print(json.dumps(stats, indent=2))
else:
    print(f"Error: {response.status_code}")
```

---

## 📱 Ejemplos con JavaScript/Fetch

### Descargar Reporte
```javascript
const downloadReport = async () => {
  const payload = {
    travel_data: {
      origin: "NYC",
      destination: "PAR",
      departure_date: "2024-02-15",
      return_date: "2024-02-22",
      travelers: 2,
      budget: 5000,
      trip_duration: 7,
      best_flight: {
        airline: "Air France",
        price: 850,
        duration: "7h 30m",
        stops: 0,
        departure_time: "10:00 AM",
        arrival_time: "10:30 PM"
      },
      best_hotel: {
        hotel_name: "Hotel Le Marais",
        price: 150,
        rating: 8.5,
        review_count: 245,
        distance: "2 km",
        address: "75003 Paris, France"
      },
      total_cost: 3500,
      market_average: 4200,
      total_savings: 700,
      savings_percentage: 16.7,
      confidence_score: 0.85,
      estimated_activities_cost: 200,
      estimated_food_cost: 400,
      recommended_activities: ["Tour gastronómico", "Visita cultural"]
    },
    report_type: "offers",
    format: "pdf"
  };

  try {
    const response = await fetch("http://localhost:8002/download-report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "ofertas.pdf";
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      console.log("✅ Reporte descargado");
    } else {
      console.error("❌ Error:", response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
```

### Obtener Estadísticas
```javascript
const getStatistics = async () => {
  try {
    const response = await fetch("http://localhost:8002/statistics");
    const stats = await response.json();
    console.log(stats);
    return stats;
  } catch (error) {
    console.error("Error:", error);
  }
};
```

---

## 🔍 Códigos de Respuesta

| Código | Significado |
|--------|------------|
| 200 | Éxito - Archivo descargado |
| 400 | Solicitud inválida |
| 500 | Error del servidor |

---

## 📋 Tipos de Reporte

| Tipo | Descripción |
|------|------------|
| `offers` | Vuelos y hoteles recomendados |
| `itinerary` | Itinerario de viaje día por día |
| `analysis` | Análisis de precios y ahorros |
| `full` | Reporte completo (todas las secciones) |

---

## 📄 Formatos Soportados

| Formato | Extensión | Tipo MIME |
|---------|-----------|-----------|
| `pdf` | .pdf | application/pdf |
| `excel` | .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet |

---

## 🧪 Prueba Rápida

```bash
# 1. Obtener estadísticas
curl http://localhost:8002/statistics

# 2. Descargar reporte (ver ejemplo arriba)
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{...}' \
  -o reporte.pdf
```

---

## ⚠️ Notas Importantes

1. **Servidor debe estar ejecutándose:** `python travel_ai_server.py`
2. **Datos completos:** Proporciona todos los campos requeridos
3. **Timeout:** Espera hasta 30 segundos para la descarga
4. **Tamaño:** Los archivos se generan en memoria

---

## 🔗 Documentación Relacionada

- [FastAPI Docs](http://localhost:8002/docs) - Documentación interactiva
- [README_REPORTES.md](./README_REPORTES.md) - Documentación completa
- [SETUP.md](./SETUP.md) - Guía de instalación

---

**Versión:** 2.0  
**Última actualización:** Enero 2024
