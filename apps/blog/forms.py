from django import forms
from .models import ComentarioArticulo

class ComentarioForm(forms.ModelForm):
    
    class Meta:
        model = ComentarioArticulo
        fields = ['texto']
        widgets = {
            'texto' : forms.Textarea(attrs={
                'rows' : 4,
                'placeholder' : 'Escribe tu comentario aquí...',
            })
        }