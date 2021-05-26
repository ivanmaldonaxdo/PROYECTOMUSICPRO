from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.edit import FormView
import json
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Usuario
from .forms import FormularioRegistro, LoginUsuario
from django.contrib.auth import (authenticate, logout ,login)
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
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

    #Buscar el carro del sujeto
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
        itemsCarrito = order.get_carro_productos
    else:
        #llamar el carrito almacenado en Cookies
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}

        #Actualizar el icono del carro
        itemsCarrito = order['get_carro_productos']

        #Loop para leer los productos creados en el carrito de Cookies


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



#Registro de usuarios

class RegistrarUsuario(CreateView):
     model = Usuario
     form_class = FormularioRegistro
     template_name = 'TiendaMPRO/registrar.html'
     success_url = reverse_lazy('store')

# class Login(FormView):
#     template_name = 'login.html'
#     form_class = LoginUsuario
#     success_url = reverse_lazy('store')

#     @method_decorator(csrf_protect)
#     @method_decorator(never_cache)
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         else:








