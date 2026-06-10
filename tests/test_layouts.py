import pytest
from utils.layouts import LayoutEngine

class TestPlaceholders:
    def test_circulo(self):
        img = LayoutEngine.generar_placeholder(100, "circulo")
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_estrella(self):
        img = LayoutEngine.generar_placeholder(100, "estrella")
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_diamante(self):
        img = LayoutEngine.generar_placeholder(100, "diamante")
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_marco(self):
        img = LayoutEngine.generar_placeholder(100, "marco")
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_formas_disponibles(self):
        assert LayoutEngine.FORMAS_PLACEHOLDER == ["circulo", "estrella", "diamante", "marco"]


class TestCalcularColocacion:
    def test_centro(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "centro", "tamano_porcentaje": 100}, 1080, 1080)
        assert "x" in col and "y" in col and "w" in col and "h" in col
        assert col["w"] > 0 and col["h"] > 0

    def test_izquierda_desborda(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "izquierda", "tamano_porcentaje": 100}, 1080, 1080)
        assert col["x"] < 0

    def test_derecha_desborda(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "derecha", "tamano_porcentaje": 100}, 1080, 1080)
        assert col["x"] + col["w"] > 1080

    def test_detras_llena_slide(self):
        col = LayoutEngine.calcular_colocacion("detras", {"posicion": "detras", "tamano_porcentaje": 100}, 1080, 1920)
        assert col["w"] >= 1920
        assert col["h"] >= 1920
        assert col["x"] <= 0
        assert col["y"] <= 0

    def test_tamano_200_porciento(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "centro", "tamano_porcentaje": 200}, 1080, 1080)
        assert col["w"] > 1080
        assert col["x"] < 0

    def test_arriba(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "arriba", "tamano_porcentaje": 100}, 1080, 1080)
        assert col["y"] < 0

    def test_abajo(self):
        col = LayoutEngine.calcular_colocacion("imagen", {"posicion": "abajo", "tamano_porcentaje": 100}, 1080, 1080)
        assert col["y"] + col["h"] > 1080

    def test_valores_por_defecto(self):
        col = LayoutEngine.calcular_colocacion("imagen", {}, 1080, 1080)
        assert col["x"] >= 0 and col["y"] >= 0
