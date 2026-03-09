from core.app import TikTokApp
from services.videos_service import VideoService
from config import PROFILE_TIKTOK
from services.favoritos_service import FavService
#from core.driver_manager import get_driver


def main():

    app = TikTokApp()

    print(app.bienvenida(PROFILE_TIKTOK))

    while True:
        print("\n0 - Salir de la app")
        print("1 - Descargar vídeos/fotos de una colección")
        print("2 - Desmarcar favoritos")
        print("3 - Herramientas para seguidores/siguiendo")

        try:
            opcion = int(input("Elige opción: "))
            if opcion not in (0, 1, 2):
                raise ValueError
        except ValueError:
            print("\nDebes introducir una opción correcta. Vuelve a probar.")
            continue
        if opcion == 1:
            urlColeccion, nombreColeccion, descripciones = app.define_coleccion(PROFILE_TIKTOK)
            VideoService(app).descargar_coleccion(urlColeccion, nombreColeccion, descripciones)

        elif opcion == 2:
            result = app.coleccionFavoritos(PROFILE_TIKTOK)
            if result is None:
                continue
            urlColeccion, nombreColeccion = result
            FavService(app).desmarcarFavoritos(urlColeccion, nombreColeccion)
        
        elif opcion == 0:
            app.cerrar()
            break

if __name__ == "__main__":
    main()