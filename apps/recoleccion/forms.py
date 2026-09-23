from django import forms
from .models import Recoleccion


class RecoleccionForm(forms.ModelForm):
    class Meta:
        model = Recoleccion
        fields = ['punto', 'operador', 'estado', 'destino', 'peso_total', 'observaciones']
        widgets = {
            'punto': forms.Select(attrs={'class': 'form-control'}),
            'operador': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'peso_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ConfirmarRecoleccionForm(forms.ModelForm):
    """Formulario de confirmación de recolección para el operador."""

    class Meta:
        model = Recoleccion
        fields = ['peso_total', 'destino', 'observaciones']
        widgets = {
            'peso_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Planta de tratamiento'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
