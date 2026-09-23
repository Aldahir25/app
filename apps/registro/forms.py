from django import forms
from .models import PuntoAcopio, RegistroRAEE


class RegistroRAEEForm(forms.ModelForm):
    class Meta:
        model = RegistroRAEE
        fields = [
            'categoria',
            'tipo_aparato',
            'marca',
            'modelo',
            'descripcion',
            'peso_estimado',
            'cantidad',
            'punto_acopio',
            'zona',
            'estado',
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'tipo_aparato': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'peso_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'punto_acopio': forms.Select(attrs={'class': 'form-control'}),
            'zona': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['punto_acopio'].queryset = PuntoAcopio.objects.filter(activo=True)

        if self.user and self.user.rol == 'operador':
            self.fields['punto_acopio'].queryset = PuntoAcopio.objects.filter(
                operador=self.user,
                activo=True,
            )
