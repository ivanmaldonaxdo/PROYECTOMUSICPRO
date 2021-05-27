$(document).ready(main)
var checkeado = false;
function main() {
    $(function () {
        $('#entrega').click(
            function () {
                if (checkeado) {
                    $('.info-envio').show();
                    $('.info-retiro').hide();
                    console.log('ENVIO DESPLEGADO');
                    checkeado = false;
                }else{
                    $('.info-envio').hide();
                    $('.info-retiro').show();
                    console.log('RETIRO DESPLEGADO');
                    checkeado = true;
                }
        });
    });

};