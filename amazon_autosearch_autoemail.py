import random
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText

# Define función para generar intervalos aleatorios de tiempo
def random_interval(min_seconds=3, max_seconds=18):
    return random.randint(min_seconds, max_seconds)

# Establecer las credenciales del usuario de Amazon
username = "usuario de Amazon"
password = "contraseña de Amazon"

# Configuración del servidor SMTP (para el correo electronico)
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'my_email@servmail.com'
smtp_password = 'my_password'

# Definir opciones del navegador
chrome_options = Options()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Configurar el driver de Selenium para utilizar Chrome
driver = webdriver.Chrome(options=chrome_options)

# Navegar a la página de inicio de Amazon España y esperar que cargue
driver.get("https://www.amazon.es/")
time.sleep(random_interval())

# Verificar si hay un aviso de cookies y hacer clic en el botón Aceptar si está presente - Actualizar la página hasta que aparezca el aviso de cookies y se pueda aceptar
cookie_present = False
while not cookie_present:
    try:
        cookie_button = driver.find_element(By.ID, "sp-cc-accept")
        cookie_button.click()
        cookie_present = True
        time.sleep(random_interval())
    except:
        # Si no hay un aviso de cookies, actualizar la página
        driver.refresh()
        time.sleep(random_interval())

# Verificar si hay una sesión iniciada y cerrarla
try:
    driver.find_element(By.ID, "nav-link-accountList-nav-line-1").click()
    driver.find_element(By.ID, "nav-item-signout").click()
except:
    pass

# Iniciar sesión con el usuario y contraseña especificado
driver.find_element(By.ID, "ap_email").send_keys(username)
driver.find_element(By.ID, "continue").click()
driver.find_element(By.ID, "ap_password").send_keys(password)
driver.find_element(By.ID, "signInSubmit").click()

# Esperar a que la página cargue completamente
time.sleep(random_interval())

# Localizar el campo de búsqueda y escribir el término "lo que se desee buscar"
search_box = driver.find_element("name", "field-keywords")
search_box.clear()
search_box.send_keys("camisas primavera mujer")

# Localizar el botón de búsqueda y hacer clic en él
search_button = driver.find_element("xpath", "//*[@id='nav-search-submit-button']")
search_button.click()

# Esperar a que carguen los resultados de búsqueda
time.sleep(random_interval())

# Encontrar todos los resultados de la búsqueda
results = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

# Imprimir en la consola la información de los 3 primeros resultados
for i in range(3):
    print("\nResultado número {}:\n".format(i+1))
    print(results[i].text)

# Enviar un correo electrónico por cada resultado obtenido (contenido y link)
for i in range(3):
    # Obtener el link de cada producto
    link = results[i].find_element(By.TAG_NAME, 'h2').find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
    # Crea el objeto del mensaje del correo
    msg = MIMEText(f'Se ha realizado una búsqueda en Amazon España del siguiente producto:\n\n{results[i].text}\n\n\nPara más información has click en el siguiente link:\n\n{link}\n\nEste mensaje fue generado automáticamente.')
    msg['From'] = 'my_email@servmail.com'
    msg['To'] = 'recipient_email@servmail.com'
    msg['Subject'] = 'Producto buscado en Amazon España'
    # Envía el mensaje
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, [msg['To']], msg.as_string())
    print("\nResultado número {} enviado por correo exitosamente".format(i+1))

# Cerrar el navegador
driver.quit()
