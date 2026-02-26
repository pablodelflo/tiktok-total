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
 

    def descargar_coleccion(self, urlColeccion, nombreColeccion, descripciones=False):
        print(f"\nEspera mientras nos dirigimos a la colección {nombreColeccion.title()}")
        self.driver.get(urlColeccion)
        print("Ya estamos aquí")
        # Aquí va tu lógica actual