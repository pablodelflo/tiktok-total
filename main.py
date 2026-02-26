from core.app import TikTokApp
from services.videos_service import VideoService
from config import PROFILE_TIKTOK
#from core.driver_manager import get_driver


def main():

    app = TikTokApp()

    print(app.bienvenida(PROFILE_TIKTOK))

    #print("")

    print("0 - Salir de la app")
    print("1 - Descargar vídeos/fotos de una colección")
    print("2 - Desmarcar favoritos")
    print("3 - Herramientas para seguidores/siguiendo")

    opcion = input("Elige opción: ")

    if opcion == "1":
        urlColeccion, nombreColeccion = VideoService(app).define_coleccion(PROFILE_TIKTOK)
        VideoService(app).descargar_coleccion(urlColeccion,nombreColeccion)

    elif opcion == "0":
        app.cerrar()

    '''elif opcion == "2":
    PhotoService(app).descargar_coleccion(
        input("URL colección: ")
    )
    '''


if __name__ == "__main__":
    main()