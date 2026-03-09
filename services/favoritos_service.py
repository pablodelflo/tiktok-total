from config import *
from services.videos_service import *
from core.driver_manager import get_driver
from core.app import TikTokApp
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FavService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path


    def checkFotos(self, foto, collection_path):
        """
        Esta función debe comprobar que la publicación de fotos tenga el mismo nº 
        en local que en la publi antes de desmarcarla
        Recibe:
            * foto → url de publicación de fotos y el directorio de colecciones
            * collection_path → directorio de la colección
        Devuelve:
            * coleccionOK → booleano si la colección está correcta
            * reDownload → list con las publicaciones a descargar de nuevo
            * colCorrectas → int con el nº de publicaciones descargadas correctamente
            * colFallidas → int con el nº de publicaciones erróneamente descargadas
        """
        dirFotos = collection_path / "Fotos"
        coleccionOK = False
        reDownload = []
        colCorrectas = 0
        colFallidas = 0

        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, slider_fotos)))
        slides = self.driver.find_elements(By.CSS_SELECTOR, slider_fotos)
        indices = {slide.get_attribute("data-swiper-slide-index")
                   for slide in slides}
        numFotosPubli = len(indices)
        print(f"\n--La publicación tiene {numFotosPubli} foto/s--")

        print("Comparamos con las fotos en local")
        full_name = self.app.info_video(foto)
        dirFotosFull = dirFotos / full_name
        print(dirFotosFull)
        if dirFotosFull.exists():
            print("La publicación existe en local, veamos si coincide en nº de ficheros")
            checkDescargadas = list(dirFotosFull.glob("*.jpg"))
            numDescargadas = len(checkDescargadas)
            print(numDescargadas)
            if numDescargadas == numFotosPubli:
                print("Perfecto, la publicación tiene todas las fotos descargadas")
                coleccionOK = True
                colCorrectas +=1
                sleep(5)
                return coleccionOK, reDownload, colCorrectas, colFallidas
            else:
                print("La publicación no tiene el mismo nº de fotos, hay que volver a descargarla")
                reDownload.append(full_name)
                colFallidas +=1
                sleep(5)
                return coleccionOK, reDownload, colCorrectas, colFallidas
        else: 
            print("La publicación no está en local")
            sleep(5)
            return coleccionOK, reDownload, colCorrectas, colFallidas



    def quitaFavoritos(self, videos, fotos, collection_path):
        totalVideos = len(videos)
        totalFotos = len(fotos)
        print(f"\nEsta colección tiene un total de {totalVideos} vídeo/s y {totalFotos} foto/s para desmarcar.")

        #for idx, coleccion in enumerate(list_colecciones, start=1):

        #for video in videos:
        for idx, video in enumerate(videos, start=1):
            self.driver.get(video)
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.css-8cdu41-5e6d46e3--ButtonActionItem.efpxn6t0")))
            boton_fav = self.app.checkFavorito()
            if idx==1 or idx%10==0:
                print("\n---- [[ Desmarcando favoritos ]] ----")
            if "#FACE15" in boton_fav:
                btn = self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Añadir a Favoritos')]")
                btn.click()
                print(f"Desmarcando {idx} de {totalVideos} video/s")
            else:
                print("Este vídeo no está marcado como favorito")
            sleep(2)


        #for foto in fotos:
        for idx, foto in enumerate(fotos, start=1):
            self.driver.get(foto)
            descargaOk, reDownload, colCorrectas, colFallidas  = self.checkFotos(foto, collection_path)
            if descargaOk:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.css-8cdu41-5e6d46e3--ButtonActionItem.efpxn6t0")))
                boton_fav = self.app.checkFavorito()
                print("\n---- [[ Desmarcando favoritos ]] ----")
                if "#FACE15" in boton_fav:
                    btn = self.driver.find_element(By.XPATH,"//button[contains(@aria-label,'Añadir a Favoritos')]")
                    btn.click()
                    print(f"Desmarcando {idx} de {totalFotos} foto/s")
                else:
                    print("Esta foto no está marcada como favorito")
                sleep(2)

        if colCorrectas and colFallidas:
            print(f"Hay un total de {colCorrectas} descargas correctas y {colFallidas} descargas erróneas")
        if reDownload:
            print(f"Las siguientes colecciones deben volver a descargarse: \n{reDownload}")

    
    def desmarcarFavoritos(self, urlColeccion, nombreColeccion):
        print(f"\nAntes de continuar, vamos a comprobar que la colección existe en tu directorio de carpetas local")
        collection_path,existePath = self.app.checkEstructura(nombreColeccion)

        if existePath:
            print(f"Genial, la colección {nombreColeccion} existe en tu ruta local. Continuamos.")
        else:
            print(f"Error. La colección no existe en tu ruta local. Saliendo del programa.")
            exit()

        print(f"\nEspera mientras nos dirigimos a la colección {nombreColeccion.title()}")
        self.driver.get(urlColeccion)
        print("Ya estamos aquí. Ahora, vamos a obtener el listado de vídeos y fotos que tienes descargados en tu carpeta local")
        videos, fotos = self.app.getDescargados(collection_path)
        self.quitaFavoritos(videos, fotos, collection_path)