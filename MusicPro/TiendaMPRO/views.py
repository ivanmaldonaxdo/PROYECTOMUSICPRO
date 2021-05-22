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
        for sb in subCateg:
            tipoProd=TipoProducto.objects.filter(sub_categ=sb).select_related('sub_categ')
            for tp in tipoProd:
                # print(subCateg)
                producto=Producto.objects.filter(tipo_prod=tp).select_related('tipo_prod')
                # print("Categoria: ", c ,", Subcateg: ",subCateg,", Tipo Prod: ", tipoProd,", Producto: ", producto )
                context={'categ':categ,"subCateg":subCateg,"tipoProd":tipoProd,"producto":producto}
                print(context)  
    return render(request, 'TiendaMPRO/Productos.html',context)
