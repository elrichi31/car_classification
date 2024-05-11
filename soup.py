import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Creating a directory to save images
def create_directory(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def download_image(image_url, folder_path, file_name):
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, f"creta{file_name}.jpg"), 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {file_name}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

# Initialize web driver
service = Service()  # Add path to your chromedriver if needed
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)  # Timeout of 10 seconds

def fetch_images(search_url, folder_name, max_images=50):
    driver.get(search_url)
    create_directory(folder_name)

    # Desplazarse para cargar imágenes
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)  # Pausa para permitir que las imágenes se carguen

    try:
        # Utiliza el nuevo selector aquí. Cambia según lo que decidas usar.
        images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.eA0Zlc.WghbWd.FnEtTd.mkpRId.m3LIae.RLdvSe.qyKxnc.ivg-i.PZPZlf.GMCzAd")))
    except TimeoutException:
        print("No se encontraron imágenes usando el selector actualizado.")
        return

    downloaded_count = 0
    for i, img in enumerate(images, start=1):
        if downloaded_count >= max_images:
            break
        try:
            img.click()
            large_img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.pT0Scc")))
            src_url = large_img.get_attribute('src')
            if src_url and src_url.startswith('http'):
                download_image(src_url, folder_name, i)
                downloaded_count += 1
            else:
                print(f"URL no válido para la imagen {i}")
        except TimeoutException:
            print("Tiempo de espera excedido para la imagen.")
        except Exception as e:
            print(f"Error al manejar la imagen {i}: {e}")




# Example usage
search_URL = "https://www.google.com/search?q=mahindra+scorpio+2020&tbm=isch"
fetch_images(search_URL, 'mahindra_scorpio', max_images=500)
