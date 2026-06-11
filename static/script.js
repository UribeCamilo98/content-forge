document.addEventListener('DOMContentLoaded', function(){
    var paletaSelect = document.getElementById('paleta-select');
    var colorFondo = document.querySelector('input[name="color_fondo"]');
    var colorTexto = document.querySelector('input[name="color_texto"]');
    function aplicarPaleta(){
        var opt = paletaSelect.options[paletaSelect.selectedIndex];
        if(opt.value && opt.dataset.fondo){
            colorFondo.value=opt.dataset.fondo;
            colorTexto.value=opt.dataset.texto;
        }
    }
    aplicarPaleta();
    paletaSelect.addEventListener('change', aplicarPaleta);
    var form = document.getElementById('form-preview');
    var previewImg = document.getElementById('preview-img');
    var slideIndex = document.getElementById('slide_index');
    var slideCounter = document.getElementById('slide-counter');
    var totalSlides = 1;
    var debounceTimer;
    function actualizarPreview() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(function() {
            var formData = new FormData(form);
            formData.set('slide_index', slideIndex.value);
            fetch('/preview', {
                method: 'POST',
                body: formData
            })
            .then(function(resp) {
                totalSlides = parseInt(resp.headers.get('X-Total-Slides')) || 1;
                return resp.blob();
            })
            .then(function(blob) {
                var url = URL.createObjectURL(blob);
                previewImg.src = url;
                slideCounter.textContent = (parseInt(slideIndex.value) + 1) + '/' + totalSlides;
            })
            .catch(function(err) {
                console.error('Error en preview:', err);
                previewImg.src = '';
                slideCounter.textContent = 'Error';
            });
        }, 300);
    }
    form.addEventListener('change', actualizarPreview);
    form.addEventListener('input', actualizarPreview);
    document.getElementById('prev-slide').addEventListener('click', function() {
        var actual = parseInt(slideIndex.value);
        if (actual > 0) {
            slideIndex.value = actual - 1;
            actualizarPreview();
        }
    });
    document.getElementById('next-slide').addEventListener('click', function() {
        var actual = parseInt(slideIndex.value);
        if (actual < totalSlides - 1) {
            slideIndex.value = actual + 1;
            actualizarPreview();
        }
    });
    var opacidadSlider = document.getElementById('opacidad_imagen');
    var opacidadValor = document.getElementById('opacidad-valor');
    if (opacidadSlider && opacidadValor) {
        opacidadValor.textContent = opacidadSlider.value + '%';
        opacidadSlider.addEventListener('input', function() {
            opacidadValor.textContent = this.value + '%';
        });
    }

    function initToggle(checkboxId, controlsId) {
        var cb = document.getElementById(checkboxId);
        var ct = document.getElementById(controlsId);
        if (cb && ct) {
            ct.classList.toggle('hidden', !cb.checked);
            cb.addEventListener('change', function() {
                ct.classList.toggle('hidden', !this.checked);
            });
        }
    }
    initToggle('borde_activar', 'borde-controls');
    initToggle('sombra_activar', 'sombra-controls');
    initToggle('fondo_activar', 'fondo-controls');

    var overlayCheck = document.getElementById('overlay_activo');
    var overlayControls = document.getElementById('overlay-controls');
    var overlayPack = document.getElementById('overlay_pack');
    var overlayArchivo = document.getElementById('overlay_archivo');
    var overlayTamano = document.getElementById('overlay_tamano');
    var overlayTamanoValor = document.getElementById('overlay-tamano-valor');

    var overlaysData = typeof OVERLAYS_AGRUPADOS !== 'undefined' ? OVERLAYS_AGRUPADOS : {};

    var phColorLabel = document.getElementById('ph-color-label');

    function actualizarArchivosOverlay() {
        var pack = overlayPack.value;
        var archivos = overlaysData[pack] || [];
        overlayArchivo.innerHTML = '';
        archivos.forEach(function(a) {
            var opt = document.createElement('option');
            opt.value = a;
            opt.textContent = a;
            overlayArchivo.appendChild(opt);
        });
        if (phColorLabel) {
            phColorLabel.classList.toggle('hidden', pack !== 'placeholder');
        }
    }

    if (overlayCheck && overlayControls) {
        overlayControls.classList.toggle('hidden', !overlayCheck.checked);
        overlayCheck.addEventListener('change', function() {
            overlayControls.classList.toggle('hidden', !this.checked);
            actualizarPreview();
        });
    }
    if (overlayPack) {
        actualizarArchivosOverlay();
        overlayPack.addEventListener('change', function() {
            actualizarArchivosOverlay();
            actualizarPreview();
        });
    }
    if (overlayArchivo) {
        overlayArchivo.addEventListener('change', actualizarPreview);
    }
    if (overlayTamano && overlayTamanoValor) {
        overlayTamanoValor.textContent = overlayTamano.value + '%';
        overlayTamano.addEventListener('input', function() {
            overlayTamanoValor.textContent = this.value + '%';
            actualizarPreview();
        });
    }

    var overlayRotacion = document.getElementById('overlay_rotacion');
    var overlayRotacionValor = document.getElementById('overlay-rotacion-valor');
    if (overlayRotacion && overlayRotacionValor) {
        overlayRotacionValor.textContent = overlayRotacion.value + '°';
        overlayRotacion.addEventListener('input', function() {
            overlayRotacionValor.textContent = this.value + '°';
            actualizarPreview();
        });
    }

    var overlayOpacidad = document.getElementById('overlay_opacidad');
    var overlayOpacidadValor = document.getElementById('overlay-opacidad-valor');
    if (overlayOpacidad && overlayOpacidadValor) {
        overlayOpacidadValor.textContent = overlayOpacidad.value + '%';
        overlayOpacidad.addEventListener('input', function() {
            overlayOpacidadValor.textContent = this.value + '%';
            actualizarPreview();
        });
    }

    initToggle('overlay_borde_activar', 'overlay-borde-controls');
    var overlayBordeGrosor = document.getElementById('overlay_borde_grosor');
    var overlayBordeGrosorValor = document.getElementById('overlay-borde-grosor-valor');
    if (overlayBordeGrosor && overlayBordeGrosorValor) {
        overlayBordeGrosorValor.textContent = overlayBordeGrosor.value;
        overlayBordeGrosor.addEventListener('input', function() {
            overlayBordeGrosorValor.textContent = this.value;
        });
    }

    initToggle('overlay_sombra_activar', 'overlay-sombra-controls');
    var overlaySombraX = document.getElementById('overlay_sombra_offset_x');
    var overlaySombraXValor = document.getElementById('overlay-sombra-offset-x-valor');
    if (overlaySombraX && overlaySombraXValor) {
        overlaySombraXValor.textContent = overlaySombraX.value;
        overlaySombraX.addEventListener('input', function() {
            overlaySombraXValor.textContent = this.value;
        });
    }
    var overlaySombraY = document.getElementById('overlay_sombra_offset_y');
    var overlaySombraYValor = document.getElementById('overlay-sombra-offset-y-valor');
    if (overlaySombraY && overlaySombraYValor) {
        overlaySombraYValor.textContent = overlaySombraY.value;
        overlaySombraY.addEventListener('input', function() {
            overlaySombraYValor.textContent = this.value;
        });
    }

    var uploadInput = document.getElementById('upload-input');
    var btnUpload = document.getElementById('btn-upload');
    var uploadMensaje = document.getElementById('upload-mensaje');
    function recargarSelectFondo(nombreSeleccionado) {
        fetch('/listar-imagenes')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var select = document.querySelector('select[name="imagen_fondo"]');
            var valorActual = select.value;
            select.innerHTML = '<option value="">Ninguna (color sólido)</option>';
            if (data.preinstaladas && data.preinstaladas.length) {
                var optg = document.createElement('optgroup');
                optg.label = 'Preinstaladas';
                data.preinstaladas.forEach(function(img) {
                    var opt = document.createElement('option');
                    opt.value = img;
                    opt.textContent = img;
                    optg.appendChild(opt);
                });
                select.appendChild(optg);
            }
            if (data.subidas && data.subidas.length) {
                var optg = document.createElement('optgroup');
                optg.label = 'Subidas';
                data.subidas.forEach(function(img) {
                    var opt = document.createElement('option');
                    opt.value = img;
                    opt.textContent = img;
                    optg.appendChild(opt);
                });
                select.appendChild(optg);
            }
            if (nombreSeleccionado) {
                select.value = nombreSeleccionado;
            } else if (valorActual) {
                select.value = valorActual;
            }
        });
    }
    if (btnUpload && uploadInput) {
        btnUpload.addEventListener('click', function() {
            var archivo = uploadInput.files[0];
            if (!archivo) {
                uploadMensaje.textContent = 'Seleccioná un archivo primero';
                uploadMensaje.className = 'upload-error';
                return;
            }
            var formData = new FormData();
            formData.append('archivo', archivo);
            uploadMensaje.textContent = 'Subiendo...';
            uploadMensaje.className = '';
            fetch('/upload-fondo', { method: 'POST', body: formData })
            .then(function(r) {
                return r.json().then(function(data) { return { status: r.status, data: data }; });
            })
            .then(function(resp) {
                if (resp.data.ok) {
                    uploadMensaje.textContent = 'Imagen subida: ' + resp.data.nombre;
                    uploadMensaje.className = 'upload-success';
                    uploadInput.value = '';
                    recargarSelectFondo(resp.data.nombre);
                    actualizarPreview();
                } else {
                    uploadMensaje.textContent = 'Error: ' + resp.data.error;
                    uploadMensaje.className = 'upload-error';
                }
            })
            .catch(function(err) {
                uploadMensaje.textContent = 'Error de conexión';
                uploadMensaje.className = 'upload-error';
            });
        });
    }
    var btnGenerar = document.getElementById('btn-generar');
    var generarLoader = document.getElementById('generar-loader');
    if (btnGenerar) {
        btnGenerar.addEventListener('click', function() {
            var formData = new FormData(form);
            btnGenerar.disabled = true;
            if (generarLoader) generarLoader.classList.remove('hidden');
            fetch('/generar', { method: 'POST', body: formData })
            .then(function(resp) {
                var contentType = resp.headers.get('Content-Type') || '';
                if (contentType.includes('application/json')) {
                    return resp.json().then(function(data) {
                        alert('Error: ' + (data.error || 'Error al generar'));
                    });
                }
                if (!resp.ok) throw new Error('Error del servidor');
                return resp.blob().then(function(blob) {
                    var url = URL.createObjectURL(blob);
                    var a = document.createElement('a');
                    a.href = url;
                    var disposition = resp.headers.get('Content-Disposition') || '';
                    var match = disposition.match(/filename\*?=(?:UTF-8'')?["']?([^;"'\s]+)/i);
                    a.download = match ? match[1] : 'contentforge.zip';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                });
            })
            .catch(function(err) {
                alert('Error al generar: ' + err.message);
            })
            .finally(function() {
                btnGenerar.disabled = false;
                if (generarLoader) generarLoader.classList.add('hidden');
            });
        });
    }
    actualizarPreview();
});