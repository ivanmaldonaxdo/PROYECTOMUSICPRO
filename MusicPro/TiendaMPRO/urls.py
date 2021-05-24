from django.conf.urls import include, url
from . import views
from .views import home, cart, checkout
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_producto/', views.updateProducto, name='update_producto')
]