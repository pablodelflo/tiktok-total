from config import PROFILE_TIKTOK

class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path

    def define_coleccion(self):
        
        print("Tu perfil ")

    def descargar_coleccion(self, url):
        print("Descargando vídeos...")
        # Aquí va tu lógica actual