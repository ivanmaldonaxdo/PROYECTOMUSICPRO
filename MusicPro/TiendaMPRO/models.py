from django.db import models
# from django.utils import timezone
from django.core.validators import MinLengthValidator



# Create your models here.
class Categoria(models.Model):
    categ_name = models.CharField(validators=[MinLengthValidator(3)],max_length=40,verbose_name="Categoria") 
    def __str__(self):
        return self.categ_name

class SubCategoria(models.Model):
    sub_categ_name = models.CharField(validators=[MinLengthValidator(3)],max_length=40,verbose_name="Sub-Categoria")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,verbose_name="Categoria")

    def __str__(self):
        return self.sub_categ_name

class TipoProducto(models.Model):
    tipo_name = models.CharField(validators=[MinLengthValidator(3)],max_length=40,verbose_name="Tipo de Producto")
    sub_categ = models.ForeignKey(SubCategoria, on_delete=models.CASCADE,verbose_name="SubCategoria")

    def __str__(self):
         return  self.tipo_name

# def ruta(filename):
#     return 'images/producto/{0}'+ '_'+'{1}'.format(pr.pk,filename)
class Producto(models.Model):
    nom_prod = models.CharField(validators=[MinLengthValidator(3)], max_length=40,verbose_name="Nombre de Producto")
    tipo_prod = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    descripcion = models.TextField(max_length=1500,null=True,blank=True)
    precio = models.FloatField(default=0.0)
    imagen = models.ImageField(upload_to="images/producto",null=True,blank=True)
    
    def __str__(self):
        return self.nom_prod
    
    
