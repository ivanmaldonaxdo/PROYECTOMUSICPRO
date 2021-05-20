from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'TiendaMPRO/home.html')

def Productos(request):
    return render(request, 'TiendaMPRO/Productos.html')
