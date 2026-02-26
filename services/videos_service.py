from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from core.app import TikTokApp


class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path
 

    def descargar_coleccion(self, urlColeccion, nombreColeccion):
        print(f"\nDe acuerdo, quieres descargar la colección {nombreColeccion.title()}, cuya url es {urlColeccion}. Vamos para allá")
        self.driver.get(urlColeccion)
        print("Ya estamos aquí")
        # Aquí va tu lógica actual