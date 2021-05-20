from django.db import models
from django.utils import timezone


# Create your models here.
class Categoria(models.Model):
    """Model definition for ."""
    categ_name = models.TextField(min_length=6,max_length=30,verbose_name="Categoria")
    sub_categ = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.categ_name

class SubCategoria(models.Model):
    sub_categ_name = models.TextField(min_length=6,max_length=30,verbose_name="Sub-Categoria")
    tipo_prod = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    def __str__(self):
        return self.sub_categ_name

class TipoProducto(models.Model):
    tipo_name = models.TextField(min_length=6,max_length=30,verbose_name="Tipo de Producto")
    # TODO: Define fields here
    def __str__(self):
         return  self.tipo_name,

