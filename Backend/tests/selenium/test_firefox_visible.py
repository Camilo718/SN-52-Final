import pytest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class TestBackendVisible:
    """Pruebas VISIBLES con Firefox - Verás el navegador abrirse"""
    
    def setup_method(self):
        # Initialize Firefox driver (visible mode)
        print("\nINICIANDO FIREFOX - Verás la ventana abrirse...")
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.base_url = "http://localhost:8000"
        # Helper for screenshots
        def _take_screenshot(name):
            path = f"tests/selenium/screenshots/{name}.png"
            self.driver.save_screenshot(path)
            print(f"Screenshot saved: {path}")
        self._take_screenshot = _take_screenshot
        """Configuración antes de cada prueba"""
        print("\nINICIANDO FIREFOX - Verás la ventana abrirse...")
        # Configurar Firefox VISIBLE (sin headless)
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        # Maximizar ventana
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        # URL de tu aplicación
        self.base_url = "http://localhost:8000"

    def teardown_method(self):
        """Limpieza después de cada prueba"""
        print("\nCerrando navegador en 10 segundos...")
        time.sleep(90)  # Pausa extendida para ver el resultado
        self.driver.quit()

    def test_1_home_page(self):
        """PRUEBA 1: Página principal"""
        print("\nNavegando a la página principal...")
        self.driver.get(f"{self.base_url}/")
        self._take_screenshot("home_page")
        time.sleep(5)
        # Verificar que cargó
        assert self.driver.current_url == f"{self.base_url}/"
        print("\nPágina principal cargada correctamente!")

    def test_2_api_documentation(self):
        """PRUEBA 2: Documentación de la API"""
        print("\nNavegando a Swagger UI...")
        self.driver.get(f"{self.base_url}/docs")
        self._take_screenshot("swagger_ui")
        time.sleep(5)
        # Tomar screenshot
        self.driver.save_screenshot("tests/selenium/screenshots/swagger_ui.png")
        print("\nDocumentación de API cargada - Mira Firefox!")

    def test_3_navigation_flow(self):
        """PRUEBA 3: Flujo de navegación"""
        print("\nProbando navegación entre páginas...")
        # 1. Ir a home
        self.driver.get(f"{self.base_url}/")
        self._take_screenshot("nav_home")
        time.sleep(4)
        print("\nHome page")
        # 2. Ir a docs
        self.driver.get(f"{self.base_url}/docs")
        self._take_screenshot("nav_docs")
        time.sleep(4)
        print("\nSwagger UI")
        # 3. Ir a redoc
        self.driver.get(f"{self.base_url}/redoc")
        self._take_screenshot("nav_redoc")
        time.sleep(4)
        print("\nHome page")
        # 2. Ir a docs
        self.driver.get(f"{self.base_url}/docs")
        time.sleep(2)
        print("\nSwagger UI")
        # 3. Ir a redoc
        self.driver.get(f"{self.base_url}/redoc")
        time.sleep(2)
        print("\nReDoc")
        print("\nNavegación completada!")

    def test_4_static_files(self):
        """PRUEBA 4: Archivos estáticos"""
        print("\nVerificando archivos estáticos...")
        self.driver.get(f"{self.base_url}/static/")
        self._take_screenshot("static_files")
        time.sleep(5)
        # Verificar que no hay error 500
        page_source = self.driver.page_source.lower()
        assert "internal server error" not in page_source
        print("\nArchivos estáticos accesibles!")
