from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import fields, widgets
from .models import Usuario


class IniciarSesion(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(IniciarSesion, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Correo'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'

class RegistrarUsuario(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs= {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password1 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput(
        attrs= {
            'class': 'form-control',
            'placeholder': 'Repita la contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model: Usuario
        fields = ('email', 'nombre')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su correo'
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre'
                }
            )
        }


