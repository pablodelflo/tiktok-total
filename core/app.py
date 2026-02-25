from pathlib import Path
from config import *
from core.driver_manager import get_driver
from selenium.webdriver.common.by import By
from time import sleep

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