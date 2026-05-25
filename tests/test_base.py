from generator.base import PlantillaBase
from config import PRESETS_TAMANO
from PIL import Image

def test_crear_imagen_retorna_pil_image():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    img = pb._crear_imagen("Hola")
    assert isinstance(img, Image.Image)
def test_crear_imagen_tamano_correcto():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    img = pb._crear_imagen("Hola")
    assert img.size == (PRESETS_TAMANO["cuadrado"])
def test_crear_imagen_fondo_correcto():
    pb = PlantillaBase((255, 0, 0), (0, 0, 0))
    img = pb._crear_imagen("Hola")
    assert img.getpixel((0, 0)) == (255, 0, 0)
def test_texto_vacio_no_crashea():
    pb = PlantillaBase((0, 0, 0), (255, 255, 255))
    img = pb._crear_imagen("")
    assert isinstance(img, Image.Image)
def test_contorno_agrega_pixeles():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    img_sin = pb._crear_imagen("Hola")
    img_con = pb._crear_imagen("Hola", contorno_color=(255, 0, 0), contorno_grosor=3)
    assert img_sin.tobytes() != img_con.tobytes()
def test_sombra_agrega_pixeles():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    img_sin = pb._crear_imagen("Hola")
    img_con = pb._crear_imagen("Hola", sombra_offset=(10, 10), sombra_color=(128, 128, 128))
    assert img_sin.tobytes() != img_con.tobytes()
def test_contorno_none_sin_cambio():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    img_sin = pb._crear_imagen("Hola")
    img_con = pb._crear_imagen("Hola", contorno_color=None)
    assert img_sin.tobytes() == img_con.tobytes()