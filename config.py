from pathlib import Path
BASE_PATH_COLECCIONES = Path("C:/proyectos/Python/tiktok_total/COLECCIONES")
DEBUG_PORT = "127.0.0.1:9222"
PROFILE_TIKTOK = "https://www.tiktok.com/@lk2_89"
SCROLL_PAUSE_TIME = 2.5
MAX_EXTRA_SCROLLS = 2  # Scrolls adicionales después del final
MAX_THREADS = 4


##CLASES CSS PARA SCRAPPING##
#---------------------------#
#H1 y H2 nombre usuario y nombre real
css_username = 'h1[data-e2e="user-title"]'
css_realname = 'h2[data-e2e="user-subtitle"]'

#Enlaces de vídeos en colecciones
#video_colección = ''
contendor_video = 'a.css-1q1pv25-5e6d46e3--AMetaCaptionLine.er0oj30'

#Slider de fotos
slider_fotos = 'div.swiper-slide[data-swiper-slide-index]'