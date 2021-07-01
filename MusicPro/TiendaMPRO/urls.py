from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login
from .views import Estrategia, RegistrarUsuario, Login,RegistraEstrateg, Registrar_vendedor, ProductoViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('productos', ProductoViewSet)

urlpatterns = [
    path('', Login.as_view(), name='login'),
    # url(r'^Productos/$', views.Productos, name="Productos"),
    url(r'^CommitPago/$', views.CommitPago, name="CommitPago"),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_producto/', views.updateProducto, name='update_producto'),
    path('registrar/', RegistrarUsuario.as_view(), name='registrar'),
    path('login/',Login.as_view(), name="login" ),
    path('logout/', logout_then_login, name='logout_usuario'),
    path('estrategias/', views.Estrategia, name='estrategias'),
    path('addEstrategia/',RegistraEstrateg.as_view(), name='addEstrategia'),
    path('registrar_trabajador/', Registrar_vendedor.as_view(), name='registrar_trabajador'),
    path('pedidos/', views.Pedido, name='pedidos'),
    path('pagos/', views.Transferencia, name='tfpagos'),
    path('products/<int:pk>/', views.detallePedido, name='detallePedido'),
    path('update_orden/', views.updateOrden, name='update_orden'),
    path('bodega/', views.productosBodega, name='bodega'),
    path('imagen/<int:pk>/', views.verImagen, name='imagenProducto'),
    path('ordenes_bodega/', views.ordenesBodega, name='ordenes_bodega'),
    path('orden/<int:pk>/', views.detalleOrden, name='ordenPedido'),
    path('crear_despacho/', views.crearDespacho, name='crear_despacho'),
    path('ordenes_despacho/', views.ordenesEnvio, name='ordenes_despacho'),
    path('cancelar_despacho/', views.cancelarDespacho, name='cancelar_despacho'),
    path('crear_direccion/', views.crearDireccion, name='crear_direccion'),
    path('api/', include(router.urls)),
    path('crear_producto/', views.CrearProducto.as_view(), name='addProducto'),
    path('delete_producto/<int:pk>/', views.DeleteProducto, name='delProducto'),


]