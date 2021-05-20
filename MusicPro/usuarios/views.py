from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from .models import Usuario
from .forms import RegistrarUsuario
from django.urls import reverse_lazy

# Create your views here.


