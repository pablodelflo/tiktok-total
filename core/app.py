from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from time import sleep
import re

class TikTokApp:

    def __init__(self):
        self.base_path = Path(BASE_PATH_COLECCIONES)
        self.driver = get_driver()

    def cerrar(self):
        print("\nSaliendo de la app... ¡Hasta la próxima!")
        self.driver.quit()
    
    def bienvenida(self, url):
        ##Esta función solo obtiene info del perfil del usuario para mostrarlo en pantalla
        self.driver.get(url)

        name_usuario = self.driver.find_element(By.CSS_SELECTOR, css_username).text
        name_real = self.driver.find_element(By.CSS_SELECTOR, css_realname).text

        nombre = f"\n\nHola, {name_usuario} ({name_real})\n-----------------------------"

        return(nombre)


    def full_scroll(self, pausa=1):
        ##Esta función fuerza el scroll vertical para asegurar la carga de todos los elementos (vídeos, colecciones, etc)
        # Obtener altura inicial
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Hacer scroll al final
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)

            # Comparar altura después del scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                print("📉 Fin del scroll detectado, forzando scrolls adicionales...")
                
                # Hacer scrolls adicionales forzados
                for i in range(MAX_EXTRA_SCROLLS):
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(SCROLL_PAUSE_TIME)
                
                # Una última comprobación
                final_height = self.driver.execute_script("return document.body.scrollHeight")
                if final_height == last_height:
                    print("✅ Scroll final confirmado.")
                    break
                else:
                    print("🔁 Scroll reactivado, continuando...")
                    last_height = final_height
            else:
                last_height = new_height
    

    def define_coleccion(self, url):
        print("Vamos a ver las colecciones de tu perfil\n")
        goto_fav = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Favoritos')]").click()
        goto_colecciones = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Colecciones')]").click()
        self.full_scroll()
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

                # subir al <a> padre
                enlace = coleccion.find_element(By.XPATH, "./ancestor::a")
                url = enlace.get_attribute("href")

                colecciones.append({
                    "id": idx,
                    "nombre": nombre,
                    "cantidad": cantidad,
                    "url": url
                })
        
        print(f"\nTu perfil tiene {numero_colecciones} colección/es:")

        for collection in colecciones:
            if collection['cantidad']>0:
                print(f"{collection['id']} - {collection['nombre'].title()} → {collection['cantidad']} vídeo/s. URL: {collection['url']}")
            else:
                zeroCollection.append(collection['nombre'])

        print(f"\nAdemás, las siguientes colecciones están vacías:\n")
        for zC in zeroCollection:
            print(f"[X] {zC.title()}")

        idColeccion = int(input("\nIntroduce el ID de la colección que quieres descargar: "))
        idColeccion -=1 
        nombreColeccion = colecciones[idColeccion]['nombre']
        urlColeccion = colecciones[idColeccion]['url']
        numeroVideosCol = colecciones[idColeccion]['cantidad']

        print(f"\nLa colección es {nombreColeccion.title()} tiene {numeroVideosCol} vídeos y su URL es {urlColeccion}")

        print("¿Quieres descargar las descripciones de los vídeos de esta colección?")
        descripcion = input("¿Si/No?")

        if descripcion.upper() == 'SI':
            descripciones = True
        else:
            descripciones = False
        
        return urlColeccion, nombreColeccion, descripciones
    

    def prepara_estructura(self, nombreColeccion,descripciones):
        if descripciones:
            print("")
        else:
            print()