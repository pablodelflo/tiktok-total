from core.app import TikTokApp
from services.videos_service import VideoService

def main():

    app = TikTokApp()

    print("0 - Salir de la app")
    print("1 - Descargar vídeos/fotos de una colección")
    print("2 - Desmarcar favoritos")
    print("3 - Herramientas para seguidores/siguiendo")

    opcion = input("Elige opción: ")

    if opcion == "1":
        VideoService(app).descargar_coleccion(
            input("URL colección: ")
        )

    elif opcion == "0":
        app.cerrar()

    '''elif opcion == "2":
    PhotoService(app).descargar_coleccion(
        input("URL colección: ")
    )
    '''


if __name__ == "__main__":
    main()