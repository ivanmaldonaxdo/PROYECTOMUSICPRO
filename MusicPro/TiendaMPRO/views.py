from django.shortcuts import render
from transbank.webpay.webpay_plus import response
from .models import *
import transbank.webpay.webpay_plus.transaction as tr
import transbank.webpay.webpay_plus.deferred_transaction as df
import random
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from django.http import JsonResponse
import json

# import transbank.webpay.webpay_plus.transaction as tr
# from transbank import transaccion_completa as tc
# from transbank.common.integration_type import IntegrationType as it
# import random
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    categ=Categoria.objects.all()
    context={'categ':categ}
    # list_resp_comercio=[[-1,"Rechazo - Posible error en el ingreso de datos de la transacción"],
    #                     [-2,"Rechazo - Se produjo fallo al procesar la transacción, este mensaje"+
    #                     "de rechazo se encuentra relacionado a parámetros de la tarjeta y/o su cuenta asociada"],
    #                     [-3,"Rechazo - Error en Transacción"	]]
    # print(list_resp_comercio)
    return render(request, 'TiendaMPRO/home.html',context)

def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
        itemsCarrito = order.get_carro_productos
    else:
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
        itemsCarrito = order['get_carro_productos']

    productos = Producto.objects.all()
    context ={'productos' : productos, 'itemsCarrito' : itemsCarrito}
    return render(request, 'TiendaMPRO/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
        itemsCarrito = order.get_carro_productos
    else:
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
        itemsCarrito = order['get_carro_productos']
    context = {'items': items, 'order': order, 'itemsCarrito': itemsCarrito}
    return render(request, 'TiendaMPRO/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
    else:
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
    context = {'items': items, 'order': order}
    return render(request, 'TiendaMPRO/checkout.html', context)

def updateProducto(request):
    data = json.loads(request.body)
    productoId = data['productoId']
    action = data['action']

    customer = request.user.customer
    producto = Producto.objects.get(id=productoId)
    order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
    productoPedido, created = ProductoPedido.objects.get_or_create(orden=order, producto=producto)

    if action == 'agregar':
        productoPedido.cantidad= (productoPedido.cantidad + 1)
    elif action == 'quitar':
        productoPedido.cantidad = (productoPedido.cantidad - 1)

    productoPedido.save()


    if productoPedido.cantidad <=0:
        productoPedido.delete()

    return JsonResponse('El item fue agregado', safe=False )


def Productos(request):
    # id_categ=Categoria.objects.all()
    categ=Categoria.objects.all()
    for c in categ:
        # print(c)
        subCateg=SubCategoria.objects.filter(categoria=c).select_related('categoria')
        for sb in subCateg:
            tipoProd=TipoProducto.objects.filter(sub_categ=sb).select_related('sub_categ')
            for tp in tipoProd:
                # print(subCateg)
                producto=Producto.objects.filter(tipo_prod=tp).select_related('tipo_prod')
                # print("Categoria: ", c ,", Subcateg: ",subCateg,", Tipo Prod: ", tipoProd,", Producto: ", producto )
                context={'categ':categ,"subCateg":subCateg,"tipoProd":tipoProd,"producto":producto}
                print(context)  
    return render(request, 'TiendaMPRO/Productos.html',context)

def Pagar(request):
    producto =Producto.objects.all()
    total=0
    for pr in producto:
        precio=getattr(pr,"precio")
        total+=precio
        print('Precio: ',precio)
    print('Total: ',total)
    currentUrl=request.build_absolute_uri()
    url_sep=currentUrl.rsplit(sep="/" ,maxsplit=2)
    retorno=url_sep[0] + '/CommitPago/'
    print('Url A Retornar: ',retorno)
    orden_compra=random.randint(10000000,99999999)
    session_id=random.randint(10000000,99999999)
    response=tr.Transaction.create(orden_compra,session_id,total,retorno)
    global token
    def token():
        return response.token
    print("Token a enviar a Commit Pagar: ",token())
    context={'producto':producto,'response':response}
    return render(request,'TiendaMPRO/Pagar.html',context)

@csrf_exempt
def CommitPago(request):
    tk= token()
    print("Token recibido dede Pago: ",token())
    response=tr.Transaction.commit(tk)
    context={'tk':tk,'respse':response}
    rpse_code=response.response_code
    print(rpse_code)
    return render(request, 'TiendaMPRO/CommitPago.html',context)