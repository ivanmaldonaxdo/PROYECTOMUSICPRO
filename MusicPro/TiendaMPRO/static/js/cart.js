var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productoId = this.dataset.product
        var action = this.dataset.action
        console.log('productoId:', productoId, 'action:', action)

        console.log('Usuario:', user)
        if(user=== 'AnonymousUser'){
            console.log('No esta logeado')
        }else{
            actualizarOrdenUsuario(productoId, action)
        }
    })
}

function actualizarOrdenUsuario(productoId, action){
    console.log('El usuario esta logeado, enviado las weas a su carro')
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