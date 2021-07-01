from django.db import models
# from django.utils import timezone
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password = None):
        if not email:
            raise ValueError('El usuario debe tener un correo electronico')

        user = self.model(
            email = self.normalize_email(email),
            nombre = nombre
            
        )

        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, nombre, password):
        user = self.create_user(
            email,
            nombre=nombre,
            password=password
        )
        user.usuario_admin = True
        user.save()
        return user



class Usuario(AbstractBaseUser):
    email = models.EmailField('Correo Electronico', max_length=100, unique=True,)
    nombre = models.CharField('Nombre', max_length=100, null=True)
    usuario_activo= models.BooleanField(default=True)
    usuario_admin = models.BooleanField(default=False)
    usuario_vend = models.BooleanField(default=False, verbose_name='Vendedor', null=True)
    usuario_bodega = models.BooleanField(default=False, verbose_name='Bodeguero', null=True)
    usuario_contador = models.BooleanField(default=False, verbose_name='Contador', null=True)
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =  ['nombre']

    def __str__(self):
        return f'{self.nombre}'


    def has_perm(self,perm,obj = None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_admin
    
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

    @property
    def imageURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url


class OrdenDeCompra(models.Model):
    customer = models.ForeignKey(Usuario, on_delete=models.SET_NULL, blank=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    retiroTienda = models.BooleanField(default=False, null=True, blank=False)
    transaction_id=  models.CharField(max_length=200, null=True)
    pagado = models.BooleanField(default=False, null=True, blank=False)
    transferencia = models.BooleanField(default=False, null=True, blank=False)
    aceptada = models.BooleanField(default=False, null=True, blank=False)
    estado = models.CharField(max_length=200, null=True, blank=True, default="En Bodega")

    
    def __str__(self):
        return str(self.id)
    
    @property
    def get_total_carro(self):
        orderitems = self.productopedido_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    

    @property
    def get_total_descuento(self):
        orderitems = self.productopedido_set.all()
        if (sum ([item.cantidad for item in orderitems])>=4):
            total = sum([item.get_total for item in orderitems])-20000
        else:
            total = sum([item.get_total for item in orderitems])
        
        return total

    @property
    def get_carro_productos(self):
        orderitems = self.productopedido_set.all()
        total = sum ([item.cantidad for item in orderitems])
        return total

    
    @property
    def envio(self):
        envio = False
        order = OrdenDeCompra.objects.all()
        for i in order:
            if i.retiro_tienda == False:
                envio = True
        return envio

        

class ProductoPedido(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=True, null=True)
    orden = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.producto.precio * self.cantidad
        return total

class DireccionDeEnvio(models.Model):
    customer =  models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(OrdenDeCompra, on_delete=models.CASCADE, blank=True, null=True)
    direccion = models.CharField(max_length=200, null=True)
    ciudad = models.CharField(max_length=200, null=True)
    estado_comuna = models.CharField(max_length=200, null=True)
    codigo_postal = models.CharField(max_length=200, null=True)
    pais = models.CharField(max_length=200, null=True)
    fecha_pedido = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.direccion


class EstrategiaDeVenta(models.Model):
    titulo = models.CharField(max_length=200)
    estrategia = models.TextField(max_length=1500,null=True,blank=True)
    fecha_creacion_modificacion = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.titulo

class Pago(models.Model):
    order = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, blank=True, null=True)
    cuenta_id = models.FloatField(default=0.0)
    monto = models.FloatField(default=1.0)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=200, null=True,blank= True)
    def __str__(self):
        return self.mensaje


class Sucursal(models.Model):
    ciudad = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.ciudad

class SucursalDeEntrega(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, blank=True, null=True)


class OrdenDeEntrega(models.Model):
    order = models.ForeignKey(OrdenDeCompra, on_delete=models.SET_NULL, blank=True, null=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    ciudad = models.CharField(max_length=200, null=True, blank=True)
    pais = models.CharField(max_length=200, null=True, blank=True)
    fecha_de_entrega = models.DateTimeField(null=True)







