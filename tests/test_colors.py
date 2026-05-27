
from utils.colors import obtener_paleta, PALETAS

def test_obtener_paleta_conocida_devuelve_dict_con_claves():
    paleta = obtener_paleta("oscuro")
    assert "fondo" in paleta
    assert "texto" in paleta

def test_obtener_paleta_conocida_devuelve_valores_correctos():
    paleta = obtener_paleta("oscuro")
    assert paleta["fondo"] == "#191923"
    assert paleta["texto"] == "#ffffff"

def test_obtener_paleta_desconocida_devuelve_oscuro():
    paleta = obtener_paleta("no_existe")
    assert paleta == obtener_paleta("oscuro")

def test_todas_las_paletas_tienen_fondo_y_texto():
    for nombre, paleta in PALETAS.items():
        assert "fondo" in paleta, f"Paleta '{nombre}' sin 'fondo'"
        assert "texto" in paleta, f"Paleta '{nombre}' sin 'texto'"