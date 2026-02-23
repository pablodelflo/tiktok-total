from pathlib import Path
from config import BASE_PATH_COLECCIONES
from core.driver_manager import get_driver

class TikTokApp:

    def __init__(self):
        self.base_path = Path(BASE_PATH_COLECCIONES)
        self.driver = get_driver()

    def cerrar(self):
        self.driver.quit()