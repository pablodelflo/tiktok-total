from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from core.app import TikTokApp
import re

class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def define_coleccion(self, url):
        print("Vamos a ver las colecciones de tu perfil\n")
        goto_fav = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Favoritos')]").click()
        goto_colecciones = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Colecciones')]").click()
        self.app.full_scroll()
        colecciones = []
        zeroCollection = []
        numero_colecciones = int(re.search(r"\d+",self.driver.find_element(By.ID, "collections").text).group())
        list_colecciones = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="collection-card-footer"]')

        for idx, coleccion in enumerate(list_colecciones, start=1):
            spans = coleccion.find_elements(By.TAG_NAME, "span")

            if len(spans) >= 2:
                nombre = spans[0].text.strip()
                cantidad_texto = spans[1].text.strip()   # "345 vídeos"
                cantidad = int(cantidad_texto.split()[0])  # 345

                colecciones.append({
                    "id": idx,
                    "nombre": nombre,
                    "cantidad": cantidad
                })
        
        print(f"\nTu perfil tiene {numero_colecciones} colección/es:")

        for collection in colecciones:
            if collection['cantidad']>0:
                print(f"{collection['id']} - {collection['nombre']} → {collection['cantidad']} vídeo/s.")
            else:
                zeroCollection.append(collection['nombre'])

        print(f"\nAdemás, las siguientes colecciones están vacías:\n")
        for zC in zeroCollection:
            print(zC)

        idColeccion = input("Introduce el ID de la colección que quieres descargar: ")
        idColeccion =+1 
        nombreColeccion = colecciones[idColeccion]['nombre']
        urlColeccion = self.driver.find_elements(By.CSS_SELECTOR, 'div[data-e2e="collection-card-footer"]')

        print(f"La colección es {nombreColeccion} cuyo ID real es {idColeccion}")

        return(urlColeccion)
 

    def descargar_coleccion(self, url):
        print("Descargando vídeos...")
        # Aquí va tu lógica actual