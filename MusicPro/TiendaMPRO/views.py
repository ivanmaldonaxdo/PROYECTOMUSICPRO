from django.db.models.query import QuerySet
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
import transbank.webpay.webpay_plus.transaction as tr
import random
# Create your views here.
from django.http import JsonResponse, request
from django.views.generic.edit import DeleteView, FormView
import json
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Usuario, EstrategiaDeVenta
from .forms import FormularioRegistro, LoginUsuario
from django.contrib.auth import (authenticate, logout ,login)
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from .forms import FormEstrategiaVta
from django.db.models import Q
# Create your views here.


def home(request):
    categ=Categoria.objects.all()
    context={'categ':categ}
    return render(request, 'TiendaMPRO/login.html',context)

@login_required
def store(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
        itemsCarrito = order.get_carro_productos
    else:
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
        itemsCarrito = order['get_carro_productos']

    categ=Categoria.objects.all()
    subcateg=SubCategoria.objects.all()
    tpProductos=TipoProducto.objects.all()
    productos = Producto.objects.all()
    queryset=request.GET.get("busqueda")
    q_tipoprod= request.GET.get('cbotipoproducto')
    q_searched=""
    q_subcateg=request.GET.get('cbosubcateg')
    q_categ=request.GET.get('cbocateg')
    if queryset:
        productos=Producto.objects.filter(Q(nom_prod__icontains=queryset))
        print("FILTRO POR NOM PRODUCTO: ")
        q_searched=queryset
    elif q_tipoprod:
        productos=Producto.objects.filter(Q(tipo_prod=q_tipoprod))
        print("FILTRO POR TIPO PROD: ")
        q_searched=q_tipoprod

    context = {'productos' : productos, 'itemsCarrito' : itemsCarrito,'categ':categ,'subcateg':subcateg,'tiposproducto':tpProductos,'q_searched':q_searched}
    return render(request, 'TiendaMPRO/store.html', context)

@login_required
def cart(request):

    #Buscar el carro del sujeto
    if request.user.is_authenticated:
        customer = request.user
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

@login_required
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        items = order.productopedido_set.all()
        total=order.get_total_descuento
        itemsCarrito = order.get_carro_productos
        currentUrl=request.build_absolute_uri()
        url_sep=currentUrl.rsplit(sep="/" ,maxsplit=2)
        retorno=url_sep[0] + '/CommitPago/'
        session_id=random.randint(10000000,99999999)
        #LLAMADA DE METODO | tr.Transaction.create() > DE TRANSBANK PARA REALIZAR UNA TRASNACCIÓN
        response=tr.Transaction.create(order.id,session_id,total,retorno)
        #SE DEFINE | def token() > COMO GLOBAL PARA QUE RETORNE TOKEN TBK Y SE LLAME EN OTRAS VISTAS
        global token
        def token(): 
            return response.token
    else:
        items = []
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
        itemsCarrito = order['get_carro_productos']
    
    print("Token a Boton: ",response.token)
    context = {'items': items, 'order': order,'response':response, 'itemsCarrito': itemsCarrito}
    return render(request, 'TiendaMPRO/checkout.html', context)


def updateProducto(request):
    data = json.loads(request.body)
    productoId = data['productoId']
    action = data['action']

    customer = request.user
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
     success_url = reverse_lazy('login')

class Login(FormView):
    template_name = 'TiendaMPRO/login.html'
    form_class = LoginUsuario
    success_url = reverse_lazy('store')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/TiendaMPRO/login/')

@csrf_exempt
def Pagar(request):
    print(request.GET)
    queryset=request.GET.get("busqueda")
    q_categoria=request.GET.get("cbocategoria")
    print(queryset)
    print(q_categoria)
    categ=Categoria.objects.all()
    subcateg=SubCategoria.objects.none()
    total=25000
    if queryset:
        producto=Producto.objects.filter(
        Q(nom_prod__icontains=queryset)
        )

    else:
        producto =Producto.objects.all()
        # subcateg=SubCategoria.objects.filter(id=1)
        print(subcateg)
        # tiproduct=TipoProducto.objects.all()

    #    total=getattr(producto,"precio")

    data={}
    try:
        action=request.POST['action']
        if action ==  'display_subcateg':
            data=[]
            for i in SubCategoria.objects.filter(id=request.POST['id']):
                data.append(i.toJSON())
                
            print(data)
        else:
            data['error']='Ha ocurrido un error'        
    except Exception as e:
        data['error']=str(e)
    # jr=JsonResponse(data,safe=False)

    # return JsonResponse(data,safe=False)
    print('Total: ',total)
    currentUrl=request.build_absolute_uri()
    url_sep=currentUrl.rsplit(sep="/" ,maxsplit=2)
    retorno=url_sep[0] + '/CommitPago/'
    print('Url A Retornar: ',retorno)
    orden_compra=random.randint(10000000,99999999)
    session_id=random.randint(10000000,99999999)
    response=tr.Transaction.create(orden_compra,session_id,total,retorno)
    
    # print("Token a enviar a Commit Pagar: ",token())
    context={'producto':producto,'response':response,'categ':categ,'subcateg':subcateg}
    return render(request,'TiendaMPRO/Pagar.html',context)
    # ,JsonResponse(data,safe=False)

@csrf_exempt
def CommitPago(request):
    transaction_id = random.randint(10000000,99999999)
    try:
        tk= token()
        response=tr.Transaction.commit(tk)
        if response.response_code == 0:
            id_order = response.buy_order
            order, created = OrdenDeCompra.objects.get_or_create(id=id_order, complete=False)
            order.transaction_id = transaction_id
            order.complete = True
            order.save()
        else:
            print('El pago fue rechazado')
        context={'tk':tk,'respse':response, 'order': order}

    except:
        print('El usuario rechazo la transaccion')
        context={}
    return render(request, 'TiendaMPRO/CommitPago.html',context)

        
    
def Estrategia(request):
    estrategias = EstrategiaDeVenta.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        order, created = OrdenDeCompra.objects.get_or_create(customer=customer, complete=False)
        itemsCarrito = order.get_carro_productos
    else:
        order= {'get_total_carro': 0, 'get_carro_productos': 0}
        itemsCarrito = order['get_carro_productos']
    context ={'itemsCarrito' : itemsCarrito, 'est': estrategias}
    return render(request, 'TiendaMPRO/estrategias.html', context)

class RegistraEstrateg(CreateView):
    model=EstrategiaDeVenta
    form_class=FormEstrategiaVta
    template_name='TiendaMPRO/addEstrategia.html'
    success_url=reverse_lazy('estrategias')