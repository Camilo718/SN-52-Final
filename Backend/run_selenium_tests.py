#!/usr/bin/env python3
"""
SCRIPT FÁCIL: Ejecutar pruebas Selenium
"""
# Opciones del script:
# 1 - Pruebas visibles (verás Firefox abrirse)
# 2 - Pruebas automáticas (sin interfaz)
# 3 - Generar reporte HTML

import subprocess
import sys
import os

def main():
    print("\n\nSELENIUM TEST RUNNER")
    print("=" * 50)
    
    # Crear carpetas necesarias
    os.makedirs("tests/selenium/screenshots", exist_ok=True)
    os.makedirs("tests/reports", exist_ok=True)
    
    print("1️  Pruebas VISIBLES BACKEND (Verás Firefox abrirse)")
    print("2⃣  Pruebas AUTOMÁTICAS BACKEND (Sin interfaz)")
    print("3️  Generar reporte HTML")
    print("4️  Pruebas FRONTEND (Interfaz Real - Requiere 'npm run dev')")
    
    choice = input("\nElige opción (1, 2, 3, 4): ").strip()
    
    if choice == "1":
        run_visible_tests()
    elif choice == "2":
        run_auto_tests()
    elif choice == "3":
        run_with_report()
    elif choice == "4":
        run_frontend_tests()
    else:
        print("\nOpción no válida")

def run_visible_tests():
    """Ejecuta pruebas VISIBLES"""
    print("\n\nEJECUTANDO PRUEBAS VISIBLES...")
    print("\nVerás Firefox abrirse y realizar las pruebas")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/test_firefox_visible.py",
        "-v", "-s"
    ]
    run_command(cmd, "Pruebas visibles")

def run_auto_tests():
    """Ejecuta pruebas AUTOMÁTICAS"""
    print("\n\nEJECUTANDO PRUEBAS AUTOMÁTICAS...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/test_firefox_visible.py",
        "-v",
        "--headless"  # Ejecutar sin interfaz
    ]
    run_command(cmd, "Pruebas automáticas")

def run_with_report():
    """Ejecuta con reporte HTML"""
    print("\n\nGENERANDO REPORTE HTML...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/test_firefox_visible.py",
        "-v",
        "--html=tests/reports/selenium_report.html",
        "--self-contained-html"
    ]
    run_command(cmd, "Reporte HTML")

def run_frontend_tests():
    """Ejecuta pruebas FRONTEND"""
    print("\n\nEJECUTANDO PRUEBAS DE INTERFAZ FRONTEND...")
    print("Asegúrate de que el frontend esté corriendo (npm run dev)")
    print("en http://localhost:5173")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/selenium/test_frontend_visible.py",
        "-v", "-s"
    ]
    run_command(cmd, "Pruebas Frontend")

def run_command(cmd, test_type):
    """Ejecuta comando y muestra resultados"""
    print(f"\n\nEjecutando: {test_type}")
    print("\nPor favor espera...")
    
    try:
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"\n✅ {test_type} COMPLETADAS EXITOSAMENTE!")
        else:
            print(f"\n❌ {test_type} tuvieron problemas")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
