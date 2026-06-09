# content‑forge

Aplicación web local para generar imágenes estáticas para TikTok (carruseles, frases, anuncios) usando Python + Flask + Pillow.

## Características (v1.2)

- **Carrusel de N slides** — divide automáticamente el texto en slides (por oraciones y párrafos)
- **Fuentes externas** — selector de fuentes .ttf con auto-ajuste si el texto no cabe
- **Tamaño de fuente manual** — slider de 10 a 200 px
- **Alineación de texto** — izquierda, centro, derecha, justificado
- **Borde y sombra en texto** — contorno configurable (color + grosor) y sombra desplazada (offset X/Y + color)
- **Selector de color interactivo** — color pickers hex + paletas predefinidas sincronizadas
- **Preview en vivo (AJAX)** — vista previa automática sin recargar la página, con navegación entre slides
- **Presets de tamaño** — cuadrado (1080×1080), vertical (1080×1920), horizontal (1920×1080)
- **Paletas de color** — varios esquemas predefinidos
- **Imagen de fondo** — seleccionar imágenes locales o subir nuevas desde el navegador, con control de opacidad para legibilidad del texto
- **Upload de imágenes** — subir imágenes desde el PC, se guardan en `images/uploads/` y aparecen en un grupo separado
- **Descarga ZIP** — al generar, se descarga un ZIP con todos los slides (diálogo Guardar aso nativo del navegador)

## Requisitos

- Python 3.9+
- pip

## Instalación

```bash
git clone <repo>
cd contentforge
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Uso

```bash
python app.py
```

Abrir `http://localhost:5000`. Escribir texto, elegir opciones, ver el preview en vivo y hacer clic en "Generar Carrusel". Se descargará un ZIP con los slides generados.

## Tests

```bash
pytest tests/ -v
```

## Roadmap

| Versión | Estado            |
|---------|-------------------|
| v1.0    | ✅ Completa       |
| v1.1    | ✅ Completa       |
| v1.2    | ✅ Completa       |
| v1.3    | 🔮 Layouts con imágenes |
| v1.4    | 🔮 Editor visual con canvas |
