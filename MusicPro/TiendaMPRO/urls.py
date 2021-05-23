from django.conf.urls import include, url
from . import views
from .views import home
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    url(r'^Productos/$', views.Productos, name="Productos"),
    url(r'^Pagar/$', views.Pagar, name="Pagar"),
    url(r'^CommitPago/$', views.CommitPago, name="CommitPago"),


]