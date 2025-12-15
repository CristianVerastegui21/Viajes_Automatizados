#!/usr/bin/env python3
"""
Script de prueba para la funcionalidad de reportes
"""

import requests
import json
from datetime import datetime, timedelta

# Configuración
SERVER_URL = "http://localhost:8002"

# Datos de prueba
test_travel_data = {
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
        "Experiencia cultural única",
        "Tour de compras en mercados locales"
    ]
}

def test_statistics():
    """Probar endpoint de estadísticas"""
    print("\n📊 Probando endpoint de estadísticas...")
    try:
        response = requests.get(f"{SERVER_URL}/statistics", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Estadísticas obtenidas:")
            print(json.dumps(stats, indent=2))
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_download_report(report_type, format_type):
    """Probar descarga de reportes"""
    print(f"\n📥 Probando descarga de reporte: {report_type} ({format_type})...")
    try:
        payload = {
            "travel_data": test_travel_data,
            "report_type": report_type,
            "format": format_type
        }
        
        response = requests.post(
            f"{SERVER_URL}/download-report",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            # Guardar archivo
            filename = f"test_{report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ Reporte descargado: {filename}")
            print(f"   Tamaño: {len(response.content)} bytes")
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

def test_all_reports():
    """Probar todos los tipos de reportes"""
    print("=" * 60)
    print("🧳 PRUEBAS DE REPORTES - TRAVEL AI PLANNER")
    print("=" * 60)
    
    # Probar estadísticas
    stats_ok = test_statistics()
    
    # Probar reportes PDF
    print("\n" + "=" * 60)
    print("📄 PRUEBAS DE REPORTES PDF")
    print("=" * 60)
    
    pdf_tests = [
        ("offers", "pdf"),
        ("itinerary", "pdf"),
        ("analysis", "pdf"),
        ("full", "pdf")
    ]
    
    pdf_results = []
    for report_type, format_type in pdf_tests:
        result = test_download_report(report_type, format_type)
        pdf_results.append((report_type, result))
    
    # Probar reportes Excel
    print("\n" + "=" * 60)
    print("📊 PRUEBAS DE REPORTES EXCEL")
    print("=" * 60)
    
    excel_tests = [
        ("offers", "excel"),
        ("analysis", "excel"),
        ("itinerary", "excel")
    ]
    
    excel_results = []
    for report_type, format_type in excel_tests:
        result = test_download_report(report_type, format_type)
        excel_results.append((report_type, result))
    
    # Resumen
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    print("\n✅ Estadísticas:", "PASÓ" if stats_ok else "FALLÓ")
    
    print("\n📄 Reportes PDF:")
    for report_type, result in pdf_results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {report_type}: {status}")
    
    print("\n📊 Reportes Excel:")
    for report_type, result in excel_results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"   {report_type}: {status}")
    
    # Contar resultados
    total_tests = 1 + len(pdf_results) + len(excel_results)
    passed_tests = sum([1 for _, r in pdf_results if r]) + sum([1 for _, r in excel_results if r]) + (1 if stats_ok else 0)
    
    print("\n" + "=" * 60)
    print(f"📊 TOTAL: {passed_tests}/{total_tests} pruebas pasadas")
    print("=" * 60)
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} prueba(s) fallaron")

if __name__ == "__main__":
    print("\n⚠️  Asegúrate de que el servidor FastAPI está ejecutándose:")
    print("   python travel_ai_server.py")
    print("\nPresiona Enter para continuar...")
    input()
    
    test_all_reports()
