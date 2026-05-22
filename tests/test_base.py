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