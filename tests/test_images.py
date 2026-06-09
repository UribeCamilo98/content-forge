import io
import struct
from utils.images import img_manager

def _png_mini():
    """Genera un PNG mínimo de 1x1 px en memoria."""
    def _chunk(tipo, datos):
        c = tipo + datos
        return struct.pack(">I", len(datos)) + c + struct.pack(">I", __import__("zlib").crc32(c) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) + _chunk(b"IDAT", __import__("zlib").compress(b"\x00\xff\x00\x00")) + _chunk(b"IEND", b"")

def test_imagemanager_lista_vacia_si_sin_imagenes():
    imagenes = img_manager.listar_imagenes()
    assert isinstance(imagenes, list)
def test_obtener_ruta_imagen_inexistente_devuelve_none():
    ruta = img_manager.obtener_ruta("no_existe")
    assert ruta is None
def test_cargar_fondo_imagen_inexistente_devuelve_none():
    img = img_manager.cargar_fondo("no_existe", 1080, 1080)
    assert img is None
def test_refrescar_no_lanza_error():
    img_manager.refrescar()
    assert isinstance(img_manager.listar_imagenes(), list)
def test_listar_agrupadas_tiene_claves():
    agrupadas = img_manager.listar_agrupadas()
    assert "preinstaladas" in agrupadas
    assert "subidas" in agrupadas
    assert isinstance(agrupadas["preinstaladas"], list)
    assert isinstance(agrupadas["subidas"], list)
def test_guardar_archivo_extension_valida(tmp_path):
    contenido = _png_mini()
    nombre = img_manager.guardar_archivo("test_upload.png", contenido)
    assert nombre.startswith("test_upload_")
    agrupadas = img_manager.listar_agrupadas()
    assert nombre in agrupadas["subidas"]
def test_guardar_archivo_extension_invalida():
    try:
        img_manager.guardar_archivo("test.txt", b"hola")
        assert False, "Debió lanzar ValueError"
    except ValueError:
        pass
