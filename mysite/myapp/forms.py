from django import forms
from .models import Publicaciones

class PublicacionForm(forms.ModelForm):

    cupos_maximos = forms.IntegerField(
        min_value=1,
        max_value=20,
        error_messages={
            'min_value': "Debe haber al menos 1 cupo.",
            'max_value': "No puedes asignar más de 20 cupos."
        },
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': 1,
            'max': 20
        })
    )

    class Meta:
        model = Publicaciones
        fields = ['titulo', 'contenido', 'sala', 'cupos_maximos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'cupos_maximos': forms.NumberInput(attrs={
                'class': 'form-control', 'min': 1, 'max': 20}),
        }