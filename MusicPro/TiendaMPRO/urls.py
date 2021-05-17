from django.conf.urls import include, url
from . import views
from .views import home
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
]