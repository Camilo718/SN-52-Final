# Selenium Tests Setup

## 4.1 Preparación

### 1. Navegar al proyecto
Asegúrate de estar en la carpeta backend:
```bash
cd Backend
```

### 2. Activar entorno virtual
```bash
venv\Scripts\activate
```

### 3. Asegurar que tu backend esté ejecutándose
```bash
uvicorn main:app --reload
```

## 4.2 Ejecutar pruebas (3 opciones)

### OPCIÓN 1: Pruebas VISIBLES (Recomendado para empezar)
Ejecuta el script interactivo y selecciona la opción 1:
```bash
python run_selenium_tests.py
```

### OPCIÓN 2: Comando directo
Ejecuta pytest directamente para ver el navegador:
```bash
python -m pytest tests/selenium/test_firefox_visible.py -v -s
```

### OPCIÓN 3: Con reporte HTML
Genera un reporte detallado:
```bash
python -m pytest tests/selenium/test_firefox_visible.py -v --html=tests/reports/selenium_report.html
```

## Requisitos previos
No olvides instalar las dependencias si no lo has hecho:
```bash
pip install selenium pytest pytest-html webdriver-manager
```
