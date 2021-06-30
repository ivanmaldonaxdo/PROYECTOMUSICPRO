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
        if(action == 'agregar'){
            alert('Producto Añadido')
        }else if(action =='quitar'){
            alert('Producto Descontado')
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

    