#!/usr/bin/env python3
"""
Script para verificar que la instalación está completa y funciona correctamente
"""

import sys
import time

print("=" * 60)
print("🧳 VERIFICACIÓN DE INSTALACIÓN - TRAVEL AI PLANNER v2.0")
print("=" * 60)

# Verificar módulos
print("\n📦 Verificando módulos instalados...")

modules_to_check = [
    ('fastapi', 'FastAPI'),
    ('streamlit', 'Streamlit'),
    ('pandas', 'Pandas'),
    ('plotly', 'Plotly'),
    ('requests', 'Requests'),
    ('uvicorn', 'Uvicorn'),
    ('pydantic', 'Pydantic'),
    ('reportlab', 'ReportLab'),
    ('openpyxl', 'OpenPyXL'),
    ('supabase', 'Supabase'),
]

all_ok = True
for module_name, display_name in modules_to_check:
    try:
        __import__(module_name)
        print(f"  ✅ {display_name:20} - Instalado")
    except ImportError:
        print(f"  ❌ {display_name:20} - NO INSTALADO")
        all_ok = False

print("\n" + "=" * 60)

if all_ok:
    print("✅ TODAS LAS DEPENDENCIAS ESTÁN INSTALADAS")
    print("\n🚀 Próximos pasos:")
    print("  1. Terminal 1: python travel_ai_server.py")
    print("  2. Terminal 2: streamlit run travel_app.py")
    print("  3. Acceder a: http://localhost:8501")
    print("\n" + "=" * 60)
    sys.exit(0)
else:
    print("❌ FALTAN DEPENDENCIAS")
    print("\nEjecuta:")
    print("  pip install -r requirements.txt")
    print("\n" + "=" * 60)
    sys.exit(1)
