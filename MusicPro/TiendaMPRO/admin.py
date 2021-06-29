from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register([Categoria,SubCategoria,TipoProducto,Producto, Usuario,
                    OrdenDeCompra, ProductoPedido, DireccionDeEnvio, EstrategiaDeVenta, Sucursal, SucursalDeEntrega,Pago])
