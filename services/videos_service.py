class VideoService:

    def __init__(self, app):
        self.app = app
        self.driver = app.driver
        self.base_path = app.base_path

    def descargar_coleccion(self, url):
        print("Descargando vídeos...")
        # Aquí va tu lógica actual