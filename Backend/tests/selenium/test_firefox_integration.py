import pytest
import os
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

# Fixture para el navegador (Headless / Automático)
@pytest.fixture
def driver():
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless") # Ejecución en segundo plano
    driver = webdriver.Firefox(service=service, options=options)
    yield driver
    driver.quit()

def test_google_integration(driver):
    """
    Prueba de integración automática.
    """
    try:
        driver.get("http://localhost:8000")
        assert driver.title != ""
        
        # Tomar captura de pantalla
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ruta para screenshots: backend/tests/selenium/screenshots
        base_dir = os.path.dirname(os.path.abspath(__file__))
        screenshots_dir = os.path.join(base_dir, "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        
        screenshot_path = os.path.join(screenshots_dir, f"integration_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot guardado en: {screenshot_path}")
        
    except Exception as e:
        pytest.fail(f"Fallo en el test de integración: {e}")
