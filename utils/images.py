import os
import re
from pathlib import Path
from PIL import Image
from config import RUTA_IMAGENES

class ImageManager:
    EXTENSIONES = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    NOMBRE_SEGURO_RE = re.compile(r"^[a-zA-Z0-9_\-]+$")

    def __init__(self):
        self.ruta_base = Path(RUTA_IMAGENES)
        self.ruta_uploads = self.ruta_base / "uploads"
        self.preinstaladas = {}
        self.subidas = {}
        self._escanear_todo()

    def _escanear_directorio(self, ruta):
        imagenes = {}
        if ruta and ruta.exists():
            for archivo in ruta.iterdir():
                if archivo.suffix.lower() in self.EXTENSIONES:
                    imagenes[archivo.stem] = str(archivo.resolve())
        return imagenes

    def _escanear_todo(self):
        self.preinstaladas = self._escanear_directorio(self.ruta_base)
        self.subidas = self._escanear_directorio(self.ruta_uploads)

    def _combinar(self):
        d = {}
        d.update(self.preinstaladas)
        d.update(self.subidas)
        return d

    def listar_imagenes(self):
        return list(self._combinar().keys())

    def listar_agrupadas(self):
        return {
            "preinstaladas": list(self.preinstaladas.keys()),
            "subidas": list(self.subidas.keys()),
        }

    def obtener_ruta(self, nombre):
        d = self._combinar()
        return d.get(nombre)

    def refrescar(self):
        self._escanear_todo()

    def cargar_fondo(self, nombre, ancho, alto):
        ruta = self.obtener_ruta(nombre)
        if not ruta:
            return None
        img = Image.open(ruta).convert("RGB")
        img = img.resize((ancho, alto), Image.LANCZOS)
        return img

    def guardar_archivo(self, nombre_archivo, contenido):
        ext = Path(nombre_archivo).suffix.lower()
        if ext not in self.EXTENSIONES:
            raise ValueError(f"Extensión no permitida: {ext}")
        self.ruta_uploads.mkdir(parents=True, exist_ok=True)
        stem = Path(nombre_archivo).stem
        stem_seguro = re.sub(r"[^a-zA-Z0-9_\-]", "_", stem)[:60]
        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_final = f"{stem_seguro}_{timestamp}{ext}"
        ruta_destino = self.ruta_uploads / nombre_final
        with open(ruta_destino, "wb") as f:
            f.write(contenido)
        self.refrescar()
        return Path(nombre_final).stem

img_manager = ImageManager()