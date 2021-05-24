from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json

# import transbank.webpay.webpay_plus.transaction as tr
# from transbank import transaccion_completa as tc
# from transbank.common.integration_type import IntegrationType as it
# import random
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def home(request):
    return render(request, 'TiendaMPRO/home.html')

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
