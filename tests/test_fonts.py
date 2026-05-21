from utils.fonts import font_manager
def test_fontmanager_tiene_fuentes_cargadas():
    fuentes = font_manager.listar_fuentes()
    assert len(fuentes) == 3
def test_listar_fuentes_incluye_las_descargadas():
    fuentes = font_manager.listar_fuentes()
    assert "Micro5-Regular" in fuentes
    assert "RubikGlitch-Regular" in fuentes
    assert "UncialAntiqua-Regular" in fuentes
def test_obtener_ruta_devuelve_path_valido():
    ruta = font_manager.obtener_ruta("Micro5-Regular")
    assert ruta is not None
    assert ruta.endswith(".ttf")
def test_obtener_ruta_fuente_inexistente_devuelve_none():
    ruta = font_manager.obtener_ruta("NoExiste")
    assert ruta is None