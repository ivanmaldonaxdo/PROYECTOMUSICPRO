from django.shortcuts import render
from .models import *
import transbank.webpay.webpay_plus.transaction as tr
import random
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def home(request):
    categ=Categoria.objects.all()
    context={'categ':categ}
    return render(request, 'TiendaMPRO/home.html',context)

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
    print(response.response_code)
    return render(request, 'TiendaMPRO/CommitPago.html',context)
    # return render(request, 'TiendaMPRO/CommitPago.html')