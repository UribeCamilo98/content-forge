from pathlib import Path
from PIL import Image

class ImageManager:
    EXTENSIONES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

    def __init__(self):
        self.ruta_base = Path(__file__).resolve().parent.parent / "images"
        self.imagenes = self._escanear()
    
    def _escanear(self):
        imagenes = {}
        if self.ruta_base.exists():
            for archivo in self.ruta_base.iterdir():
                if archivo.suffix.lower() in self.EXTENSIONES:
                    imagenes[archivo.stem] = str(archivo.resolve())
        return imagenes

    def listar_imagenes(self):
        return list(self.imagenes.keys())
    
    def obtener_ruta(self, nombre):
        return self.imagenes.get(nombre)
    
    def refrescar(self):
        self.imagenes = self._escanear()

    def cargar_fondo(self, nombre, ancho, alto):
        ruta = self.obtener_ruta(nombre)
        if not ruta:
            return None
        img = Image.open(ruta).convert("RGB")
        img = img.resize((ancho, alto), Image.LANCZOS)
        return img
    
img_manager = ImageManager()