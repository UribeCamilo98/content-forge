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

    def test_cuadrado(self):
        img = LayoutEngine.generar_placeholder(100, "cuadrado")
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_color_personalizado(self):
        img = LayoutEngine.generar_placeholder(100, "circulo", (255, 0, 0))
        assert img.mode == "RGBA"
        assert img.size == (100, 100)

    def test_formas_disponibles(self):
        assert LayoutEngine.FORMAS_PLACEHOLDER == ["circulo", "estrella", "cuadrado"]


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


class TestCalcularColocaciones:
    def test_collage_cantidad_5(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 5, "tam_min": 30, "tam_max": 100}, 1080, 1080)
        assert len(cols) == 5
        for c in cols:
            assert "x" in c and "y" in c and "w" in c and "h" in c
            assert c["w"] > 0 and c["h"] > 0

    def test_collage_tam_range(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 10, "tam_min": 30, "tam_max": 50}, 1080, 1080)
        assert len(cols) == 10
        for c in cols:
            lado_base = min(1080, 1080)
            min_esperado = int(lado_base * 0.3 * 0.7)
            max_esperado = int(lado_base * 0.5 * 0.7)
            assert min_esperado <= c["w"] <= max_esperado * 2

    def test_collage_area_izquierda(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 3, "tam_min": 30, "tam_max": 50, "area": "izquierda"}, 1080, 1080)
        centros_x = [c["x"] + c["w"] // 2 for c in cols]
        assert sum(centros_x) / len(centros_x) < 1080 // 2

    def test_collage_area_derecha(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 3, "tam_min": 30, "tam_max": 50, "area": "derecha"}, 1080, 1080)
        centros_x = [c["x"] + c["w"] // 2 for c in cols]
        assert sum(centros_x) / len(centros_x) > 1080 // 2

    def test_collage_rotacion_aleatoria(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 20, "tam_min": 30, "tam_max": 50, "rotacion_aleatoria": True, "separacion": 10}, 1080, 1080)
        rotaciones = [c.get("rotacion", 0) for c in cols]
        assert any(r != 0 for r in rotaciones)

    def test_collage_separacion_cero_mismo_centro(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 5, "tam_min": 30, "tam_max": 50, "separacion": 0}, 1080, 1080)
        assert len(cols) == 5
        centros_x = [c["x"] + c["w"] // 2 for c in cols]
        centros_y = [c["y"] + c["h"] // 2 for c in cols]
        # Con separacion 0 todos comparten el mismo centro
        assert all(x == centros_x[0] for x in centros_x)
        assert all(y == centros_y[0] for y in centros_y)

    def test_collage_separacion_alta_dispersa(self):
        cols = LayoutEngine.calcular_colocaciones("collage", {"cantidad": 3, "tam_min": 30, "tam_max": 40, "separacion": 90}, 1080, 1080)
        assert len(cols) == 3
        # Con separacion alta, los centros deberían estar dispersos
        centros_x = [c["x"] + c["w"] // 2 for c in cols]
        centros_y = [c["y"] + c["h"] // 2 for c in cols]
        # Verificar que no todos están en el mismo punto
        assert not (all(x == centros_x[0] for x in centros_x) and all(y == centros_y[0] for y in centros_y))

    def test_tapiz_horizontal(self):
        cols = LayoutEngine.calcular_colocaciones("tapiz", {"direccion": "horizontal", "tam_celda": 150, "espaciado": 10}, 1080, 1080)
        assert len(cols) > 0
        for c in cols:
            assert c["h"] == 150
            # Centrado verticalmente
            assert c["y"] + c["h"] // 2 == 1080 // 2

    def test_tapiz_vertical(self):
        cols = LayoutEngine.calcular_colocaciones("tapiz", {"direccion": "vertical", "tam_celda": 150, "espaciado": 10}, 1080, 1080)
        assert len(cols) > 0
        for c in cols:
            assert c["w"] == 150
            # Centrado horizontalmente
            assert c["x"] + c["w"] // 2 == 1080 // 2

    def test_tapiz_diagonal(self):
        cols = LayoutEngine.calcular_colocaciones("tapiz", {"direccion": "diagonal", "tam_celda": 150, "espaciado": 10}, 1080, 1080)
        assert len(cols) > 0
        for c in cols:
            # En diagonal, x e y aumentan juntos
            assert abs(c["x"] - c["y"]) < 10  # tolerancia por redondeo

    def test_tapiz_espaciado(self):
        cols_sin = LayoutEngine.calcular_colocaciones("tapiz", {"direccion": "horizontal", "tam_celda": 100, "espaciado": 0}, 500, 500)
        cols_con = LayoutEngine.calcular_colocaciones("tapiz", {"direccion": "horizontal", "tam_celda": 100, "espaciado": 50}, 500, 500)
        assert len(cols_sin) >= len(cols_con)  # con espaciado, caben menos
