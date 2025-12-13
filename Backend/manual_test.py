import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def pause():
    input("\nPresiona ENTER para continuar...")

print("--- INICIANDO TEST MANUAL INTERACTIVO ---")
print("1. Configurando carpetas...")
os.makedirs("tests/selenium/screenshots", exist_ok=True)

print("2. Abriendo Firefox... Por favor espera.")
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(service=service)
driver.maximize_window()
base_url = "http://localhost:8000"

print("\n✅ Navegador abierto.")
pause()

# 1. Home
print("\n👉 Navegando a HOME...")
driver.get(f"{base_url}/")
print(f"   URL: {driver.current_url}")
driver.save_screenshot("tests/selenium/screenshots/manual_1_home.png")
print("   📸 Screenshot guardado.")
pause()

# 2. Docs
print("\n👉 Navegando a DOCS...")
driver.get(f"{base_url}/docs")
driver.save_screenshot("tests/selenium/screenshots/manual_2_docs.png")
print("   📸 Screenshot guardado.")
pause()

# 3. Static
print("\n👉 Navegando a ARCHIVOS ESTÁTICOS...")
driver.get(f"{base_url}/static/")
driver.save_screenshot("tests/selenium/screenshots/manual_3_static.png")
print("   📸 Screenshot guardado.")
print("\n✅ Pruebas finalizadas. El navegador se cerrará.")
pause()

driver.quit()
print("👋 Navegador cerrado.")
