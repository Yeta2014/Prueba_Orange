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

# Configurar logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OrangeHRMAutomation:
    def __init__(self):
        self.driver = self.setup_driver()

    @staticmethod
    def setup_driver():
        """Configura el navegador con ChromeDriver."""
        service = Service(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--start-maximized')
        # options.add_argument('--headless')  # Ejecutar en modo headless si es necesario
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def login(self):
        """Realiza el inicio de sesión en la plataforma."""
        logging.info("Iniciando sesión...")
        self.driver.get(APP_URL)

        # Extraer credenciales
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'orangehrm-demo-credentials'))
        )
        credenciales = self.driver.find_elements(By.TAG_NAME, 'p')
        username = credenciales[0].text.split(":")[-1].strip()
        password = credenciales[1].text.split(":")[-1].strip()

        # Rellenar campos de inicio de sesión
        self.driver.find_element(By.XPATH, '//input[@placeholder="username"]').send_keys(username)
        self.driver.find_element(By.XPATH, '//input[@placeholder="password"]').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'orangehrm-login-button').click()

        time.sleep(3)  # Esperar 3 segundos

    def navigate_to_recruitment(self):
        """Navega al módulo de Recruitment y abre el formulario 'Add Candidate'."""
        logging.info("Navegando al módulo Recruitment...")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Recruitment"]'))
        ).click()
        time.sleep(3)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()=" Add "]'))
        ).click()
        time.sleep(3)  # Esperar 3 segundos
        

    def fill_form(self):
        """Llena el formulario con los datos del candidato."""
        logging.info("Llenando el formulario de candidato...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, 'firstName')))

        # Ingresar datos básicos
        self.driver.find_element(By.NAME, 'firstName').send_keys(datos['first_name'])
        self.driver.find_element(By.NAME, 'middleName').send_keys(datos['middle_name'])
        self.driver.find_element(By.NAME, 'lastName').send_keys(datos['last_name'])

        # Seleccionar Vacancy
        # Espera a que el dropdown sea visible y haz clic en él
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div/div/div[2]/div/div/div[2]/i'))
        )

        dropdown_vacancy = self.driver.find_element(
            By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div/div/div[2]/div/div/div[2]/i'
        )
        dropdown_vacancy.click()

        # Espera a que las opciones del dropdown sean visibles
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="listbox"]//span'))
        )

        # Encuentra la opción que contenga el texto 'Payroll Administrator' y haz clic en ella
        payroll_administrator = self.driver.find_element(
            By.XPATH, "//div[@role='listbox']//span[text()='Payroll Administrator']"
        )
        payroll_administrator.click()

        # Email, contacto y archivo
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[1]/div/div[2]/input').send_keys(
            datos['email']
        )
        self.driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/div/div[2]/div/div[2]/input').send_keys(
            datos['contact_number']
        )
        self.driver.find_element(By.XPATH, '//input[@placeholder="Enter comma seperated words..."]').send_keys(
            datos['keywords']
        )
        self.driver.find_element(By.XPATH, '//input[@type="file"]').send_keys(datos['resume_path'])

        # Interactuar con el datepicker y establecer la fecha
        logging.info("Configurando el datepicker...")
        date_picker = self.driver.find_element(By.XPATH, '//input[@placeholder="dd-mm-yyyy"]')
        date_picker.click()  # Abrir el datepicker

        # Limpiar cualquier fecha existente
        clear_button = self.driver.find_element(By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/form[1]/div[5]/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div[2]')
        clear_button.click()  # Limpiar el campo

        # Ingresar la fecha
        date_picker.send_keys(datos['date_of_joining'])
        time.sleep(3)  # Esperar 3 segundos

    def submit_form(self):
        """Envía el formulario e interactúa con los botones en las páginas subsiguientes."""
        logging.info("Enviando el formulario...")
        
        # Hacer clic en el botón de envío del formulario
        self.driver.find_element(By.XPATH, '//button[@class="oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space"]').click()
        time.sleep(3)  # Esperar 3 segundos para la transición
        
        # Esperar a que el botón adicional sea clickeable y hacer clic en él
        logging.info("Esperando el botón adicional en la nueva página...")
        try:
            boton_adicional = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/form/div[2]/div[2]/button[2]'))
            )
            logging.info("Haciendo clic en el botón adicional...")
            boton_adicional.click()
            time.sleep(3)  # Esperar 3 segundos después de hacer clic
        except Exception as e:
            logging.error(f"No se pudo encontrar o hacer clic en el botón adicional: {e}")
            return  # Detener el flujo si ocurre un error
        
        # Esperar y hacer clic en el último botón
        logging.info("Esperando el último botón en la siguiente página...")
        try:
            ultimo_boton = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space"]'))
            )
            logging.info("Haciendo clic en el último botón...")
            ultimo_boton.click()
            time.sleep(3)  # Esperar 3 segundos después de hacer clic
        except Exception as e:
            logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")
            
        # Esperar y hacer clic en el último botón
        logging.info("Esperando el último botón en la siguiente página...")
        try:
            ultimo_boton = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@class="oxd-button oxd-button--medium oxd-button--success"]'))
            )
            logging.info("Haciendo clic en el último botón...")
            ultimo_boton.click()
            time.sleep(3)  # Esperar 3 segundos después de hacer clic

            # Esperar a que el campo de entrada esté disponible y llenar el campo
            input_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[2]/div/div[1]/div/div[2]/input'))
            )
            input_field.send_keys(datos['title'])
            
            # Esperar a que el campo de entrada esté disponible
            logging.info("Seleccionando el campo de entrada para la vacante...")
            vacancy_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//input[@placeholder="Type for hints..."]'
                ))
            )

            vacancy_input.click()  # Hacer clic en el campo de entrada
            vacancy_input.send_keys(datos['interviewer'])  # Ingresar el texto deseado

            # Esperar un poco para que las opciones aparezcan
            time.sleep(2)  # Ajustar el tiempo si es necesario

            # Esperar a que el primer resultado del desplegable esté disponible y hacer clic
            logging.info("Esperando el primer resultado en el desplegable...")
            first_result = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//div[@class="oxd-autocomplete-wrapper"]//span[1]'
                ))
            )

            first_result.click()  # Hacer clic en el primer resultado
            logging.info("Vacante seleccionada correctamente.")
            
            logging.info("Configurando el datepicker...")
            date_picker = self.driver.find_element(By.XPATH, '//input[@placeholder="dd-mm-yyyy"]')
            date_picker.click()  # Abrir el datepicker

            # Ingresar la fecha
            date_picker.send_keys(datos['date_of_joining'])
            date_picker = self.driver.find_element(By.XPATH, '//input[@placeholder="hh:mm"]')
            date_picker.click() 
            
            time.sleep(3)
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@class="oxd-button oxd-button--medium oxd-button--secondary orangehrm-left-space"]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
            
            
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/form/div[2]/div[2]/button[3]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
                
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos

            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/form/div[2]/div[2]/button[3]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
            
            
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos}
                
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
                
                
                
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div[1]/form/div[2]/div[2]/button[3]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
                
                            
            logging.info("Esperando el último botón en la siguiente página...")
            try:
                ultimo_boton = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[1]/div[2]/div[2]/div/div/form/div[3]/button[2]'))
                )
                logging.info("Haciendo clic en el último botón...")
                ultimo_boton.click()
                time.sleep(3)  # Esperar 3 segundos después de hacer clic
            except Exception as e:
                logging.error(f"No se pudo encontrar o hacer clic en el último botón: {e}")# Esperar 3 segundos después de enviar los datos
                
        except Exception as e:
            logging.error(f"No se pudo encontrar o interactuar con el campo de entrada: {e}")
                
        
        

# Ejecutar la automatización
if __name__ == "__main__":
    automation = OrangeHRMAutomation()
    automation.login()
    automation.navigate_to_recruitment()
    automation.fill_form()
    automation.submit_form()
    automation.driver.quit()

