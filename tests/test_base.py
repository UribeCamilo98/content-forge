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
def test_imagen_fondo_cambia_contenido():
    import tempfile, os
    pb = PlantillaBase((255, 0, 0), (0, 0, 0))
    fondo = Image.new("RGB", (50, 50), (0, 255, 0))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fondo.save(f.name)
        img = pb._crear_imagen("Hola", ancho=200, alto=200, ruta_imagen_fondo=f.name)
    os.unlink(f.name)
    assert isinstance(img, Image.Image)
    assert img.size == (200, 200)

def test_colocaciones_sobre_fondo_blanco():
    pb = PlantillaBase((255, 255, 255), (0, 0, 0))
    overlay = Image.new("RGBA", (50, 50), (255, 0, 0, 255))
    colocaciones = [{"imagen": overlay, "x": 10, "y": 10, "w": 50, "h": 50}]
    img = pb._crear_imagen("Hola", ancho=200, alto=200, colocaciones=colocaciones)
    assert isinstance(img, Image.Image)
    px = img.getpixel((15, 15))
    assert px[0] > 200

def test_colocaciones_varias():
    pb = PlantillaBase((0, 0, 0), (255, 255, 255))
    rojo = Image.new("RGBA", (30, 30), (255, 0, 0, 255))
    verde = Image.new("RGBA", (30, 30), (0, 255, 0, 255))
    cols = [
        {"imagen": rojo, "x": 0, "y": 0, "w": 30, "h": 30},
        {"imagen": verde, "x": 100, "y": 100, "w": 30, "h": 30}
    ]
    img = pb._crear_imagen("Test", ancho=200, alto=200, colocaciones=cols)
    assert img.getpixel((5, 5))[0] > 200
    assert img.getpixel((105, 105))[1] > 200

def test_colocaciones_none_mismo_comportamiento():
    pb = PlantillaBase((100, 100, 100), (255, 255, 255))
    img_sin = pb._crear_imagen("Hola", ancho=100, alto=100)
    img_con = pb._crear_imagen("Hola", ancho=100, alto=100, colocaciones=None)
    assert img_sin.tobytes() == img_con.tobytes()