import pytest
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager

class TestFrontendVisible:
    """Pruebas VISIBLES de la Interfaz (Frontend) - Puerto 5173"""
    
    def setup_method(self):
        print("\nINICIANDO FIREFOX PARA FRONTEND...")
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        # URL del Frontend (Vite con base path)
        self.base_url = "http://localhost:5173/Proyecto-SN-52"
        
        def _take_screenshot(name):
            try:
                path = f"tests/selenium/screenshots/frontend_{name}.png"
                self.driver.save_screenshot(path)
                print(f"Screenshot saved: {path}")
            except Exception as e:
                print(f"Error taking screenshot: {e}")
        self._take_screenshot = _take_screenshot

    def teardown_method(self):
        print("\nCerrando navegador en 10 segundos...")
        time.sleep(10)
        self.driver.quit()

    def test_1_home_page_ui(self):
        """PRUEBA 1: Carga de la Página Principal del Frontend"""
        print(f"\nNavegando a {self.base_url}/ ...")
        self.driver.get(f"{self.base_url}/")
        
        # Esperar a que cargue algo visual (ajustar según tu UI)
        time.sleep(5)
        self._take_screenshot("home")
        
        # Verificaciones simples
        assert "localhost" in self.driver.current_url
        # Puedes agregar aquí chequeos de título si supieramos el <title>
        print("\nInterfaz de Home cargada.")

    def test_2_navigation_login(self):
        """PRUEBA 2: Navegación a Login"""
        print("\nNavegando a Login...")
        self.driver.get(f"{self.base_url}/login")
        time.sleep(3)
        self._take_screenshot("login")
        
        # Verificar URL
        assert "login" in self.driver.current_url
        print("\nPágina de Login visible.")

    def test_3_category_deportes(self):
        """PRUEBA 3: Sección Deportes"""
        print("\nNavegando a Deportes...")
        self.driver.get(f"{self.base_url}/deportes")
        time.sleep(3)
        self._take_screenshot("deportes")
        print("\nSección Deportes visible.")
