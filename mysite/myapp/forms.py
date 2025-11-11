from django import forms
from .models import Publicaciones

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicaciones
        fields = ['titulo', 'contenido', 'sala', 'cupos_maximos']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control'}),
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'cupos_maximos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 20}),
        }