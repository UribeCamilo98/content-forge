import re
import os
from datetime import datetime
from generator.base import PlantillaBase
from config import RUTA_OUTPUT

class Carrusel(PlantillaBase):
    def __init__(self, textos, color_fondo, color_texto, num_slides=None, fuente=None, 
                 tamano=None, alineacion="centro", ancho=None, alto=None, contorno_color=None,
                 contorno_grosor=3, sombra_offset=None, sombra_color=(128, 128, 128),
                 ruta_imagen_fondo=None, opacidad_imagen=1.0, colocaciones=None):
        super().__init__(color_fondo,color_texto)
        self.textos = self._procesar_textos(textos,num_slides)
        self.tamano = tamano
        self.alineacion = alineacion
        self.fuente = fuente
        self.ancho = ancho
        self.alto = alto
        self.contorno_color = contorno_color
        self.contorno_grosor = contorno_grosor
        self.sombra_offset = sombra_offset
        self.sombra_color = sombra_color
        self.ruta_imagen_fondo = ruta_imagen_fondo
        self.opacidad_imagen = opacidad_imagen
        self.colocaciones = colocaciones

    def render_slide(self, indice=0):
        if indice < 0 or indice >= len(self.textos):
            indice = 0
        texto = self.textos[indice]
        return self._crear_imagen(texto, self.fuente,self.tamano, self.alineacion, self.ancho,
                                  self.alto, self.contorno_color, self.contorno_grosor, self.sombra_offset,
                                  self.sombra_color, ruta_imagen_fondo=self.ruta_imagen_fondo,
                                  opacidad_imagen=self.opacidad_imagen,
                                  colocaciones=self.colocaciones)

    def render_all(self):
        return [self._crear_imagen(
            t, self.fuente, self.tamano, self.alineacion, self.ancho,
            self.alto, self.contorno_color, self.contorno_grosor, self.sombra_offset,
            self.sombra_color, ruta_imagen_fondo=self.ruta_imagen_fondo,
            opacidad_imagen=self.opacidad_imagen,
            colocaciones=self.colocaciones
        ) for t in self.textos]

    def generar(self, ruta_destino=None):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if ruta_destino:
            base = ruta_destino
        else:
            base = RUTA_OUTPUT
        ruta_carpeta = os.path.join(base, timestamp)
        os.makedirs(ruta_carpeta,exist_ok=True)

        for i, texto in enumerate(self.textos):
            img = self._crear_imagen(texto, self.fuente, self.tamano, self.alineacion, self.ancho, 
                                     self.alto, self.contorno_color, self.contorno_grosor, self.sombra_offset,
                                     self.sombra_color, ruta_imagen_fondo=self.ruta_imagen_fondo,
                                     colocaciones=self.colocaciones)
            nombre = f"slide_{i+1:02d}.png"
            ruta = os.path.join(ruta_carpeta, nombre)
            img.save(ruta)
        
        return ruta_carpeta

    def _dividir_oraciones(self, texto):
        oraciones = re.split(r'(?<=[.!?])\s+', texto.strip())
        return [o for o in oraciones if o]
    
    def _distribuir(self, elementos, cantidad):
        grupos = []
        if cantidad <= 0:
            return grupos
        base = len(elementos) // cantidad
        resto = len(elementos) % cantidad
        idx=0
        for i in range(min(cantidad, len(elementos))):
            extra = 1 if i < resto else 0
            tope = idx + base + extra
            grupo = elementos[idx:tope]
            grupos.append(" ".join(grupo))
            idx=tope
        return grupos
    
    def _dividir_parrafos(self, oraciones_por_parrafo, cant_parrafos, num_slides):
        resultado = []
        slides_por_parrafo = num_slides // cant_parrafos
        resto = num_slides % cant_parrafos

        for i, oraciones in enumerate(oraciones_por_parrafo):
            extra = 1 if i < resto else 0
            slides_para_este = slides_por_parrafo + extra
            partes = self._distribuir(oraciones, slides_para_este)
            resultado.extend(partes)
        
        while len(resultado) < num_slides:
            resultado.append("...")
        
        return resultado

    def _procesar_textos(self, textos, num_slides=None):
        texto_normalizado= textos.replace('\r\n', '\n')
        parrafos_raw = texto_normalizado.split('\n\n')
        parrafos = []
        for p in parrafos_raw:
            p_limpio = p.strip()
            if p_limpio != "":
                parrafos.append(p_limpio)

        oraciones_por_parrafo = []
        for p in parrafos:
            oraciones = self._dividir_oraciones(p)
            oraciones_por_parrafo.append(oraciones)

        cant_parrafos=len(parrafos)
        if num_slides is None:
            num_slides = min(cant_parrafos, 20)
        else:
            num_slides = min(num_slides,20)

        if num_slides == cant_parrafos:
            return parrafos
        
        if num_slides < cant_parrafos:
            todas = []
            for oraciones in oraciones_por_parrafo:
                todas.extend(oraciones)
            return self._distribuir(todas, num_slides)

        if num_slides > cant_parrafos:
            return self._dividir_parrafos(oraciones_por_parrafo,cant_parrafos,num_slides)

