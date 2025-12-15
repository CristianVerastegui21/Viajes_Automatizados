# 🧳 Travel AI Planner - Sistema de Reportes y Descargas

## 📋 Descripción General

Se ha agregado funcionalidad completa de **reportes estadísticos** y **descargas** al sistema de planificación de viajes automatizados. Ahora puedes descargar tus ofertas, itinerarios, análisis e historial en formato PDF y Excel.

## ✨ Nuevas Características

### 1. **Descargas de Reportes**
- 📄 **Reporte de Ofertas** (PDF/Excel) - Vuelos y hoteles recomendados
- 📅 **Itinerario de Viaje** (PDF) - Detalles del viaje día por día
- 💰 **Análisis de Precios** (PDF) - Desglose de costos y ahorros
- 📊 **Reporte Completo** (PDF) - Todas las secciones en un documento

### 2. **Estadísticas del Sistema**
- 📊 Total de búsquedas realizadas
- 💵 Ahorro promedio en viajes
- 🌍 Destinos más populares
- 👥 Usuarios activos
- 📈 Gráficos de tendencias

### 3. **Nuevos Endpoints API**

#### POST `/download-report`
Descargar reportes en PDF o Excel

**Parámetros:**
```json
{
  "travel_data": {
    "origin": "NYC",
    "destination": "PAR",
    "departure_date": "2024-02-15",
    "return_date": "2024-02-22",
    "travelers": 2,
    "budget": 5000,
    "best_flight": {...},
    "best_hotel": {...},
    "total_cost": 3500,
    "market_average": 4200,
    "total_savings": 700,
    "savings_percentage": 16.7,
    "confidence_score": 0.85,
    "estimated_activities_cost": 200,
    "estimated_food_cost": 400,
    "recommended_activities": [...]
  },
  "report_type": "offers|itinerary|analysis|full",
  "format": "pdf|excel"
}
```

#### GET `/statistics`
Obtener estadísticas del sistema

**Respuesta:**
```json
{
  "total_searches": 150,
  "average_savings": 18.5,
  "most_popular_destination": "París",
  "average_trip_duration": 7,
  "total_users": 45,
  "timestamp": "2024-01-15T10:30:00"
}
```

## 🚀 Cómo Usar

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar el Servidor FastAPI

```bash
python travel_ai_server.py
```

El servidor estará disponible en `http://localhost:8002`

### Ejecutar la Aplicación Streamlit

```bash
streamlit run travel_app.py
```

La aplicación estará disponible en `http://localhost:8501`

## 📥 Descargar Reportes desde la UI

1. **Realiza una búsqueda de viaje** en el panel lateral
2. **Ve a la pestaña "🎯 Ofertas"**
3. **Desplázate hasta la sección "📥 Descargar Reportes"**
4. **Elige el tipo y formato:**
   - Ofertas PDF/Excel
   - Itinerario PDF
   - Análisis PDF

## 📊 Pestaña de Estadísticas

Una nueva pestaña **"📊 Estadísticas"** muestra:
- Métricas clave del sistema
- Gráficos de tendencias de búsquedas
- Destinos más populares
- Información de usuarios activos

## 🔧 Estructura de Reportes

### Reporte de Ofertas
```
- Información del Viaje
  - Origen, Destino, Fechas
  - Número de Viajeros
  - Presupuesto
- Mejores Ofertas
  - Vuelo Recomendado
  - Hotel Recomendado
```

### Reporte de Itinerario
```
- Resumen del Viaje
  - Destino, Duración
  - Fechas de Inicio/Fin
- Actividades Recomendadas
```

### Reporte de Análisis
```
- Métricas de Precios
  - Costo Total
  - Precio de Mercado
  - Ahorro Total
  - Porcentaje de Ahorro
  - Confianza IA
- Desglose de Costos
  - Vuelos, Hotel, Actividades, Comida
```

## 🎨 Estilos y Colores

Los reportes PDF utilizan:
- **Naranja (#FF6B35)** - Títulos y encabezados principales
- **Verde (#4CAF50)** - Información de vuelos
- **Azul (#2196F3)** - Información de hoteles
- **Naranja claro (#FF9800)** - Desglose de costos

## 📝 Notas Técnicas

### Librerías Utilizadas
- **reportlab** - Generación de PDFs
- **openpyxl** - Generación de archivos Excel
- **pandas** - Manipulación de datos
- **fastapi** - API REST
- **streamlit** - Interfaz de usuario

### Configuración del Servidor

El servidor FastAPI está configurado para:
- Escuchar en `0.0.0.0:8002`
- Aceptar CORS desde cualquier origen
- Procesar solicitudes de reportes de forma asincrónica

## 🔐 Consideraciones de Seguridad

- Los reportes se generan en memoria (BytesIO)
- No se almacenan archivos en el servidor
- Los datos se transmiten a través de HTTPS (recomendado en producción)

## 🐛 Troubleshooting

### Error: "No se pudieron cargar las estadísticas"
- Asegúrate de que el servidor FastAPI está ejecutándose
- Verifica que el puerto 8002 está disponible

### Error al descargar reportes
- Comprueba que el servidor está activo
- Verifica que los datos del viaje están completos
- Revisa los logs del servidor para más detalles

## 📈 Mejoras Futuras

- [ ] Reportes en más idiomas
- [ ] Gráficos personalizados en PDFs
- [ ] Exportación a Google Sheets
- [ ] Reportes automáticos por email
- [ ] Análisis histórico avanzado
- [ ] Comparativa de múltiples viajes

## 📞 Soporte

Para reportar problemas o sugerencias, contacta al equipo de desarrollo.

---

**Versión:** 2.0  
**Última actualización:** Enero 2024
