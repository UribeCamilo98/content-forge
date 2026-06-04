from utils.images import img_manager
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
