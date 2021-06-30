$(document).ready(inicio)
function inicio() {
    //#region ANIOANDO COMBOBOXES
    $(function () {
        $('#subcategoria').chained('#categoria');
        $('#tp_producto').chained('#subcategoria');
        //AJUSTE DE ANCHO EN CBOBOX POR DEFECTO
        $('#subcategoria,#tp_producto').width("68%");
        $('#subcategoria').width("55%");

        // $('#categoria').width("72%");

    });
 
};