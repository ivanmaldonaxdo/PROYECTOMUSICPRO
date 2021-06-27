var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productoId = this.dataset.product
        var action = this.dataset.action
        if(user=== 'AnonymousUser'){
            agregarProductoCookie(productoId, action)
        }else{
            actualizarOrdenUsuario(productoId, action)
        }
    })
}

//function agregarProductoCookie(productoId, action){
   // if (action == 'agregar'){
        //if (cart[productoId]==undefined){
         //   cart[productoId] = {'cantidad': 1}
        //}else{
        //    cart[productoId]['cantidad'] += 1
      //  }
    //}
    //if (action == 'quitar'){
        //cart[productoId]['cantidad'] -=1

        //if (cart[productoId]['cantidad']<=0){
          //  delete cart[productoId]
      //  }
    //}
    //document.cookie='cart=' + JSON.stringify(cart) + ";domain=;path=/"
   // location.reload()
//}


function actualizarOrdenUsuario(productoId, action){
    var url = '/update_producto/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productoId': productoId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

var envio = document.getElementById('entrega')
	var total = '{{order.get_total_descuento|floatformat:0}}'

	envio.addEventListener('change', function(e){
		e.preventDefault()
		if (this.checked){
			document.getElementById('shipping-info').classList.remove("hidden");
			document.getElementById('info-sucursal').classList.add("hidden");
		}else{
			document.getElementById('shipping-info').classList.add("hidden");
			document.getElementById('info-sucursal').classList.remove("hidden");
		}
	})

	var form = document.getElementById('form')
	form.addEventListener('submit', function(e){
		e.preventDefault()
		console.log('form enviado')
		document.getElementById('form-button').classList.add("hidden");
		document.getElementById('payment-info').classList.remove("hidden");
	})

	document.getElementById('make-payment').addEventListener('click', function(e){
		submitFormData()
	})
	function submitFormData(){
		console.log('Boton pagar clickeado')

		var datosUser = {
			'total': total
		}

		var shippingInfo = {
			'address': null,
			'city': null,
			'state': null,
			'zipcode': null,
			'country': null,
		}

		var sucursal = {
			'ciudad': null,
		}

		if (envio.checked){
			shippingInfo.address = form.address.value
			shippingInfo.city = form.city.value
			shippingInfo.state = form.state.value
			shippingInfo.zipcode = form.zipcode.value
			shippingInfo.country = form.country.value
		}else{
			sucursal.ciudad = form.tienda.value
		}

		var url = '/CommitPago/'
		
		fetch(url,{
			method:'POST',
			headers:{
				'Content-Type':'applicacion/json',
				'X-CSRFToken': csrftoken,
			},
			body:JSON.stringify({'shippingInfo.address' : shippingInfo})

		})
		.then((response)=>{
        	return response.json()
    	})
		.then((data)=>{
			console.log('Success:', data);
		})
	}