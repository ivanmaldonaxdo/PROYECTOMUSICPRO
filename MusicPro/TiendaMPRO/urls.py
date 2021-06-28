from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login
from .views import Estrategia, RegistrarUsuario, Login,RegistraEstrateg, Registrar_vendedor
from django.urls import path

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
<<<<<<< HEAD
    path('pagos/', views.Transferencia, name='tfpagos')

=======
    path('products/<int:pk>/', views.detallePedido, name='detallePedido'),
>>>>>>> 4663f54ddda47d5b562163b5db3ba934224e65f8


]