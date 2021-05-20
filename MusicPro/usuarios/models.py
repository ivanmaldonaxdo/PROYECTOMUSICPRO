from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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
    email = models.EmailField('Correo Electronico', max_length=100, unique=True)
    nombre = models.CharField('Nombre', max_length=100, null=True)
    usuario_activo= models.BooleanField(default=True)
    usuario_admin = models.BooleanField(default=False)
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