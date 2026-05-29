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
    actualizarPreview();
});