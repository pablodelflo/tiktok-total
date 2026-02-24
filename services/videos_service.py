from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path

    def define_coleccion(self, url):
        print("Vamos a ver las colecciones de tu perfil")
        #self.driver.get(url)
        goto_fav = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Favoritos')]")
        goto_fav.click()
        goto_colecciones = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Colecciones')]")
        goto_colecciones.click()
        sleep(5)
        colecciones = []
        #list_colecciones = self.driver.find_elements(By.CSS_SELECTOR, 'div.css-118uiny-7937d88b--DivCollectionInfoContainer.esxudtv1')
        list_colecciones = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="collection-card-footer"]')

        for coleccion in list_colecciones:
            spans = coleccion.find_elements(By.TAG_NAME, "span")

            if len(spans) >= 2:
                nombre = spans[0].text
                cantidad = spans[1].text
                colecciones.append(f"{nombre} ({cantidad})")
        
        #print(colecciones)

        print(f"Tu perfil tiene estas colecciones: {colecciones}")

        

    def descargar_coleccion(self, url):
        print("Descargando vídeos...")
        # Aquí va tu lógica actual