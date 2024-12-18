from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configuración del navegador
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument('--start-maximized')  # Para maximizar la ventana del navegador
#options.add_argument('--headless')  # Ejecutar Chrome en modo headless
options.add_argument('--no-sandbox')  # Opciones adicionales para mejorar la estabilidad
driver = webdriver.Chrome(service=service, options=options)

# Datos a ingresar
datos = {
    "first_name": "John",
    "middle_name": "Michael",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "contact_number": "1234567890",
    "keywords": "Python, Selenium, QA",
    "resume_path": os.path.abspath("resume.docx"),  # Ruta del archivo local
    "date_of_joining": "2024-16-12"
}

try:
    # URL de inicio de sesión
    url = 'https://opensource-demo.orangehrmlive.com'
    driver.get(url)

    # Iniciar sesión
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'orangehrm-demo-credentials'))
    )
    credenciales = driver.find_elements(By.TAG_NAME, 'p')
    username = credenciales[0].text.split(":")[-1].strip()
    password = credenciales[1].text.split(":")[-1].strip()

    driver.find_element(By.XPATH, '//input[@placeholder="Username"]').send_keys(username)
    driver.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'orangehrm-login-button').click()
    
    # Navegación a Recruitment > Add
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Recruitment"]'))).click()
    time.sleep(3)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()=" Add "]'))).click()

    # Llenar el formulario "Add Candidate"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'firstName')))

    driver.find_element(By.NAME, 'firstName').send_keys(datos['first_name'])
    driver.find_element(By.NAME, 'middleName').send_keys(datos['middle_name'])
    driver.find_element(By.NAME, 'lastName').send_keys(datos['last_name'])

    # Hacer clic en el dropdown de Vacancy
    dropdown_vacancy = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div/div/div[2]/div/div/div[2]/i')
    dropdown_vacancy.click()

    # Esperar a que las opciones estén visibles
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@role="listbox"]//span'))
    )

    # Seleccionar la primera opción de la lista
    primera_opcion = driver.find_element(By.XPATH, '//div[@role="listbox"]//span[1]')
    primera_opcion.click()
    
    # Email y contacto
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[1]/div/div[2]/input').send_keys(datos['email'])
    driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[2]/div/div[2]/input').send_keys(datos['contact_number'])

    # Subir el archivo de Resume
    driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(datos['resume_path'])

    # Keywords
    driver.find_element(By.XPATH, '//input[@placeholder="Enter comma seperated words..."]').send_keys(datos['keywords'])
    time.sleep(5)
    
    # Interactuar con el datepicker y abrirlo
    date_picker = driver.find_element(By.XPATH, '//input[@placeholder="yyyy-dd-mm"]')
    date_picker.click()  # Hacer clic en el campo para abrir el datepicker

    # Hacer clic en el botón para limpiar el campo de fecha
    clear_button = driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[5]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div[2]')
    clear_button.click()  # Hacer clic en el botón de limpieza

    # Ahora ingresar la fecha proporcionada (date_of_joining)
    date_picker.send_keys(datos['date_of_joining'])  # Ingresar la fecha '2024-16-12'


    # Submit (opcional)
    submit_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    submit_button.click()

    print("Formulario completado con éxito.")

except Exception as e:
    print(f"Error: {e}")

finally:
    time.sleep(5)
    driver.quit()
