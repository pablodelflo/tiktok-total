from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from core.app import TikTokApp
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import requests
import glob


class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def descargar_un_video(self, video, full_path_video):
        try:
            full_name = self.app.info_video(video)
            full_name_video = f"{full_name}.mp4"

            comando = [
                #"yt-dlp",
                "py", "-3.11", "-m", "yt_dlp",
                #"--cookies", "cookies.txt",
                "--cookies-from-browser", "firefox",
                "-o", full_name_video,
                "-P", str(full_path_video),
                video,
                "-q"
            ]

            result = subprocess.run(comando, capture_output=True, text=True)
            if result.returncode != 0:
                return f"❌ Error con {full_name_video}: {result.stderr.strip()}"
            
            return f"✅ Descargado: {full_name_video}"
        
        except Exception as e:
            return f" Error procesando: {video} → {e}"
    

    def descargar_una_foto(self, img_url, dirFotos, index, idPublicacion):
        try:
            r = requests.get(img_url, timeout=15)
            r.raise_for_status()

            nombreFoto = f"{idPublicacion}_{index}.jpg"
            rutaFoto = dirFotos / nombreFoto

            with rutaFoto.open("wb") as foto:
                foto.write(r.content)

        except Exception as e:
            print(f"Error descargando imagen {index}: {e}")


    def descarga_videos(self, collection_path, MAX_THREADS):
        listaVideos = collection_path / "videos.txt"
        full_path_video = collection_path / "videos"
        print("Iniciamos la descarga de vídeos.")

        with listaVideos.open("r", encoding="utf-8") as fich_videos:
            urls = [line.strip() for line in fich_videos if line.strip()]
            
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            tareas = [
                executor.submit(self.descargar_un_video, video, full_path_video)
                for video in urls
            ]

            for f in tqdm(as_completed(tareas), total=len(urls), desc="Descargando vídeos", unit=" video/s"):
                resultado = f.result()
                tqdm.write(resultado)

    
    def descarga_fotos(self, collection_path):
        listaFotos = collection_path / "fotos.txt"
        full_path_foto = collection_path / "Fotos"

        print("Iniciamos la descarga de fotos.")

        with listaFotos.open("r", encoding="utf-8") as fich_fotos:
            
            for foto in tqdm(fich_fotos, desc="Descargando fotos ", unit=" foto/s"):
                url_foto = foto.strip()
                self.driver.get(url_foto)
                sleep(2)

                slides = self.driver.find_elements(By.CSS_SELECTOR, slider_fotos)

                indices = {slide.get_attribute("data-swiper-slide-index")
                           for slide in slides}
                
                numFotosPubli = len(indices)
                print(f"\n--La publicación tiene {numFotosPubli} foto/s--")

                nombre_dir_format = self.app.info_video(url_foto)
                id_post = nombre_dir_format.split("-")
                idPublicacion = id_post[1]
                dirFotos = full_path_foto / nombre_dir_format
                dirFotos.mkdir(parents=True, exist_ok=True)

                for slide in slides:
                    index = slide.get_attribute("data-swiper-slide-index")
                    img = slide.find_element(By.TAG_NAME, "img")
                    img_url = img.get_attribute("src")

                    self.descargar_una_foto(img_url, dirFotos, index, idPublicacion)
                
                checkDescargadas = list(dirFotos.glob("*.jpg"))
                numDescargadas = len(checkDescargadas)

                print(f"Se han descargado {numDescargadas} de {numFotosPubli} foto/s")

                if (numDescargadas != numFotosPubli):
                    print("No se han descargado todas las imágenes, hay que relanzarlo.")



    def descargar_coleccion(self, urlColeccion, nombreColeccion, descripciones=False):
        print(f"\nEspera mientras nos dirigimos a la colección {nombreColeccion.title()}")
        self.driver.get(urlColeccion)
        print("Ya estamos aquí. Vamos primero con la estructura de carpetas")
        collection_path = self.app.prepara_estructura(nombreColeccion, descripciones)
        hayVideos, hayFotos = self.app.get_enlaces_descripciones(collection_path, descripciones)

        if hayVideos:
            self.descarga_videos(collection_path, MAX_THREADS)
        else:
            print("No hay vídeos para descargar")

        if hayFotos:
            self.descarga_fotos(collection_path)
        else:
            print("No hay fotos para descargar")