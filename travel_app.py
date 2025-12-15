import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
from datetime import datetime, timedelta
from supabase import create_client
import time
import base64
from io import BytesIO

# Configuración de página
st.set_page_config(
    page_title="AI Travel Planner - Optimizador de Precios",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cliente Supabase
@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 1rem;
    }
    .savings-excellent {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .savings-good {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .savings-poor {
        background: linear-gradient(135deg, #F44336, #D32F2F);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B35;
        margin-bottom: 1rem;
    }
    .deal-card {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin-bottom: 0.5rem;
    }
    .affiliate-button {
        background-color: #FF6B35;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

def trigger_travel_search(travel_data):
    """Disparar búsqueda de viajes en n8n"""
    n8n_webhook_url = st.secrets["N8N_WEBHOOK_URL"]
    
    try:
        response = requests.post(n8n_webhook_url, json=travel_data, timeout=90)
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, f"Connection error: {str(e)}"

def download_report(travel_data, report_type, format_type):
    """Descargar reporte desde el servidor"""
    try:
        server_url = "http://localhost:8002"  # Cambiar según tu configuración
        
        payload = {
            "travel_data": travel_data,
            "report_type": report_type,
            "format": format_type
        }
        
        response = requests.post(f"{server_url}/download-report", json=payload, timeout=30)
        
        if response.status_code == 200:
            return True, response.content
        else:
            return False, f"Error: {response.status_code}"
    except Exception as e:
        return False, f"Error descargando reporte: {str(e)}"

def get_statistics():
    """Obtener estadísticas del sistema"""
    try:
        server_url = "http://localhost:8002"
        response = requests.get(f"{server_url}/statistics", timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        st.warning(f"No se pudieron cargar las estadísticas: {str(e)}")
        return None

def fetch_travel_history(user_id):
    """Obtener historial de búsquedas del usuario"""
    supabase = init_supabase()
    
    try:
        response = supabase.table('travel_searches')\
                         .select('*')\
                         .eq('user_id', user_id)\
                         .order('search_completed_at', desc=True)\
                         .limit(20)\
                         .execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching travel history: {e}")
        return pd.DataFrame()

def create_price_comparison_chart(result):
    """Crear gráfico de comparación de precios"""
    total_cost = result.get('total_cost', 0)
    market_average = result.get('market_average', total_cost * 1.2)
    
    categories = ['Tu Precio', 'Promedio Mercado']
    prices = [total_cost, market_average]
    
    fig = go.Figure(data=[
        go.Bar(name='Costo Total', x=categories, y=prices,
               marker_color=['#4CAF50', '#FF9800'])
    ])
    
    fig.update_layout(
        title="Comparación de Precios",
        yaxis_title="Precio (USD)",
        showlegend=False,
        height=400
    )
    
    return fig

def create_cost_breakdown_chart(itinerary):
    """Crear gráfico de desglose de costos"""
    cost_breakdown = itinerary.get('cost_breakdown', {})
    
    labels = ['Vuelos', 'Hotel', 'Actividades', 'Comida']
    values = [
        cost_breakdown.get('flights', 0),
        cost_breakdown.get('hotel', 0),
        cost_breakdown.get('activities', 0),
        cost_breakdown.get('food', 0)
    ]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title="Desglose de Costos", height=400)
    
    return fig

def create_itinerary_timeline(itinerary):
    """Crear línea de tiempo del itinerario"""
    day_by_day = itinerary.get('day_by_day', [])
    
    if not day_by_day:
        return None
    
    fig = go.Figure()
    
    for i, day in enumerate(day_by_day):
        fig.add_trace(go.Scatter(
            x=[day['date'], day['date']],
            y=[i, i],
            mode='markers+text',
            marker=dict(size=20, color='#FF6B35'),
            text=[f"Día {day['day']}", f"Día {day['day']}"],
            textposition="middle right",
            name=f"Día {day['day']}"
        ))
        
        # Agregar actividades
        activities = day.get('activities', [])
        for j, activity in enumerate(activities):
            fig.add_annotation(
                x=day['date'],
                y=i - 0.1 - j*0.05,
                text=activity,
                showarrow=False,
                xanchor='left',
                font=dict(size=10)
            )
    
    fig.update_layout(
        title="Itinerario de Viaje",
        xaxis_title="Fecha",
        yaxis=dict(showticklabels=False),
        height=500,
        showlegend=False
    )
    
    return fig

def main():
    # Header principal
    st.markdown('<h1 class="main-header">🧳 AI Travel Planner</h1>', unsafe_allow_html=True)
    st.markdown("### Optimizador de Precios con Redes Neuronales - ✈️ Encuentra las Mejores Ofertas 🏨")
    
    # Sidebar para entrada de datos
    with st.sidebar:
        st.header("📍 Planifica tu Viaje")
        
        with st.form("travel_planning"):
            st.subheader("Destino y Fechas")
            
            col1, col2 = st.columns(2)
            with col1:
                origin = st.text_input("Ciudad de Origen", "NYC", placeholder="NYC, LON, etc.")
                departure_date = st.date_input("Fecha de Ida", datetime.now() + timedelta(days=30))
            with col2:
                destination = st.text_input("Ciudad de Destino", "PAR", placeholder="PAR, ROM, etc.")
                return_date = st.date_input("Fecha de Vuelta", datetime.now() + timedelta(days=37))
            
            st.subheader("Viajeros y Presupuesto")
            col1, col2 = st.columns(2)
            with col1:
                travelers = st.number_input("Número de Viajeros", min_value=1, max_value=10, value=2)
                currency = st.selectbox("Moneda", ["USD", "EUR", "GBP", "JPY"])
            with col2:
                budget = st.number_input("Presupuesto (Opcional)", min_value=0, value=0)
                locale = st.selectbox("Idioma", ["en-US", "es-ES", "fr-FR", "de-DE"])
            
            st.subheader("Preferencias de Viaje")
            travel_style = st.selectbox(
                "Estilo de Viaje",
                ["budget", "comfort", "luxury"],
                format_func=lambda x: {
                    "budget": "💰 Económico",
                    "comfort": "😊 Confort", 
                    "luxury": "💎 Lujo"
                }[x]
            )
            
            # Datos para notificaciones
            st.subheader("Notificaciones (Opcional)")
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Email para ofertas", placeholder="tu@email.com")
            with col2:
                phone = st.text_input("Teléfono para alertas", placeholder="+1234567890")
            
            if st.form_submit_button("🚀 Buscar Mejores Ofertas con IA", type="primary", use_container_width=True):
                travel_data = {
                    "origin": origin.upper(),
                    "destination": destination.upper(),
                    "departure_date": departure_date.isoformat(),
                    "return_date": return_date.isoformat(),
                    "travelers": travelers,
                    "currency": currency,
                    "locale": locale,
                    "budget": budget if budget > 0 else None,
                    "travel_style": travel_style,
                    "email": email,
                    "phone_number": phone
                }
                
                with st.spinner("🤖 Analizando millones de opciones con modelo híbrido CNN-LSTM..."):
                    success, result = trigger_travel_search(travel_data)
                    
                    if success:
                        st.session_state.last_search = result
                        st.session_state.user_id = result.get('user_id')
                        st.success("✅ ¡Ofertas optimizadas encontradas!")
                        st.rerun()
                    else:
                        st.error(f"❌ Error: {result}")
        
        st.markdown("---")
        st.header("📊 Historial de Viajes")

        url = "https://ardtcbulqkenbrnqhlsc.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFyZHRjYnVscWtlbmJybnFobHNjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjM0OTU2MiwiZXhwIjoyMDc3OTI1NTYyfQ.dj8pZAXvojJ_nCGMu7cSKeeqM-r4KMHuvDICPH2lZO0"
        supabase = create_client(url, key)


        if st.button("Ver Mis Búsquedas"):
            response = supabase.table("travel_searches").select("*").order("search_completed_at", desc=True).execute()

            if response.data:
                df = pd.DataFrame(response.data)
                st.session_state.travel_history = df
                st.success(f"✅ Se cargaron {len(df)} búsquedas desde tu historial.")
            else:
                st.session_state.travel_history = pd.DataFrame()
                st.warning("⚠️ No se encontraron registros en tu historial.")

    # Contenido principal
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Ofertas", "📅 Itinerario", "💰 Análisis", "📈 Historial", "📊 Estadísticas"])
    
    with tab1:
        if 'last_search' in st.session_state:
            result = st.session_state.last_search
            
            # Mostrar ahorros
            savings_percentage = result.get('savings_percentage', 0)
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col2:
                if savings_percentage >= 20:
                    st.markdown(f'<div class="savings-excellent">🎉 Ahorras {savings_percentage}%</div>', unsafe_allow_html=True)
                elif savings_percentage >= 10:
                    st.markdown(f'<div class="savings-good">👍 Ahorras {savings_percentage}%</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="savings-poor">💡 Ahorras {savings_percentage}%</div>', unsafe_allow_html=True)
            
            # Métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Costo Total", f"${result.get('total_cost', 0):.0f}")
            with col2:
                st.metric("Ahorro Total", f"${result.get('total_savings', 0):.0f}")
            with col3:
                st.metric("Confianza IA", f"{result.get('confidence_score', 0) * 100:.0f}%")
            with col4:
                valid_until = datetime.fromisoformat(result.get('price_valid_until', datetime.now().isoformat()))
                st.metric("Válido hasta", valid_until.strftime('%d/%m %H:%M'))
            
            # Mejores ofertas
            st.markdown("## ✈️🏨 Mejores Ofertas Encontradas")
            
            col1, col2 = st.columns(2)
            
            with col1:
                best_flight = result.get('best_flight', {})
                st.markdown("### ✈️ Vuelo Recomendado")
                st.markdown(f'<div class="deal-card">', unsafe_allow_html=True)
                st.write(f"**Aerolínea:** {best_flight.get('airline', 'N/A')}")
                st.write(f"**Precio:** ${best_flight.get('price', 0):.0f}")
                st.write(f"**Duración:** {best_flight.get('duration', 'N/A')}")
                st.write(f"**Escalas:** {best_flight.get('stops', 0)}")
                st.write(f"**Salida:** {best_flight.get('departure_time', 'N/A')}")
                
                if best_flight.get('affiliate_link'):
                    st.markdown(f'<a href="{best_flight["affiliate_link"]}" target="_blank" class="affiliate-button">🎫 Reservar este Vuelo</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                best_hotel = result.get('best_hotel', {})
                st.markdown("### 🏨 Hotel Recomendado")
                st.markdown(f'<div class="deal-card">', unsafe_allow_html=True)
                st.write(f"**Hotel:** {best_hotel.get('hotel_name', 'N/A')}")
                st.write(f"**Precio:** ${best_hotel.get('price', 0):.0f}")
                st.write(f"**Rating:** {best_hotel.get('rating', 0)}/10")
                st.write(f"**Reviews:** {best_hotel.get('review_count', 0)}")
                st.write(f"**Distancia:** {best_hotel.get('distance', 'N/A')}")
                
                if best_hotel.get('affiliate_link'):
                    st.markdown(f'<a href="{best_hotel["affiliate_link"]}" target="_blank" class="affiliate-button">🏨 Reservar este Hotel</a>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Alertas de precio
            price_alerts = result.get('price_alerts', [])
            if price_alerts:
                st.markdown("## 🔔 Alertas de Precio")
                for alert in price_alerts:
                    if alert.get('priority') == 'high':
                        st.error(f"🚨 {alert.get('message')}")
                    else:
                        st.warning(f"⚠️ {alert.get('message')}")
            
            # Recomendaciones de IA
            st.markdown("## 🤖 Recomendaciones de IA")
            ai_recommendations = result.get('ai_recommendations', [])
            for rec in ai_recommendations:
                st.info(f"💡 {rec}")
            
            # Sección de descargas
            st.markdown("## 📥 Descargar Reportes")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("📄 Ofertas PDF", use_container_width=True):
                    success, file_content = download_report(result, 'offers', 'pdf')
                    if success:
                        st.download_button(
                            label="⬇️ Descargar Ofertas PDF",
                            data=file_content,
                            file_name=f"ofertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error: {file_content}")
            
            with col2:
                if st.button("📊 Ofertas Excel", use_container_width=True):
                    success, file_content = download_report(result, 'offers', 'excel')
                    if success:
                        st.download_button(
                            label="⬇️ Descargar Ofertas Excel",
                            data=file_content,
                            file_name=f"ofertas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error: {file_content}")
            
            with col3:
                if st.button("📋 Itinerario PDF", use_container_width=True):
                    success, file_content = download_report(result, 'itinerary', 'pdf')
                    if success:
                        st.download_button(
                            label="⬇️ Descargar Itinerario",
                            data=file_content,
                            file_name=f"itinerario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error: {file_content}")
            
            with col4:
                if st.button("💹 Análisis PDF", use_container_width=True):
                    success, file_content = download_report(result, 'analysis', 'pdf')
                    if success:
                        st.download_button(
                            label="⬇️ Descargar Análisis",
                            data=file_content,
                            file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error: {file_content}")
                
        else:
            st.info("👈 Completa los datos de tu viaje en el panel lateral y encuentra las mejores ofertas")
    
    with tab2:
        if 'last_search' in st.session_state:
            result = st.session_state.last_search
            itinerary = result.get('itinerary', {})
            
            st.markdown("## 📅 Itinerario Detallado de Viaje")
            
            # Resumen del viaje
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🌍 Destino", result.get('destination', 'N/A'))
            with col2:
                st.metric("📍 Duración", f"{result.get('trip_duration', 0)} días")
            with col3:
                st.metric("👥 Viajeros", result.get('travelers', 1))
            with col4:
                st.metric("💰 Presupuesto", f"${result.get('budget', 0):.0f}")
            
            st.markdown("---")
            
            # Línea de tiempo del itinerario
            timeline_chart = create_itinerary_timeline(itinerary)
            if timeline_chart:
                st.plotly_chart(timeline_chart, use_container_width=True)
            
            # Desglose de costos
            st.markdown("## 💰 Desglose de Costos por Día")
            cost_chart = create_cost_breakdown_chart(itinerary)
            if cost_chart:
                st.plotly_chart(cost_chart, use_container_width=True)
            
            # Detalles día por día mejorado
            st.markdown("## 📋 Plan Detallado Día por Día")
            day_by_day = itinerary.get('day_by_day', [])
            
            if day_by_day:
                for day in day_by_day:
                    day_num = day.get('day', 'N/A')
                    day_date = day.get('date', 'N/A')
                    
                    with st.expander(f"📅 Día {day_num} - {day_date}", expanded=(day_num == 1)):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            # Información del día
                            st.subheader(f"Día {day_num}: {day.get('theme', 'Exploración')}")
                            
                            # Descripción del día
                            if day.get('description'):
                                st.info(f"📝 {day.get('description')}")
                            
                            # Actividades por horario
                            st.markdown("### ⏰ Itinerario del Día")
                            activities = day.get('activities', [])
                            
                            if activities:
                                for i, activity in enumerate(activities, 1):
                                    if isinstance(activity, dict):
                                        time = activity.get('time', '09:00')
                                        name = activity.get('name', activity.get('activity', 'Actividad'))
                                        duration = activity.get('duration', '2h')
                                        cost = activity.get('cost', 0)
                                        
                                        st.write(f"**{time}** - {name}")
                                        st.write(f"   ⏱️ Duración: {duration} | 💰 Costo: ${cost:.0f}")
                                    else:
                                        st.write(f"**{i}.** {activity}")
                            else:
                                st.write("No hay actividades programadas para este día")
                            
                            # Recomendaciones del día
                            if day.get('recommendations'):
                                st.markdown("### 💡 Recomendaciones")
                                for rec in day.get('recommendations', []):
                                    st.write(f"• {rec}")
                            
                            # Comidas sugeridas
                            if day.get('meals'):
                                st.markdown("### 🍽️ Comidas Sugeridas")
                                meals = day.get('meals', {})
                                if meals.get('breakfast'):
                                    st.write(f"**Desayuno:** {meals.get('breakfast')}")
                                if meals.get('lunch'):
                                    st.write(f"**Almuerzo:** {meals.get('lunch')}")
                                if meals.get('dinner'):
                                    st.write(f"**Cena:** {meals.get('dinner')}")
                        
                        with col2:
                            # Resumen del día
                            st.markdown("### 📊 Resumen")
                            total_cost = sum([
                                a.get('cost', 0) if isinstance(a, dict) else 0 
                                for a in activities
                            ])
                            st.metric("Costo Estimado", f"${total_cost:.0f}")
                            
                            if day.get('difficulty'):
                                difficulty = day.get('difficulty', 'Moderado')
                                st.metric("Nivel de Actividad", difficulty)
                            
                            if day.get('weather'):
                                st.metric("Clima Esperado", day.get('weather', 'N/A'))
            else:
                st.info("📝 Crea un itinerario realizando una búsqueda de viaje")
            
            # Consejos generales
            st.markdown("## 🎒 Consejos para tu Viaje")
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### ✈️ Antes de Viajar
                - Verificar documentos de viaje
                - Confirmar reservas de vuelos y hoteles
                - Comprar seguro de viaje
                - Notificar al banco sobre viajes
                - Descargar mapas offline
                """)
            
            with col2:
                st.markdown("""
                ### 🏨 Durante el Viaje
                - Mantener copia de documentos
                - Usar transporte seguro
                - Respetar horarios locales
                - Probar comida local
                - Tomar fotos y disfrutar
                """)
    
    with tab3:
        if 'last_search' in st.session_state:
            result = st.session_state.last_search
            
            st.markdown("## 📊 Análisis de Precios")
            
            # Gráfico de comparación
            comparison_chart = create_price_comparison_chart(result)
            if comparison_chart:
                st.plotly_chart(comparison_chart, use_container_width=True)
            
            # Alternativas
            st.markdown("## 🔄 Otras Opciones")
            alternatives = result.get('alternative_options', [])
            
            for alt in alternatives:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{alt.get('description', 'Alternativa')}**")
                with col2:
                    st.write(f"${alt.get('price', 0):.0f}")
                with col3:
                    savings = alt.get('savings', 0)
                    if savings > 0:
                        st.write(f"💰 Ahorro: ${savings:.0f}")
            
            # Métricas detalladas
            st.markdown("## 📈 Métricas Detalladas")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Precio Mercado", f"${result.get('market_average', 0):.0f}")
            with col2:
                st.metric("Tu Precio", f"${result.get('total_cost', 0):.0f}")
            with col3:
                st.metric("Duración Viaje", f"{result.get('trip_duration', 0)} días")
            with col4:
                st.metric("Temporada", result.get('season', 'N/A').title())
    
    with tab4:
        st.markdown("## 📈 Tu Historial de Viajes")
     
        if 'travel_history' in st.session_state and not st.session_state.travel_history.empty:
            df = st.session_state.travel_history
            
            # 🔧 Convertir columnas numéricas que pueden venir como texto
            numeric_cols = ['total_savings', 'savings_percentage', 'confidence_score', 'total_cost']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # --- Aquí siguen tus métricas ---

            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_searches = len(df)
                st.metric("Total Búsquedas", total_searches)
            with col2:
                total_savings = df['total_savings'].sum()
                st.metric("Ahorro Total", f"${total_savings:.0f}")
            with col3:
                avg_savings = df['savings_percentage'].mean()
                st.metric("Ahorro Promedio", f"{avg_savings:.1f}%")
            with col4:
                favorite_dest = df['destination'].mode().iloc[0] if not df.empty else 'N/A'
                st.metric("Destino Favorito", favorite_dest)
            
            # Gráfico de ahorros a lo largo del tiempo
            if not df.empty:
                df['search_completed_at'] = pd.to_datetime(df['search_completed_at'])
                fig = px.line(df, x='search_completed_at', y='savings_percentage',
                            title='Evolución de tus Ahorros en Viajes',
                            markers=True)
                st.plotly_chart(fig, use_container_width=True)
            
            # Historial detallado
            st.markdown("### 📋 Historial Detallado")
            display_df = df[['search_completed_at', 'destination', 'total_cost', 'savings_percentage', 'confidence_score']].copy()
            display_df['search_completed_at'] = pd.to_datetime(display_df['search_completed_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(display_df, use_container_width=True)
            
        else:
            st.info("Ejecuta 'Ver Mis Búsquedas' para cargar tu historial de viajes")
    
    with tab5:
        st.markdown("## 📊 Estadísticas del Sistema")
        
        # Obtener estadísticas
        stats = get_statistics()
        
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Búsquedas", stats.get('total_searches', 0))
            with col2:
                st.metric("Ahorro Promedio", f"{stats.get('average_savings', 0):.1f}%")
            with col3:
                st.metric("Destino Popular", stats.get('most_popular_destination', 'N/A'))
            with col4:
                st.metric("Duración Promedio", f"{stats.get('average_trip_duration', 0)} días")
            
            st.markdown("---")
            
            # Información adicional
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 👥 Usuarios Activos")
                st.metric("Total Usuarios", stats.get('total_users', 0))
            
            with col2:
                st.markdown("### ⏰ Última Actualización")
                st.info(f"Actualizado: {stats.get('timestamp', 'N/A')}")
            
            # Gráfico de tendencias (simulado)
            st.markdown("### 📈 Tendencias de Búsquedas")
            
            # Crear datos simulados para el gráfico
            dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
            trend_data = pd.DataFrame({
                'Fecha': dates,
                'Búsquedas': np.random.randint(10, 50, 30),
                'Ahorro Promedio %': np.random.uniform(10, 30, 30)
            })
            
            fig = px.line(trend_data, x='Fecha', y='Búsquedas', 
                         title='Tendencia de Búsquedas en los Últimos 30 Días',
                         markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Distribución de destinos (simulado)
            st.markdown("### 🌍 Destinos Más Populares")
            
            destinations = ['París', 'Nueva York', 'Roma', 'Londres', 'Tokio', 'Barcelona']
            searches = np.random.randint(20, 100, 6)
            
            fig_dest = px.bar(x=destinations, y=searches,
                             labels={'x': 'Destino', 'y': 'Número de Búsquedas'},
                             title='Destinos Más Buscados')
            st.plotly_chart(fig_dest, use_container_width=True)
        else:
            st.warning("⚠️ No se pudieron cargar las estadísticas del sistema")
            st.info("Asegúrate de que el servidor esté ejecutándose en http://localhost:8002")

if __name__ == "__main__":
    main()
