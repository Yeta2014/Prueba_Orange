# Selenium Automation Script

Este proyecto utiliza Selenium para automatizar tareas de scraping e interacción con una página web. Está configurado para trabajar con Google Chrome y emplea el controlador gestionado por `webdriver_manager` para garantizar compatibilidad.

## Requisitos

Antes de ejecutar el script, asegúrate de tener instalados los siguientes componentes:

### Dependencias de Python

- Python 3.7 o superior
- Las bibliotecas listadas en `requirements.txt`:
  ```
  selenium
  webdriver-manager
  ```

Puedes instalarlas ejecutando:
```bash
pip install -r requirements.txt
```

### Otros Requisitos

- Google Chrome (ultima versión estable)
- Archivo `datos.py` que debe contener las siguientes variables:
  - `datos`: Información necesaria para la ejecución del script.
  - `APP_URL`: URL de la aplicación web que deseas automatizar.

## Configuración

El script utiliza las siguientes configuraciones por defecto:

- **WebDriver Manager**: Maneja automáticamente la descarga y actualización del controlador de Chrome.
- **Opciones de Chrome**: Ejecuta el navegador en modo personalizado según las configuraciones establecidas en el script.

## Estructura del Proyecto

```plaintext
.
├── datos.py               # Contiene datos necesarios como URL o información de entrada.
├── prueba.py              # Script principal de automatización.
├── README.md              # Documentación del proyecto.
└── requirements.txt       # Lista de dependencias.
```

## Uso

1. Asegúrate de que los archivos necesarios estén configurados, especialmente `datos.py`.
2. Ejecuta el script utilizando el siguiente comando:
   ```bash
   python prueba.py
   ```

El script realiza lo siguiente:

- Inicia el navegador Chrome.
- Navega a la URL especificada en `APP_URL`.
- Interactúa con los elementos de la página web según las reglas definidas.

## Detalles del Código

### Módulos Principales

- **time**: Controla los tiempos de espera fijos.
- **logging**: Genera logs para depuración y monitoreo.
- **selenium.webdriver**: Interactúa con el navegador.
- **webdriver_manager**: Gestiona automáticamente el controlador del navegador.

### Estructura de Importaciones

```python
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datos import datos, APP_URL
```

### Lógica del Script

- **Inicialización del Navegador**: El navegador se configura con opciones predeterminadas:
  ```python
  chrome_options = Options()
  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  ```

- **Espera Explícita**: Garantiza que los elementos necesarios estén disponibles antes de interactuar:
  ```python
  element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "element_id"))
  )
  ```

- **Navegación a la URL**:
  ```python
  driver.get(APP_URL)
  ```

- **Tareas Automatizadas**: Los pasos específicos dependen de la estructura de la página y los datos de `datos.py`.

## Notas Adicionales

- **Seguridad**: Si `datos.py` contiene información confidencial, no lo compartas ni subas a repositorios públicos.
- **Depuración**: Utiliza `logging` para rastrear posibles errores.

## Contribución
Si deseas contribuir a este proyecto, abre un `pull request` o crea un `issue` en el repositorio correspondiente.

