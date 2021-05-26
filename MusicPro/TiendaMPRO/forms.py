from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.forms import fields, widgets
from .models import Usuario


#Formulario de registro
class FormularioRegistro(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Repita la contraseña', widget = forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente la contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ('email', 'nombre')
        widgets= {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su correo electronico'
                }
            ),
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre'
                }
            )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit = True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginUsuario(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginUsuario, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Ingrese su correo'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'