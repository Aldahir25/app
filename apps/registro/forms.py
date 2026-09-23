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
            'categoria': forms.Select(attrs={'class': 'form-control', 'id': 'id_categoria'}),
            'tipo_aparato': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'id_tipo_aparato', 'autocomplete': 'off'}
            ),
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
        # Si el ciudadano omite la categoría, se asigna automáticamente (IA)
        self.fields['categoria'].required = False
        self.fields['punto_acopio'].queryset = PuntoAcopio.objects.filter(activo=True)

        if self.user and self.user.rol == 'operador':
            self.fields['punto_acopio'].queryset = PuntoAcopio.objects.filter(
                operador=self.user,
                activo=True,
            )

        # Los ciudadanos registran a nombre propio: se ocultan usuario y estado.
        if self.user and self.user.rol == 'ciudadano':
            self.fields.pop('usuario', None)
            self.fields.pop('estado', None)

    def clean_categoria(self):
        """Aplica la clasificación inteligente si el ciudadano omitió la categoría."""
        categoria = self.cleaned_data.get('categoria')
        tipo = self.cleaned_data.get('tipo_aparato')
        if not categoria and tipo:
            from .services import clasificar_aparato

            sugerida = clasificar_aparato(tipo)
            if sugerida:
                from .models import CategoriaRAEE

                categoria, _ = CategoriaRAEE.objects.get_or_create(
                    nombre=sugerida,
                    defaults={'descripcion': 'Categoría UNITAR asignada automáticamente.'},
                )
        return categoria
