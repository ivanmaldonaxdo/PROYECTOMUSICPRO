$(document).ready(inicio)

function inicio() {
    $(function() {
		$('#subcategoria').chained('#categoria');
        $('#tp_producto').chained('#subcategoria');
	});
};