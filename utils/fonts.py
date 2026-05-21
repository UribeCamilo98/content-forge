from pathlib import Path

class FontManager:
    def __init__(self):
        self.ruta_base = Path(__file__).resolve().parent.parent / "fonts"
        self.fuentes = self._escanear()

    def _escanear(self):
        fuentes = {}
        if self.ruta_base.exists():
            for archivo in self.ruta_base.iterdir():
                if archivo.suffix.lower() == ".ttf":
                    fuentes[archivo.stem] = str(archivo.resolve())
        return fuentes

    def listar_fuentes(self):
        return list(self.fuentes.keys())
    
    def obtener_ruta(self, nombre):
        return self.fuentes.get(nombre)
    

font_manager = FontManager()