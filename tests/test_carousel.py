import os
from generator.carousel import Carrusel


def test_dividir_oraciones_con_puntuacion_seguida():
    c = Carrusel("dummy", (0,0,0), (255,255,255))
    oraciones = c._dividir_oraciones("Hola...  Mundo.")
    assert len(oraciones) == 2  # "Hola..." y "Mundo."

def test_distribuir_2_grupos_4_elementos():
    c = Carrusel("dummy", (0,0,0), (255,255,255))
    grupos = c._distribuir(["a","b","c","d"], 2)
    assert len(grupos) == 2

def test_distribuir_grupos_contienen_todos_los_elementos():
    c = Carrusel("dummy", (0,0,0), (255,255,255))
    grupos = c._distribuir(["a","b","c","d"], 2)
    assert len(grupos[0].split()) == 2
    assert len(grupos[1].split()) == 2

def test_procesar_textos_un_parrafo_una_oracion():
    c = Carrusel("Hola mundo.", (0,0,0), (255,255,255))
    assert len(c.textos) == 1

def test_procesar_textos_dos_parrafos_dos_slides():
    c = Carrusel("Primer párrafo.\n\nSegundo párrafo.", (0,0,0), (255,255,255))
    assert len(c.textos) == 2

def test_carrusel_con_imagen_fondo_renderiza():
    import tempfile, os, shutil
    from PIL import Image
    fondo = Image.new("RGB", (50, 50), (0, 255, 0))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fondo.save(f.name)
        c = Carrusel("Test slide.", (0,0,0), (255,255,255), ruta_imagen_fondo=f.name)
        img = c.render_slide(0)
    os.unlink(f.name)
    assert isinstance(img, Image.Image)

def test_carrusel_con_imagen_fondo_genera_slide():
    import tempfile, os, shutil
    from PIL import Image
    fondo = Image.new("RGB", (50, 50), (0, 0, 255))
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        fondo.save(f.name)
        c = Carrusel("Test slide.\n\nOtro slide.", (0,0,0), (255,255,255), ruta_imagen_fondo=f.name)
        ruta = c.generar()
    os.unlink(f.name)
    assert os.path.isdir(ruta)
    archivos = os.listdir(ruta)
    assert len(archivos) == 2
    assert all(f.endswith(".png") for f in archivos)
    shutil.rmtree(ruta)

def test_generar_crea_carpeta_con_imagenes():
    c = Carrusel("Primer slide.\n\nSegundo slide.", (0,0,0), (255,255,255))
    ruta = c.generar()
    assert os.path.isdir(ruta)
    archivos = os.listdir(ruta)
    assert len(archivos) == 2
    assert all(f.endswith(".png") for f in archivos)

    # Limpieza del test
    import shutil
    shutil.rmtree(ruta)