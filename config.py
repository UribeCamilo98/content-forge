import os

MARGEN = 80
TEXTO_AREA = 1080

COLOR_FONDO = (25, 25, 35)
COLOR_TEXTO = (255, 255, 255)

RUTA_OUTPUT = os.path.join(os.path.dirname((__file__)), "output")

PRESETS_TAMANO = {
    "cuadrado": (1080, 1080),
    "vertical": (1080, 1920),
    "horizontal": (1920, 1080)
}

TAMANO_OPCIONES = list(range(10, 201, 5))