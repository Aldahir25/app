"""Formularios de autenticación y registro de usuarios."""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Usuario


class RegistroUsuarioForm(UserCreationForm):
    """Formulario de registro para nuevos ciudadanos de Villa El Salvador."""

    email = forms.EmailField(required=True, label='Correo electrónico')
    dni = forms.CharField(
        max_length=8, min_length=8, required=False, label='DNI',
        help_text='8 dígitos.',
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'dni', 'telefono', 'direccion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['first_name'].label = 'Nombres'
        self.fields['last_name'].label = 'Apellidos'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'
        for name in ('username', 'first_name', 'last_name', 'email', 'dni', 'telefono', 'direccion'):
            self.fields[name].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_dni(self):
        dni = self.cleaned_data.get('dni', '')
        if dni and not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo números.')
        return dni

    def save(self, commit=True):
        user = super().save(commit=False)
        user.rol = 'ciudadano'
        if commit:
            user.save()
        return user
