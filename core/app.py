from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from time import sleep
import re
import os
import glob
from pathlib import Path

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

    def info_video(self, url):
        path = urlparse(url).path
        partes = path.split("/")

        usuario = partes[1][1:]      # quita el @
        video_id = partes[3]

        full_name = usuario + " - " + video_id 

        return full_name
    

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
        descripcion = input("¿Si/No? → ")

        if descripcion.upper() == 'SI':
            descripciones = True
        else:
            descripciones = False
        
        return urlColeccion, nombreColeccion, descripciones


    def prepara_estructura(self, nombreColeccion, descripciones):
        collection_path = BASE_PATH_COLECCIONES / nombreColeccion

        rutas = [
            collection_path / "Videos",
            collection_path / "Fotos"
        ]

        if descripciones:
            rutas.append(collection_path / "Descripciones")

        print(f"\nCreando estructura para la colección → {nombreColeccion.title()}")

        for ruta in rutas:
            ruta.mkdir(parents=True, exist_ok=True)
            print(f"{ruta}")

        return collection_path


    def get_enlaces_descripciones(self, collection_path, descripciones):
        print("Ahora, analizamos los vídeos y fotos de la colección para obtener sus enlaces")
        self.full_scroll()

        videos_txt = collection_path / "videos.txt"
        fotos_txt = collection_path / "fotos.txt"
        descripciones_path = collection_path / "Descripciones"
        
        publicaciones = self.driver.find_elements(By.CSS_SELECTOR, contendor_video)

        with videos_txt.open("w", encoding="utf-8") as fich_videos, \
            fotos_txt.open("w", encoding="utf-8") as fich_fotos:

            for publicacion in publicaciones:
                url = publicacion.get_attribute("href")
                if "/video/" in url:
                    fich_videos.write(url + "\n")
                elif "/photo/" in url:
                    fich_fotos.write(url + "\n")
                else:
                    print(f"No sé que hacer con esto → {url}")

                if descripciones:
                    descripcion = publicacion.get_attribute("title")
                    full_name = self.info_video(url)
                    full_path_desc = descripciones_path / f"{full_name}.txt"
                    with full_path_desc.open("w", encoding="utf-8") as desc:
                        desc.write(descripcion)
        
        print("He finalizado la obtención de enlaces de la colección")

        hayFotos = hayVideos = False

        if videos_txt.exists():
            hayVideos = True
        if fotos_txt.exists():
            hayFotos = True

        return hayVideos, hayFotos
    

## FUNCIONES PARA FAVORITOS ##
    def coleccionFavoritos (self, url):
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

        idColeccion = int(input("\nIntroduce el ID de la colección en la que quieres desmarcar favoritos: "))
        idColeccion -=1 
        nombreColeccion = colecciones[idColeccion]['nombre']
        urlColeccion = colecciones[idColeccion]['url']
        numeroVideosCol = colecciones[idColeccion]['cantidad']

        print(f"\nLa colección es {nombreColeccion.title()} tiene {numeroVideosCol} vídeos y su URL es {urlColeccion}")

        return urlColeccion, nombreColeccion
    

    def checkEstructura(self, nombreColeccion):
        existePath = os.path.exists(BASE_PATH_COLECCIONES / nombreColeccion)

        if existePath:
            collectionPath = BASE_PATH_COLECCIONES / nombreColeccion
        else:
            collectionPath = BASE_PATH_COLECCIONES

        return collectionPath, existePath
    
    '''
        def getDescargados(self, collection_path):
            videosPath = collection_path / "videos"
            fotosPath = collection_path / "fotos"
            videos = []
            fotos = []

            for fichero in videosPath.iterdir():
                if fichero.is_file():
                    video = fichero.name.split(" - ")
                    idUsuario = video[0]
                    idVideo = video[1].split(".mp4")[0]
                    urlVideoBase = f"https://www.tiktok.com/@{idUsuario}/video/{idVideo}"
                    videos.append(urlVideoBase)
            
            for carpeta in fotosPath.iterdir():
                foto = carpeta.name.split(" - ")
                idUsuario = foto[0]
                idFoto = foto[1]
                urlFotoBase = f"https://www.tiktok.com/@{idUsuario}/photo/{idFoto}"
                fotos.append(urlFotoBase)

            return videos, fotos
    '''


    def getDescargados(self, collection_path):
        videosPath = collection_path / "videos"
        fotosPath = collection_path / "fotos"
        videos = {}
        fotos = {}
        videosLocal = []
        fotosLocal = []

        #Primero, volver a obtener listado de fotos/videos (temporales, los podemos borrar después)
        #Hacemos full scroll
        self.full_scroll()

        publicaciones = self.driver.find_elements(By.CSS_SELECTOR, contendor_video)

        for publicacion in publicaciones:
            url = publicacion.get_attribute("href")
            if "/video/" in url:
                nombreVideo = self.info_video(url)
                #fich_videos.write(nombreVideo + "\n")
                videos[nombreVideo] = url
            elif "/photo/" in url:
                nombreFoto = self.info_video(url)
                #fich_fotos.write(nombreFoto + "\n")
                fotos[nombreFoto] = url
            else:
                print(f"No sé que hacer con esto → {url}")

        #Ya tenemos los elementos de la colección. Ahora, los locales
        for fichero in videosPath.iterdir():
            if fichero.is_file():
                video = fichero.stem
                videosLocal.append(video)
        
        for carpeta in fotosPath.iterdir():
            fotosLocal.append(carpeta.name)

        videos_a_desmarcar = [videos[nombre] for nombre in videosLocal if nombre in videos]
        fotos_a_desmarcar = [fotos[nombre] for nombre in fotosLocal if nombre in fotos]

        return videos_a_desmarcar, fotos_a_desmarcar
    

    def checkFavorito(self):
        boton = self.driver.find_element(By.CSS_SELECTOR, 'button[aria-label*="Añadir a Favoritos"]')
        path_element = boton.find_element(By.CSS_SELECTOR, 'path:first-child')
        fill_value = path_element.get_attribute("fill")

        return fill_value