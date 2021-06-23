$(document).ready(inicio)

function inicio() {
    $(function() {
		$('#subcategoria').chained('#categoria');
        $('#tp_producto').chained('#subcategoria');
	});

    $(function () {
        $("#categoria, #subcategoria, #tp_producto").on('change',function () {
            // alert("CBO CAMBIADO")
            // $("#filtro").submit();
           var v_categ=$("#categoria").val();
           var v_subcateg=$("#categoria").val();
           var v_tprod=$("#categoria").val();
           console.log("Categoria : ",v_categ," -subcategoria : ", v_subcateg," -tipo producto : ",v_tprod);
           $("#filtro").submit();

        });
    });

};