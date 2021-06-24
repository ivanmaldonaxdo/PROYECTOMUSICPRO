$(document).ready(inicio)
function inicio() {
    //#region ANIOANDO COMBOBOXES
    $(function () {
        $('#subcategoria').chained('#categoria');
        $('#tp_producto').chained('#subcategoria');
    });
    //#endregion
    //#region SUBMIT AL CAMBIAR DATO DE ENTRADA
        // $('#buscar').on('change',function () {
        //     $('filtro').submit();
        // });
    //#endregion
};