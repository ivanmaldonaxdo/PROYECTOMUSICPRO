from django.shortcuts import render
from .models import *
# import transbank.webpay.webpay_plus.transaction as tr
# from transbank import transaccion_completa as tc
# from transbank.common.integration_type import IntegrationType as it
# import random
# from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    return render(request, 'TiendaMPRO/home.html')

def Productos(request):
    # id_categ=Categoria.objects.all()
    categ=Categoria.objects.all()
    for c in categ:
        # print(c)
        subCateg=SubCategoria.objects.filter(categoria=c).select_related('categoria')
        context={'categ':categ}
        # print(subCateg)
        print("Categoria: ", c ,"Subcateg: ",subCateg)

        # sb=getattr(subCateg,"sub_categ_name")
        # print(categ)
        # print(subCateg)
        # print("sb",sb)
        # print(categ.get(id))
        # prod=Producto.objects.all()
        # subCateg=SubCategoria.objects.filter(categoria=id_categ)
    return render(request, 'TiendaMPRO/Productos.html',context)
