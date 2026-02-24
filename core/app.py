from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By

class TikTokApp:

    def __init__(self):
        self.base_path = Path(BASE_PATH_COLECCIONES)
        self.driver = get_driver()

    def cerrar(self):
        print("\nSaliendo de la app... ¡Hasta la próxima!")
        self.driver.quit()
    
    def navegar(self, url):
        self.driver.get(url)

        #name_usuario = self.driver.find_element(By.CSS_SELECTOR, 'h1.css-18md4rm-7937d88b--H1ShareTitle.ed8bszu8').text
        #name_real = self.driver.find_element(By.CSS_SELECTOR, 'h2.css-dgridp-7937d88b--H2ShareSubTitle.empjf527').text

        #name_usuario = self.driver.find_element(By.CSS_SELECTOR, 'h1[data-e2e="user-title"]').text
        #name_real = self.driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-subtitle"]').text
        name_usuario = self.driver.find_element(By.CSS_SELECTOR, css_username).text
        name_real = self.driver.find_element(By.CSS_SELECTOR, css_realname).text

        nombre = f"\n\nHola, {name_usuario} ({name_real})\n-----------------------------"

        return(nombre)        