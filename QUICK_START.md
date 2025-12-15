# ⚡ Inicio Rápido

## 🚀 En 5 Minutos

### 1. Instalar (1 minuto)
```bash
cd c:\Users\veras\Music\Viajes
pip install -r requirements.txt
```

### 2. Ejecutar Servidor (Terminal 1)
```bash
python travel_ai_server.py
```
✅ Espera a ver: `Uvicorn running on http://0.0.0.0:8002`

### 3. Ejecutar App (Terminal 2)
```bash
streamlit run travel_app.py
```
✅ Se abrirá automáticamente en http://localhost:8501

### 4. Usar la App
1. Completa los datos en el panel lateral
2. Haz clic en "🚀 Buscar Mejores Ofertas con IA"
3. Ve a la pestaña "🎯 Ofertas"
4. Haz clic en los botones de descarga

---

## 📥 Descargar Reportes

### Desde la UI
```
1. Realiza una búsqueda de viaje
2. Pestaña "🎯 Ofertas"
3. Sección "📥 Descargar Reportes"
4. Elige:
   - 📄 Ofertas PDF
   - 📊 Ofertas Excel
   - 📋 Itinerario PDF
   - 💹 Análisis PDF
```

### Desde API (cURL)
```bash
curl -X POST http://localhost:8002/download-report \
  -H "Content-Type: application/json" \
  -d '{
    "travel_data": {...},
    "report_type": "offers",
    "format": "pdf"
  }' \
  -o reporte.pdf
```

---

## 📊 Ver Estadísticas

```
1. Pestaña "📊 Estadísticas"
2. Métricas clave
3. Gráficos de tendencias
4. Destinos populares
```

---

## 🧪 Probar Todo

```bash
python test_reports.py
```

Genera archivos de prueba en el directorio actual.

---

## 📁 Archivos Importantes

| Archivo | Función |
|---------|---------|
| `travel_ai_server.py` | Servidor API |
| `travel_app.py` | Interfaz web |
| `config.py` | Configuración |
| `test_reports.py` | Pruebas |
| `README_REPORTES.md` | Documentación |
| `SETUP.md` | Instalación |

---

## 🆘 Problemas Comunes

### "Connection refused"
```bash
# Verifica que el servidor está ejecutándose
python travel_ai_server.py
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### Puerto ocupado
```bash
# Cambiar puerto en travel_ai_server.py
uvicorn.run(app, host="0.0.0.0", port=8003)
```

---

## 🎯 Próximos Pasos

1. ✅ Instalar y ejecutar
2. ✅ Realizar una búsqueda
3. ✅ Descargar un reporte
4. ✅ Ver estadísticas
5. ✅ Explorar más características

---

## 📚 Más Información

- **Documentación completa:** `README_REPORTES.md`
- **Guía de instalación:** `SETUP.md`
- **Cambios realizados:** `CAMBIOS.md`
- **Configuración:** `config.py`

---

¡Listo! 🎉 Ahora puedes descargar reportes de tus viajes.
