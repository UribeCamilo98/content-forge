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
})