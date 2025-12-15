# 🚀 Guía de Instalación y Ejecución

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

## Paso 1: Instalación de Dependencias

### Opción A: Instalación Completa

```bash
# Navegar al directorio del proyecto
cd c:\Users\veras\Music\Viajes

# Instalar todas las dependencias
pip install -r requirements.txt
```

### Opción B: Instalación en Entorno Virtual (Recomendado)

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Paso 2: Configuración

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Supabase
SUPABASE_URL=tu_url_supabase
SUPABASE_KEY=tu_clave_supabase

# n8n Webhook
N8N_WEBHOOK_URL=tu_webhook_url

# Servidor
SERVER_HOST=0.0.0.0
SERVER_PORT=8002

# Streamlit
STREAMLIT_PORT=8501
```

## Paso 3: Ejecutar la Aplicación

### Terminal 1: Iniciar el Servidor FastAPI

```bash
# Activar entorno virtual (si lo creaste)
venv\Scripts\activate

# Ejecutar servidor
python travel_ai_server.py
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://0.0.0.0:8002
INFO:     Application startup complete
```

### Terminal 2: Iniciar la Aplicación Streamlit

```bash
# Abrir una nueva terminal en el mismo directorio

# Activar entorno virtual (si lo creaste)
venv\Scripts\activate

# Ejecutar Streamlit
streamlit run travel_app.py
```

**Salida esperada:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

## Paso 4: Acceder a la Aplicación

Abre tu navegador web y ve a:
- **Aplicación Principal:** http://localhost:8501
- **API Documentation:** http://localhost:8002/docs

## Pruebas

### Ejecutar Pruebas de Reportes

```bash
# En una tercera terminal

# Activar entorno virtual
venv\Scripts\activate

# Ejecutar pruebas
python test_reports.py
```

## Estructura del Proyecto

```
Viajes/
├── travel_ai_server.py          # Servidor FastAPI con generador de reportes
├── travel_app.py                # Aplicación Streamlit
├── config.py                    # Configuración centralizada
├── test_reports.py              # Script de pruebas
├── requirements.txt             # Dependencias
├── README_REPORTES.md           # Documentación de reportes
├── SETUP.md                     # Este archivo
├── .env                         # Variables de entorno (crear)
├── .streamlit/
│   └── config.toml             # Configuración de Streamlit
└── n8n_data/                   # Datos de n8n
```

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'reportlab'"

```bash
pip install reportlab
```

### Error: "ModuleNotFoundError: No module named 'openpyxl'"

```bash
pip install openpyxl
```

### Error: "Connection refused" al descargar reportes

1. Verifica que el servidor FastAPI está ejecutándose
2. Comprueba que el puerto 8002 está disponible
3. Revisa que no hay firewall bloqueando la conexión

### Error: "Streamlit is not installed"

```bash
pip install streamlit
```

### Puerto 8501 ya está en uso

```bash
# Usar un puerto diferente
streamlit run travel_app.py --server.port 8502
```

### Puerto 8002 ya está en uso

Edita `travel_ai_server.py` y cambia:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)  # Cambiar puerto
```

## Verificación de Instalación

Ejecuta este comando para verificar que todo está instalado:

```bash
python -c "import streamlit; import fastapi; import reportlab; import openpyxl; print('✅ Todas las dependencias están instaladas')"
```

## Configuración Avanzada

### Cambiar URL del Servidor

En `travel_app.py`, busca:
```python
server_url = "http://localhost:8002"
```

Y cambia a tu URL del servidor.

### Habilitar HTTPS

En `travel_ai_server.py`, usa:
```bash
uvicorn travel_ai_server:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

### Ejecutar en Producción

Para ejecutar en producción, usa Gunicorn:

```bash
pip install gunicorn

gunicorn -w 4 -k uvicorn.workers.UvicornWorker travel_ai_server:app
```

## Logs y Debugging

### Ver logs del servidor

Los logs se mostrarán en la terminal donde ejecutaste `python travel_ai_server.py`

### Ver logs de Streamlit

Los logs se mostrarán en la terminal donde ejecutaste `streamlit run travel_app.py`

### Habilitar modo debug

En `travel_app.py`, agrega:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Próximos Pasos

1. ✅ Instalar dependencias
2. ✅ Configurar variables de entorno
3. ✅ Ejecutar servidor y aplicación
4. ✅ Acceder a http://localhost:8501
5. ✅ Realizar una búsqueda de viaje
6. ✅ Descargar un reporte

## Soporte

Si encuentras problemas:

1. Revisa los logs en la terminal
2. Verifica que todos los puertos están disponibles
3. Asegúrate de que Python 3.8+ está instalado
4. Intenta reinstalar las dependencias

```bash
pip install --upgrade -r requirements.txt
```

## Recursos Útiles

- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [Documentación de ReportLab](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Documentación de OpenPyXL](https://openpyxl.readthedocs.io/)

---

**Última actualización:** Enero 2024
