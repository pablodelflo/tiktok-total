import time
import openpyxl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pathlib import Path
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
import yt_dlp
import os
import re
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
import requests
import glob

###################
###  VARIABLES  ###
###################

#path_base = Path("C:/Users/lk2_89/Documents/Proyectos y varios/Python/tiktok_bot/COLECCIONES")
path_base = Path("C:/proyectos/Python/tiktok_bot/COLECCIONES")

clave='/video/'
foto='/photo/'
clavev2='https://www.tiktok.com/'
tiktoker='/@'
tiktokerv2='com/@'
contador = 0
contadorKO = 0
comprueba = []
#colecciones_con_descripcion = ["INGLÉS""Egypt!","DIY","Viajes","Futbol", "Podcast", "DECO_2", "Deco","Cocina_2","Cocina","FUT2","BARES","SALSAS","Perretes","NAVIDAD"]
download_desc = False

###################
###  FUNCIONES  ###
###################

def descargar_un_video(video: str, directorio_videos: Path, clave: str, tiktoker: str):
    path_base = Path("C:/proyectos/Python/tiktok_bot/COLECCIONES")
    borra_favoritos = directorio_videos.parent / "delete_fav.txt"
    pendiente_favoritos = directorio_videos.parent / "pdte_fav.txt"

    try:
        video = video.strip()
        nombre_video = video.index(clave)
        nombreOK = video[nombre_video+7:]
        nombre_autor = video.index(tiktoker)
        autorOK = video[nombre_autor+2:nombre_video]
        full_nombre = f"{autorOK.strip()} - {nombreOK.strip()}.mp4"

        comando = [
            "yt-dlp", "--cookies", "cookies.txt",
            "-o", full_nombre,
            "-P", str(directorio_videos),
            video,
            "-q"
        ]

        result = subprocess.run(comando, capture_output=True, text=True)
        if result.returncode != 0:
            return f"❌ Error con {full_nombre}: {result.stderr.strip()}"
        
        ruta_absoluta_video = os.path.join(directorio_videos,full_nombre)
        #print(ruta_absoluta_video)

        if os.path.isfile(ruta_absoluta_video):
            #print("--------EXISTE")
            with open(borra_favoritos, "a", encoding="utf-8") as bf:
                bf.write(video + "\n")
        else:
            print("❌ --------NO EXISTE")
            with open(pendiente_favoritos, "a", encoding="utf-8") as bf:
                bf.write(video + "\n")

        return f"✅ Descargado: {full_nombre}"

    except Exception as e:
        return f" Error procesando: {video} → {e}"
    
    
def descarga_videos(directorio_videos, lista_videos, total_videos, clave, tiktoker, max_hilos=4):
    with open(lista_videos, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    with ThreadPoolExecutor(max_workers=max_hilos) as executor:
        tareas = [
            executor.submit(descargar_un_video, video, directorio_videos, clave, tiktoker)
            for video in urls
        ]

        for f in tqdm(as_completed(tareas), total=len(urls), desc="Descargando vídeos", unit=" video/s"):
            resultado = f.result()
            tqdm.write(resultado)


def descargar_una_imagen(img_url, directorio_OK, indice, id_OK):

    try:
        r = requests.get(img_url, timeout=15)
        r.raise_for_status()

        nombre_fichero = f"{id_OK}_{indice}.jpg"
        ruta_fichero = os.path.join(directorio_OK, nombre_fichero)

        with open(ruta_fichero, "wb") as f:
            f.write(r.content)

    except Exception as e:
        print(f"Error descargando imagen {indice}: {e}")


def descarga_fotos(ruta_fotos: Path, full_path_photos, num_fotos, foto, tiktoker):

    with open(full_path_photos, "r", encoding="utf-8") as fotos:

        for photo in tqdm(fotos, desc="Descargando fotos ", unit=" foto/s"):

            url_photo = photo.strip()
            driver.get(url_photo)
            sleep(2)

            slides = driver.find_elements(
                By.CSS_SELECTOR,
                'div.swiper-slide[data-swiper-slide-index]'
            )

            # Obtener índices únicos reales
            indices = {
                slide.get_attribute("data-swiper-slide-index")
                for slide in slides
            }

            numero_fotos_publi = len(indices)
            print(f"La publicación tiene {numero_fotos_publi} fotos")

            # Extraer autor e id
            autor_pos = url_photo.index(tiktoker)
            id_pos = url_photo.index(foto)

            autor_OK = url_photo[autor_pos + 2:id_pos]
            id_OK = url_photo[id_pos + 7:]

            # ✅ Crear nombre de carpeta correcto
            nombre_dir = f"{autor_OK} - {id_OK}"
            directorio_OK = ruta_fotos / nombre_dir

            # Crear carpeta si no existe
            directorio_OK.mkdir(parents=True, exist_ok=True)

            # Descargar imágenes
            for slide in slides:
                index = slide.get_attribute("data-swiper-slide-index")
                img = slide.find_element(By.TAG_NAME, "img")
                img_url = img.get_attribute("src")

                descargar_una_imagen(
                    img_url,
                    str(directorio_OK),
                    index,
                    id_OK
                )

            # -----------------------------------
            # ✅ COMPROBACIÓN CORRECTA
            # -----------------------------------

            fotos_descargadas = list(directorio_OK.glob("*.jpg"))
            numero_fotos_descargadas = len(fotos_descargadas)

            print(
                f"Descargadas {numero_fotos_descargadas} "
                f"de {numero_fotos_publi}"
            )

            borra_favoritos = ruta_fotos.parent / "delete_fav.txt"
            pendiente_favoritos = ruta_fotos.parent / "pdte_fav.txt"

            if numero_fotos_descargadas == numero_fotos_publi:
                with open(borra_favoritos, "a", encoding="utf-8") as bf:
                    bf.write(url_photo + "\n")
            else:
                print("❌ Número de fotos no coincide")
                with open(pendiente_favoritos, "a", encoding="utf-8") as bf:
                    bf.write(url_photo + "\n")


############################
###  COLECCIONES TIKTOK  ###
############################
#driver.get('https://www.tiktok.com/@lk2_89/collection/Futbol-7144318295951985414')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Podcast-7136541040690121478')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Cocina-7220764663899278085')
#driver.get('https://www.tiktok.com/@lk2_89/collection/VARIOS-7238629674440461083')
#driver.get('https://www.tiktok.com/@lk2_89/collection/MAMASOTA-7238638399544380186')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Navidad-7299362851322465056')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Deco-7139456759835462405')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Recetas%20Monsieur-7404883331617245985')
#driver.get('https://www.tiktok.com/@lk2_89/collection/ACShadows-7489344934026251031')
#driver.get('https://www.tiktok.com/@lk2_89/collection/MMST2-7522989649163733782')
#driver.get('https://www.tiktok.com/@lk2_89/collection/3D-7593770981689281302')

#############################################
###  CARGAMOS Y ABRIMOS EL DRIVER CHROME  ###
#############################################
# Configura Selenium
options = Options()
Options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

colecciones_con_descripcion = ["MADRID","3D","Recetas","LIBROS","SHEINNN","DOMOTICA","RDR2","Rutas senderismo","Bebidas","PELIS & SERIES","ALBAÑILERÍA","CASA","GYM","IT!","Podcast","ACShadows","SIMS","Recetas Thermomix","CHISTES","DIABETES","SUPERMERCADOS","INGLÉS""Egypt!","DIY","Viajes","Futbol", "Podcast", "DECO_2", "Deco","Cocina_2","Cocina","FUT2","BARES","SALSAS","Perretes","NAVIDAD"]

driver.get('https://www.tiktok.com/@lk2_89/collection/Recetas-7220764663899278085')
#driver.get('https://www.tiktok.com/@lk2_89/collection/MADRID-7578597178436619030')
#driver.get('https://www.tiktok.com/@lk2_89/collection/3D-7593770981689281302')
#driver.get('https://www.tiktok.com/@lk2_89/collection/Futbol-7144318295951985414')
SCROLL_PAUSE_TIME = 2.5
MAX_EXTRA_SCROLLS = 2  # Scrolls adicionales después del final

# Obtener altura inicial
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Hacer scroll al final
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(SCROLL_PAUSE_TIME)

    # Comparar altura después del scroll
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    if new_height == last_height:
        print("📉 Fin del scroll detectado, forzando scrolls adicionales...")
        
        # Hacer scrolls adicionales forzados
        for i in range(MAX_EXTRA_SCROLLS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
        
        # Una última comprobación
        final_height = driver.execute_script("return document.body.scrollHeight")
        if final_height == last_height:
            print("✅ Scroll final confirmado.")
            break
        else:
            print("🔁 Scroll reactivado, continuando...")
            last_height = final_height
    else:
        last_height = new_height

###############################################
###  TRABAJAMOS LOS VÍDEOS DE LA COLECCIÓN  ###
###############################################

##PRIMERO, OBTENER Nº DE VÍDEOS DE LA COLECCIÓN Y NOMBRE DE LA MISMA
num_videos = driver.find_element(By.CSS_SELECTOR, 'h2.css-1yqadhb-7937d88b--H2SubTitle.e18j1j0m0').text
nombre_coleccion = driver.find_element(By.CSS_SELECTOR, 'h1.css-isz8q8-7937d88b--H1ShareTitle.empjf524').text

print("La colección se llama: " + str(nombre_coleccion) + " y tiene " + str(num_videos) + ".")

##COMPROBAR SI EXISTE LA CARPETA DE LA COLECCIÓN, SI NO, CREARLA.
collection_path = path_base / nombre_coleccion
ruta_videos = collection_path / "VIDEOS"
ruta_fotos = collection_path / "FOTOS"
ruta_descripciones = collection_path / "DESCRIPCIONES"

rutas = [ruta_videos, ruta_descripciones, ruta_fotos]

for ruta in rutas:
    if os.path.exists(ruta):
        print(f"La ruta existe: {ruta}")
    else:
        print(f"No existe: {ruta}, la creamos.")
        os.makedirs(ruta)

full_path_videos = collection_path / "videos.txt"
full_path_photos = collection_path / "fotos.txt"

##OBTENER URLs Y ESCRIBIRLAS EN UN TXT
#Primero, comprobamos si la colección incluye descripciones
if nombre_coleccion in colecciones_con_descripcion:
    print(f"La colección {nombre_coleccion} está definida para descargar las descripciones.")
    download_desc = True
    descripciones = driver.find_elements(By.CSS_SELECTOR, 'a.css-5udr5j-7937d88b--AMetaCaptionLine.ensh35y0')
else:
    print(f"La colección {nombre_coleccion} no está definida para descargar las descripciones.")

#Definimos el fichero en modo escritura
#fichero = open(r"C:\Users\lk2_89\Documents\Proyectos y varios\Python\tiktok_bot\videos.txt","w", encoding="utf-8")
videos = driver.find_elements(By.CSS_SELECTOR, 'a.css-1undbtb-7937d88b--AVideoContainer.e7uspnp4')
urls = [v.get_attribute("href") for v in videos if v.get_attribute("href")]

with full_path_videos.open("w", encoding="utf-8") as fich_videos, \
     full_path_photos.open("w", encoding="utf-8") as fich_fotos:

    for url, descr in zip(urls, descripciones):

        if clave in url:
            fich_videos.write(url + "\n")

            nombre_video = url.index(clave)
            nombreOK = url[nombre_video+7:]

            nombre_tiktoker = url.index(tiktokerv2)
            tiktoker_OK = url[nombre_tiktoker+5:nombre_video]

            if download_desc:
                descripcion = descr.get_attribute("title")
                if descripcion:
                    nombre_descripcion = f"{tiktoker_OK} - {nombreOK}.txt"
                    full_path_desc_video = os.path.join(
                        ruta_descripciones, nombre_descripcion
                    )

                    with open(full_path_desc_video, "w", encoding="utf-8") as f:
                        f.write(descripcion)

        elif foto in url:
            fich_fotos.write(url + "\n")


numero_videos = int(num_videos.split()[0])
descarga_videos(ruta_videos, full_path_videos, numero_videos, clave, tiktoker)
print("Finalizada la descarga de vídeos.")

with full_path_photos.open("r", encoding="utf-8") as ff:
    cuentaphotos=sum(1 for _ in ff)

if cuentaphotos >= 1:
    print("Hay fotos para descargar. Procedemos")
    print("Comprobamos si la colección ya dispone de directorio de descarga.")

    '''
    if os.path.exists(ruta_fotos):
        print(f"La ruta existe: {ruta_fotos}")
    else:
        print(f"La ruta no existe, la creamos: {ruta_fotos}")
        os.makedirs(ruta_fotos)
    '''

    descarga_fotos(ruta_fotos, full_path_photos, cuentaphotos, foto, tiktoker)
    print("Finalizada la descarga de fotos.")

print("\nProceso finalizado.")